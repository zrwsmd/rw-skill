---
name: ld-json-generator
description: >
  生成 IEC 61131-3 梯形图（Ladder Diagram）专用 JSON 格式。当用户用自然语言描述梯形图逻辑时，
  直接输出可供前端渲染器使用的完整 JSON 结构，包含 segmentList、variableList 等所有字段。
  触发场景：用户描述"梯形图"、"LD程序"、"PLC逻辑"、"触点线圈"、"功能块"、"CTU/CTD/TON/TOF/TP/SR/RS"
  等关键词，或要求"生成JSON"、"转成JSON"、"写成梯形图格式"时，必须使用本 Skill。
  即使用户只是说"帮我写一段XX逻辑的梯形图"，也应使用本 Skill 输出 JSON。
  严格禁止：FBDCompartment 外层出现 varName；port 条目出现 name/value/scope/type 以外的字段。
---

# IEC 61131-3 梯形图 JSON 生成器

## 目标
将用户的自然语言梯形图描述转换为标准 JSON 格式，该格式可直接被前端梯形图渲染器使用。

## 输出结构总览

```json
[{
  "segmentList": [
    { ...segment1... },
    { ...segment2... }
  ],
  "variableList": [
    { ...variable1... },
    { ...variable2... }
  ],
  "pouType": "PROGRAM",
  "pouName": "用户指定名称，未指定时默认 MAIN",
  "extensionPath": ""
}]
```

> 详细字段规范见 `references/schema.md`
> 节点类型对照见 `references/node-types.md`
> 功能块引脚见 `references/function-blocks.md`

---

## 生成步骤

### Step 1：解析逻辑，拆分梯级

每个独立的"从左母线到线圈"的逻辑单元是一个 segment。
- 多个输出线圈共享同一条能流路径 → 同一个 segment
- 逻辑上独立的控制回路 → 拆分为不同 segment

### Step 2：为每个节点生成唯一 ID

格式：`{nodeType}-{8位随机数}-{13位时间戳}`

示例：
- `contact-14645617-1782348599492`
- `FBD-compartment-CTU-90012318-1782348611830`
- `coil-57604879-1782352989213`

特殊固定节点：
- 左母线固定为 `"start-node-line"`
- 右母线（如有）固定为 `"end-node-line-{随机数}-{时间戳}"`
- ENO连接节点固定为 `"edit-node-rect"`

### Step 2.5：varName 与特殊属性规则

**必须有 `varName` 的节点类型**（触点、线圈、功能块）：
- `contact` / `negatedContact` / `risingContact` / `fallingContact`
- `coil` / `setCoil` / `resetCoil`
- `FBDCompartment`（varName 在 childrenNode 内，见 Step 2.6）

**不需要 `varName` 的节点**：`startLine` / `endLine` / `editRect`

`varName` 固定结构：
```json
"varName": {
  "name": "",
  "value": "变量名",
  "type": "BOOL",
  "scope": "VAR"
}
```

**`startLine` 必须包含 `Xlayer` 和 `Ylayer` 字段**，固定为 0：
```json
"start-node-line": {
  "id": "start-node-line",
  "type": "startLine",
  "Xlayer": 0,
  "Ylayer": 0,
  "sourceIds": [],
  "targetIds": ["第一个节点id"]
}
```

### Step 2.6：FBDCompartment 的 varName 位置（关键约束）

FBDCompartment 的 `varName` 必须放在 `childrenNode` 内部，FBDCompartment 外层绝对不能有 `varName`。

#### ❌ 错误写法（严禁，输出前必须检查）
```json
{
  "id": "FBD-compartment-CTU-xxx",
  "type": "FBDCompartment",
  "sourceIds": [...],
  "targetIds": [...],
  "varName": { "name": "", "value": "n", "type": "CTU", "scope": "VAR" },
  "childrenNode": {
    "type": "CTU",
    "isFunction": false,
    "portInputs": [...],
    "portOutputs": [...]
  }
}
```

#### ✅ 正确写法（必须严格遵守）
```json
{
  "id": "FBD-compartment-CTU-xxx",
  "type": "FBDCompartment",
  "sourceIds": [...],
  "targetIds": [...],
  "childrenNode": {
    "type": "CTU",
    "isFunction": false,
    "portInputs": [...],
    "portOutputs": [...],
    "varName": { "name": "", "value": "n", "type": "CTU", "scope": "VAR" }
  }
}
```

### Step 3：建立拓扑关系（sourceIds / targetIds）

**串联**：A → B → C
```
A.targetIds = [B.id]
B.sourceIds = [A.id]
B.targetIds = [C.id]
C.sourceIds = [B.id]
```

**并联（一分多）**：A 后分出 B、C 两支路
```
A.targetIds = [B.id, C.id]
B.sourceIds = [A.id]
C.sourceIds = [A.id]
```

**并联（多合一）**：B、C 汇合到 D
```
B.targetIds = [D.id]
C.targetIds = [D.id]
D.sourceIds = [B.id, C.id]
```

**功能块连接**：
- 触点 → FBDCompartment（EN得电）：触点.targetIds 包含 FBDCompartment.id
- FBDCompartment → 后续触点（ENO流出）：FBDCompartment.targetIds 包含下一触点.id
- 功能块引脚变量（CU/R/PV/Q 等）**不走拓扑连线**，只写在 portInputs/portOutputs 里

### Step 4：构造 editRect

每个 segment 必须有且仅有一个 `edit-node-rect`，位于最后一个触点和线圈之间：
```
最后触点.targetIds = ["edit-node-rect"]
edit-node-rect.sourceIds = [最后触点.id]
edit-node-rect.targetIds = [coil1.id, coil2.id, ...]
```

`edit-node-rect` 固定结构：
```json
{
  "id": "edit-node-rect",
  "type": "editRect",
  "sourceIds": ["..."],
  "targetIds": ["..."],
  "children": [
    {
      "id": "edit-node-rect-left-port",
      "type": "node:edgePort",
      "side": "left",
      "parentId": "edit-node-rect",
      "cssClasses": ["contact-left-port"],
      "position": {"x": -45, "y": 0},
      "size": {"width": 45, "height": 22}
    },
    {
      "id": "edit-node-rect-bottom-port",
      "type": "node:edgeBottomPort",
      "side": "bottom",
      "parentId": "edit-node-rect",
      "cssClasses": ["contact-bottom-port"],
      "position": {"x": 0, "y": 0},
      "size": {"width": 70, "height": 22}
    }
  ]
}
```

### Step 5：构造 variableList

收集所有节点中出现的变量，每个变量生成一条记录：

```json
{
  "scope": "VAR",
  "name": "变量名",
  "type": "BOOL",
  "initValue": "",
  "address": "",
  "comment": "",
  "pathLabels": ["base", "BOOL"],
  "id": "变量名大写",
  "isShow": true
}
```

**pathLabels 对照：**

| 变量类型 | pathLabels |
|---------|------------|
| BOOL | `["base", "BOOL"]` |
| INT  | `["base", "INT"]` |
| TIME | `["base", "TIME"]` |
| CTU  | `["Standard function blocks", "CTU"]` |
| CTD  | `["Standard function blocks", "CTD"]` |
| TON  | `["Standard function blocks", "TON"]` |
| TOF  | `["Standard function blocks", "TOF"]` |
| TP   | `["Standard function blocks", "TP"]` |
| SR   | `["Standard function blocks", "SR"]` |
| RS   | `["Standard function blocks", "RS"]` |

**id 字段规则**：变量名全部大写，例如 `name: "a5"` → `id: "A5"`，`name: "myVar"` → `id: "MYVAR"`

### Step 6：segment 尺寸

- `height` 和 `width` 根据复杂度估算，简单梯级填 `82`/`315`，复杂梯级填 `436`/`1430` 或更大
- `isExpand: true`（固定）
- `label: ""`，`note: ""`（固定为空）

---

## 输出前自检清单（每次生成后必须逐项核对）

- [ ] 顶层是 `[{ segmentList, variableList, pouType, pouName, extensionPath }]` 结构
- [ ] 每个 segment 的节点容器字段名是 `nodesObj`（对象），不是 `nodeDataArray`/`nodes` 等任何其他名称
- [ ] 每个 segment 有 `edgesObj: {}`
- [ ] `extensionPath` 固定为空字符串 `""`
- [ ] 每个 FBDCompartment 外层**没有** varName，varName **在** childrenNode 内
- [ ] 每个 port 条目**严格只有** name / value / scope / type 四个字段，无多余字段
- [ ] portInputs 第一项是 EN（scope: ""），portOutputs 第一项是 ENO（scope: ""）
- [ ] 所有触点、线圈、FBDCompartment 都有 varName
- [ ] startLine 有 Xlayer: 0 和 Ylayer: 0
- [ ] startLine / endLine / editRect 没有 varName
- [ ] variableList 包含所有出现过的变量，FB实例 type 填 FB 类型名

---

## 输出要求

1. **只输出 JSON**，不加任何解释文字（除非用户明确要求解释）
2. 顶层结构为 `[{ segmentList:[...], variableList:[...], pouType:"PROGRAM", pouName:"MAIN", extensionPath:"" }]`
3. JSON 必须合法，可直接解析
4. 变量命名遵循用户描述，用户未指定时使用语义化名称
5. 时间戳使用当前时间的毫秒值（13位），随机数使用8位数字
6. 如用户描述模糊，优先生成最简结构，不臆测未提及的逻辑

---

## 常见模式快速参考

| 用户说 | 对应结构 |
|--------|----------|
| "A 串联 B" | A.targetIds=[B.id], B.sourceIds=[A.id] |
| "A 并联 B" | 共同源节点.targetIds=[A.id,B.id]，A/B.targetIds=[汇合节点.id] |
| "常闭触点" | type: "negatedContact" |
| "上升沿" | type: "risingContact" |
| "下降沿" | type: "fallingContact" |
| "置位线圈" | type: "setCoil" |
| "复位线圈" | type: "resetCoil" |
| "计数器CTU" | type: "FBDCompartment", childrenNode.type: "CTU" |
| "定时器TON" | type: "FBDCompartment", childrenNode.type: "TON" |
