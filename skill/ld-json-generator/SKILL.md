---
name: ld-json-generator
description: >
  生成 IEC 61131-3 梯形图（Ladder Diagram）专用 JSON 格式。当用户用自然语言描述梯形图逻辑时，
  直接输出可供前端渲染器使用的完整 JSON 结构，包含 segmentList、variableList 等所有字段。
  触发场景：用户描述"梯形图"、"LD程序"、"PLC逻辑"、"触点线圈"、"功能块"、"CTU/CTD/TON/TOF/TP/SR/RS"
  等关键词，或要求"生成JSON"、"转成JSON"、"写成梯形图格式"时，必须使用本 Skill。
  即使用户只是说"帮我写一段XX逻辑的梯形图"，也应使用本 Skill 输出 JSON。
  严格禁止：FBDCompartment 外层出现 varName；port 条目字段数超过4个；
  节点容器字段名写成 nodeDataArray 或其他任何名称而非 nodesObj；
  变量命名混用风格（必须统一 Pascal_Snake_Case）。
---

# IEC 61131-3 梯形图 JSON 生成器

## 目标
将用户的自然语言梯形图描述转换为标准 JSON 格式，该格式可直接被前端梯形图渲染器使用。

## 输出结构总览

```json
[{
  "segmentList": [ ...segment列表... ],
  "variableList": [ ...变量列表... ],
  "pouType": "PROGRAM",
  "pouName": "用户指定名称，未指定时默认 MAIN",
  "extensionPath": ""
}]
```

**严禁输出**：`nodeDataArray` / `nodes` / `nodeList` 等字段名，节点容器固定为 `nodesObj`

> 详细字段规范见 `references/schema.md`
> 节点类型对照见 `references/node-types.md`
> 功能块引脚见 `references/function-blocks.md`
> 业务模式见 `references/patterns.md`

---

## 生成步骤

### Step 1：解析逻辑，拆分梯级

每个独立的"从左母线到线圈"的逻辑单元是一个 segment。
- 多个输出线圈共享同一条能流路径 → 同一个 segment
- 逻辑上独立的控制回路 → 拆分为不同 segment
- **每个 segment 的 `label` 字段必须填写中文功能描述**，例如"系统启动自保持"、"气缸A伸出控制"，不能留空
- **`note` 字段**：默认为空字符串；当存在关键安全互锁、时序假设、故障复位前提或用户显式说明的工艺条件时，填写中文简述，例如"急停为硬件常闭，断线即停"、"需确认气缸缩回到位后方可置位伸出"

### Step 2：为每个节点生成唯一 ID

格式：`{nodeType}-{8位随机数}-{13位时间戳}`

示例：
- `contact-14645617-1782348599492`
- `negatedContact-78431259-1784698860002`
- `FBD-compartment-CTU-90012318-1782348611830`
- `coil-57604879-1782352989213`
- `setCoil-98470127-1784698860001`
- `resetCoil-75222252-1784698860011`

特殊固定节点：
- 左母线固定为 `"start-node-line"`
- 右母线（如有）固定为 `"end-node-line-{随机数}-{时间戳}"`
- ENO连接节点固定为 `"edit-node-rect"`

⚠️ **同一变量在同一梯级中多次出现（如并联支路中重复使用），每次必须生成不同的节点 id，绝对不能复用同一个节点 id。**

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
  "targetIds": ["第一个节点id或多个并联节点id"]
}
```

### Step 2.6：FBDCompartment 的 varName 位置（关键约束）

FBDCompartment 的 `varName` 必须放在 `childrenNode` 内部，FBDCompartment 外层绝对不能有 `varName`。

#### ❌ 错误写法（严禁）
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

#### ✅ 正确写法
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
B.sourceIds = [A.id], B.targetIds = [C.id]
C.sourceIds = [B.id]
```

**并联从左母线直接分叉**（最常见）：startLine 后直接分出 A、B、C 三路汇合到 D
```
startLine.targetIds = [A.id, B.id, C.id]
A.sourceIds = ["start-node-line"], A.targetIds = [D.id]
B.sourceIds = ["start-node-line"], B.targetIds = [D.id]
C.sourceIds = ["start-node-line"], C.targetIds = [D.id]
D.sourceIds = [A.id, B.id, C.id]
```

**并联从中间节点分叉**：A 后分出 B、C 再汇合到 D
```
A.targetIds = [B.id, C.id]
B.sourceIds = [A.id], B.targetIds = [D.id]
C.sourceIds = [A.id], C.targetIds = [D.id]
D.sourceIds = [B.id, C.id]
```

**功能块连接**：
- 触点 → FBDCompartment：触点.targetIds 包含 FBDCompartment.id
- FBDCompartment → 后续节点：FBDCompartment.targetIds 包含下一节点.id
- 功能块引脚变量不走拓扑连线，只写在 portInputs/portOutputs 里

### Step 4：构造 editRect

每个 segment 必须有且仅有一个 `edit-node-rect`，位于最后一个触点/功能块与末端输出节点之间；末端输出节点可以是线圈或 endLine。

- **串联回路**：`edit-node-rect.sourceIds` 仅包含主路径最后一个节点的 id。
- **并联回路**：`edit-node-rect.sourceIds` 必须包含每条并联支路末节点的 id；每条支路末节点的 `targetIds` 都必须指向 `"edit-node-rect"`。
- **并联后继续串联**：支路应先汇合到后续公共节点；`edit-node-rect.sourceIds` 只填写该公共节点的 id，不能直接填写各支路末节点。

```text
串联：
Last_Node.targetIds = ["edit-node-rect"]
edit-node-rect.sourceIds = [Last_Node.id]

并联后直接接线圈：
Branch_A_Last.targetIds = ["edit-node-rect"]
Branch_B_Last.targetIds = ["edit-node-rect"]
edit-node-rect.sourceIds = [Branch_A_Last.id, Branch_B_Last.id]

并联后串联 C：
Branch_A_Last.targetIds = [C.id]
Branch_B_Last.targetIds = [C.id]
C.sourceIds = [Branch_A_Last.id, Branch_B_Last.id]
C.targetIds = ["edit-node-rect"]
edit-node-rect.sourceIds = [C.id]
```

`edit-node-rect` 固定结构：
```json
{
  "id": "edit-node-rect",
  "type": "editRect",
  "sourceIds": ["最后节点id或各并联支路末节点id"],
  "targetIds": ["coil1.id", "coil2.id"],
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


### Step 4.5：功能块输出与 endLine

功能块 `portOutputs` 中的 Q、ET、CV、Q1 等变量由功能块直接写入。

- 严禁在同一或其他梯级中，用 `coil`、`setCoil` 或 `resetCoil`
  写入同一个功能块输出变量。
- 若一个 segment 以 FBDCompartment 的输出结束，且不需要额外输出线圈，
  拓扑必须为：`FBDCompartment -> edit-node-rect -> endLine`。
- FBDCompartment.targetIds 必须为 `["edit-node-rect"]`。
- edit-node-rect.sourceIds 必须为 `[FBDCompartment.id]`。
- edit-node-rect.targetIds 必须为 `[endLine.id]`。
- endLine.sourceIds 必须为 `["edit-node-rect"]`，endLine.targetIds 固定为 `[]`。
- endLine 不带 `varName`，id 格式为
  `"end-node-line-{8位随机数}-{13位时间戳}"`。
- 后续梯级通过触点读取功能块输出变量，例如
  `Action_Timeout(NO)`、`Class_A_Count_Done(NO)`。


### Step 5：构造 variableList

收集所有节点中出现的变量，每个变量只记录一次：

```json
{
  "scope": "VAR",
  "name": "变量名",
  "type": "BOOL",
  "initValue": "",
  "address": "",
  "comment": "中文说明",
  "pathLabels": ["base", "BOOL"],
  "id": "变量名全大写",
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

**id 字段规则**：变量名全部大写，例如 `System_Run` → `SYSTEM_RUN`，`Ton_Cyl_A` → `TON_CYL_A`

### Step 6：变量命名规范（严格执行）

**统一使用 Pascal_Snake_Case**：每个单词首字母大写，单词间用下划线连接。

✅ 正确示例：`Start_Button`、`E_Stop`、`System_Run`、`Cylinder_A_Extend_Valve`、`Ton_Cyl_A_Timeout`
❌ 禁止：`start_button`（全小写）、`StartButton`（驼峰）、`startButton`（小驼峰）、混用风格

**各类型变量命名前缀规则：**

| 变量类别 | 前缀 | 示例 |
|---------|------|------|
| BOOL 输入信号 | 无前缀，语义词开头 | `Start_Button`、`E_Stop`、`Inlet_Sensor` |
| BOOL 内部状态/输出 | 无前缀，语义词开头 | `System_Run`、`Cylinder_A_Extending` |
| BOOL 物理阀/输出点 | 无前缀，`_Valve`/`_Motor`/`_Output`结尾 | `Cylinder_A_Extend_Valve`、`Conveyor_Motor` |
| TON 实例 | `Ton_` | `Ton_Cyl_A_Timeout`、`Ton_Jam_Detect` |
| TOF 实例 | `Tof_` | `Tof_Conveyor_Delay` |
| TP 实例 | `Tp_` | `Tp_Alarm_Pulse` |
| CTU 实例 | `Ctu_` | `Ctu_Class_A`、`Ctu_Reject` |
| CTD 实例 | `Ctd_` | `Ctd_Batch` |
| SR 实例 | `Sr_` | `Sr_Cyl_A` |
| RS 实例 | `Rs_` | `Rs_Alarm` |
| TIME 设定值 | `Time_` + `_Set` 结尾 | `Time_Cyl_Timeout_Set`、`Time_Jam_Set` |
| TIME 当前值/输出 | `Time_` + `_Elapsed` 结尾 | `Time_Cyl_A_Elapsed`、`Time_Jam_Elapsed` |
| INT 计数/数值 | `Int_` | `Int_Class_A_Count`、`Int_Batch_Set` |

### Step 7：segment 尺寸估算

| 并联支路数 | 串联节点数 | height | width |
|-----------|-----------|--------|-------|
| 0（纯串联） | 1-3 | 82 | 400~600 |
| 0（纯串联） | 4-6 | 82 | 700~1000 |
| 2路并联 | 每路1-2节点 | 218 | 600~900 |
| 3路并联 | 每路1-2节点 | 300 | 800~1100 |
| 4路以上并联 | 任意 | 436~538 | 1200~2000 |
| 含功能块 | 在以上基础上 | +100~150 | +200~400 |

---

## 输出前自检清单（每次生成后必须逐项核对）

- [ ] 顶层是 `[{ segmentList, variableList, pouType, pouName, extensionPath }]` 结构
- [ ] `extensionPath` 固定为空字符串 `""`
- [ ] 每个 segment 必须同时包含 `id` 与 `isExpand`：`id` 格式固定为 `segment-{8位随机数}-{13位时间戳}`，且所有 segment 的 id 全局唯一；`isExpand` 必须存在且固定为布尔值 `true`（不得省略、不得写成字符串 `"true"`）
- [ ] 每个 segment 的 `label` 已填写中文功能描述，不为空
- [ ] `note` 字段：无特殊工艺说明时为空，有关键互锁/时序假设时填写
- [ ] 节点容器字段名是 `nodesObj`（对象），不是 `nodeDataArray` 或其他
- [ ] 每个 segment 有 `edgesObj: {}`
- [ ] `editRect.sourceIds`：串联时为最后节点；并联直连输出时包含全部支路末节点；并联后有公共节点时仅为公共节点
- [ ] 若 segment 以功能块输出结束，拓扑必须为 `FBDCompartment -> edit-node-rect -> endLine`
- [ ] 功能块 portOutputs 中的 Q、ET、CV、Q1 等变量没有被 coil、setCoil 或 resetCoil 重复写入
- [ ] 每个 FBDCompartment 外层**没有** varName，varName **在** childrenNode 内
- [ ] 每个 port 条目**严格只有** name / value / scope / type 四个字段
- [ ] portInputs 第一项是 EN（scope: ""），portOutputs 第一项是 ENO（scope: ""）
- [ ] 所有触点、线圈、FBDCompartment 都有 varName
- [ ] startLine 有 Xlayer: 0 和 Ylayer: 0，无 varName
- [ ] startLine / endLine / editRect 没有 varName
- [ ] 同一变量在同一梯级多次出现时，每次使用不同节点 id
- [ ] variableList 中同名变量只出现一次
- [ ] 所有变量命名统一为 Pascal_Snake_Case，无混用
- [ ] 若逻辑包含双线圈气缸，伸出/缩回电磁阀梯级必须互相串联对方常闭触点
- [ ] 故障报警：setCoil(Fault) 锁存，单独梯级 Fault 常开驱动 coil(Alarm)

---

## 输出要求

1. **只输出 JSON**，不加任何解释文字（除非用户明确要求解释）
2. 顶层结构为 `[{ segmentList:[...], variableList:[...], pouType:"PROGRAM", pouName:"MAIN", extensionPath:"" }]`
3. JSON 必须合法，可直接解析
4. 变量命名遵循用户描述，用户未指定时使用语义化 Pascal_Snake_Case 命名
5. 时间戳使用当前时间毫秒值（13位），随机数使用8位数字
6. 如用户描述模糊，优先生成最简结构，不臆测未提及的逻辑

---

## 常见模式快速参考

| 用户说 | 对应结构 |
|--------|----------|
| "A 串联 B" | A.targetIds=[B.id], B.sourceIds=[A.id] |
| "从左母线并联A、B、C" | startLine.targetIds=[A,B,C]，三者targetIds均指向汇合节点 |
| "A 并联 B 后串 C" | 源节点.targetIds=[A,B], A/B.targetIds=[C.id] |
| "常闭触点" | type: "negatedContact" |
| "上升沿" | type: "risingContact" |
| "下降沿" | type: "fallingContact" |
| "置位线圈" | type: "setCoil" |
| "复位线圈" | type: "resetCoil" |
| "启动自保持" | 见 references/patterns.md → 模式1 |
| "气缸前进/缩回" | 见 references/patterns.md → 模式2 |
| "故障报警" | 见 references/patterns.md → 模式3 |
| "计数器CTU" | type: "FBDCompartment", childrenNode.type: "CTU" |
| "定时器TON" | type: "FBDCompartment", childrenNode.type: "TON" |
