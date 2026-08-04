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
> FBD JSON 渲染规则见 `references/function-blocks.md`
> 运行时库索引（元件名称、类别、端口与数据类型）见 `references/runtime-library.md`
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
- 当前插入占位节点固定为 `"edit-node-rect"`，表示前端红色虚线框所在位置，不等同于 ENO 节点

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

### Step 2.6.5：运行时库查询（强制）

每次创建或声明运行时库元件前，必须先查询 `references/runtime-library.md`，它是库定义的唯一真源。

- 对 `function` 与 `functionBlock`：`childrenNode.type`、库 type、业务端口名称、顺序、数量、类型和边沿属性必须逐项匹配库条目。
- `function` 必须使用 `FUN-compartment-{name}-*` 与 `isFunction: true`，且不得有 `varName`。
- `functionBlock` 必须使用 `FBD-compartment-{name}-*` 与 `isFunction: false`，且必须在 `childrenNode.varName` 声明实例。
- 对 `struct`：按条目成员名、成员类型及默认值声明；对 `enum`：仅使用条目枚举成员；对 `derived`：按基础类型与默认值声明。三者均不是 FBD 节点。
- 不得按名称习惯改写库名（如自行添加或删除下划线），也不得按示例推断未查询的端口。

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

## Step 2.6.6 FBD 端口类型与变量类型强制规则

### 端口类型唯一来源

对于每个 FBDCompartment，必须在 runtime-library.md 中查找
childrenNode.type 对应函数或功能块的完整接口定义。

childrenNode.portInputs 与 childrenNode.portOutputs 中每个端口的：

- name
- 输入或输出方向
- type

必须严格、逐字匹配 runtime-library.md。

禁止根据业务场景、端口所连接的变量、变量名或推断出的工程量单位，
修改、具体化或替换 runtime-library.md 的端口 type。

### 泛型类型必须原样保留

运行库出现以下泛型类型时，JSON 中必须原样写入：

| runtime-library.md 类型 | JSON port.type 必须为 |
| ----------------------- | --------------------- |
| ANY                     | ANY                   |
| ANYNUM                  | ANYNUM                |
| ANYREAL                 | ANYREAL               |
| ANYINT                  | ANYINT                |
| ANYBIT                  | ANYBIT                |

禁止进行如下替换：

- ANY -> REAL
- ANY -> INT
- ANYNUM -> REAL
- ANYREAL -> LREAL
- ANYINT -> DINT

### variableList 自动创建规则

如果 port.value 引用的变量由本次 JSON 自动创建，则：

variableList 中该变量的 type 必须与该端口的 port.type 完全一致。

示例：

- SEL.IN0 的 port.type 为 ANY，则其自动创建变量的 type 也必须为 ANY
- LIMIT.OUT 的 port.type 为 ANY，则其自动创建变量的 type 也必须为 ANY
- PID.PV 的 port.type 为 REAL，则其自动创建变量的 type 也必须为 REAL
- TON.PT 的 port.type 为 TIME，则其自动创建变量的 type 也必须为 TIME

对于同一变量被多个端口引用的情况：

1. 所有引用端口的 type 必须完全一致；
2. variableList 中变量的 type 必须与该共同端口类型一致；
3. 如端口类型冲突，不得猜测或强制转换，必须拆分变量或使用运行库提供的显式类型转换函数。

### EN / ENO 规则

函数节点的 EN 和 ENO 也必须严格按运行库或既有编辑器导出格式生成。
若真实编辑器导出的 EN/ENO type 为空，则保持为空；
不得因为相邻控制信号是 BOOL 而擅自改为 BOOL。

### 生成后强制校验

输出 JSON 前，必须对每个 FBDCompartment 执行以下校验：

1. 在 runtime-library.md 中定位 childrenNode.type；
2. 校验 portInputs 与 portOutputs 的端口名称、顺序、方向、type；
3. 校验每个自动创建的 port.value 在 variableList 中存在；
4. 校验该自动创建变量的 variableList.type 等于 port.type；
5. 任一项失败时，JSON 不合格，必须修复后再输出。

不得以“业务变量实际应为 REAL”等理由，使泛型库端口或其自动创建变量偏离运行库定义。

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

### Step 3.5：强制拓扑完整性规则

**强制规则：禁止悬空节点。** 在同一个 segment 内，除左母线 `start-node-line` 外，所有节点（触点、线圈、FBDCompartment、editRect、endLine）都必须从 `start-node-line` 出发，经由 `targetIds` 路径可达。

- `start-node-line.sourceIds` 必须固定为 `[]`，且 `targetIds` 至少包含一个首节点 ID。
- 除 `start-node-line` 外，每个节点的 `sourceIds` 必须非空。
- 除末端线圈及 `endLine` 外，每个节点的 `targetIds` 必须非空。
- 所有连接必须双向一致：若 `A.targetIds` 包含 `B.id`，则 `B.sourceIds` 必须包含 `A.id`；反之亦然。
- 每个 segment 必须从 `start-node-line` 沿 `targetIds` 完成一次 BFS/DFS 遍历；`nodesObj` 中的全部节点 ID 都必须被遍历到。若存在未访问节点，即为悬空节点，必须修正后才能输出。
- 批量生成时，禁止仅按“已创建节点”判断正确；必须对生成完成的最终 `nodesObj` 执行一次独立遍历校验。

### Step 4：构造 editRect

`edit-node-rect` 是前端当前可编辑插入点，也就是红色虚线框对应的占位节点。它不是 IEC 语义节点，也不是固定 ENO 节点。

每个 segment 通常保留一个 `edit-node-rect`，位置由当前编辑点决定：

- 可以位于左母线后：`start-node-line -> edit-node-rect -> 后续节点`
- 可以位于普通节点之间：`前置节点 -> edit-node-rect -> 后续节点`
- 可以位于并联支路汇合处：多条支路末节点共同指向 `edit-node-rect`
- 可以位于最终输出前：`最后逻辑节点 -> edit-node-rect -> 线圈/endLine`

如果用户只是要求生成一张完整梯形图、没有指定当前编辑位置，则默认把 `edit-node-rect` 放在本 segment 最后逻辑节点与末端输出节点之间；但不要把它理解成永远只能在末尾。

- **串联回路的当前插入点在末端输出前**：`edit-node-rect.sourceIds` 仅包含主路径最后一个逻辑节点 id。
- **并联回路直接进入当前插入点**：`edit-node-rect.sourceIds` 必须包含每条并联支路末节点 id；每条支路末节点的 `targetIds` 都必须指向 `"edit-node-rect"`。
- **并联后继续串联，再进入当前插入点**：支路应先汇合到后续公共节点；`edit-node-rect.sourceIds` 只填写该公共节点 id，不能直接填写各支路末节点。
- **当前插入点位于左母线后**：`edit-node-rect.sourceIds = ["start-node-line"]`，`start-node-line.targetIds = ["edit-node-rect"]`。
- **当前插入点位于两个节点之间**：`edit-node-rect.sourceIds = [前置节点.id]`，`edit-node-rect.targetIds = [后续节点.id]`，并保持双向连接一致。

```text
串联：
Last_Node.targetIds = ["edit-node-rect"]
edit-node-rect.sourceIds = [Last_Node.id]

左母线后：
start-node-line.targetIds = ["edit-node-rect"]
edit-node-rect.sourceIds = ["start-node-line"]
edit-node-rect.targetIds = [Next_Node.id]
Next_Node.sourceIds = ["edit-node-rect"]

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
  "sourceIds": ["当前插入点左侧节点id；可为start-node-line、单个节点或多个并联支路末节点"],
  "targetIds": ["当前插入点右侧节点id；可为触点、功能块、线圈或endLine"],
  "children": [
    {
      "id": "edit-node-rect-left-port",
      "type": "node:edgePort",
      "side": "left",
      "parentId": "edit-node-rect",
      "cssClasses": ["contact-left-port"],
      "position": { "x": -45, "y": 0 },
      "size": { "width": 45, "height": 22 }
    },
    {
      "id": "edit-node-rect-bottom-port",
      "type": "node:edgeBottomPort",
      "side": "bottom",
      "parentId": "edit-node-rect",
      "cssClasses": ["contact-bottom-port"],
      "position": { "x": 0, "y": 0 },
      "size": { "width": 70, "height": 22 }
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

| 变量类型 | pathLabels                            |
| -------- | ------------------------------------- |
| BOOL     | `["base", "BOOL"]`                    |
| INT      | `["base", "INT"]`                     |
| TIME     | `["base", "TIME"]`                    |
| CTU      | `["Standard function blocks", "CTU"]` |
| CTD      | `["Standard function blocks", "CTD"]` |
| TON      | `["Standard function blocks", "TON"]` |
| TOF      | `["Standard function blocks", "TOF"]` |
| TP       | `["Standard function blocks", "TP"]`  |
| SR       | `["Standard function blocks", "SR"]`  |
| RS       | `["Standard function blocks", "RS"]`  |

**id 字段规则**：变量名全部大写，例如 `System_Run` → `SYSTEM_RUN`，`Ton_Cyl_A` → `TON_CYL_A`

### Step 6：变量命名规范（严格执行）

**统一使用 Pascal_Snake_Case**：每个单词首字母大写，单词间用下划线连接。

✅ 正确示例：`Start_Button`、`E_Stop`、`System_Run`、`Cylinder_A_Extend_Valve`、`Ton_Cyl_A_Timeout`
❌ 禁止：`start_button`（全小写）、`StartButton`（驼峰）、`startButton`（小驼峰）、混用风格

**各类型变量命名前缀规则：**

| 变量类别           | 前缀                                    | 示例                                        |
| ------------------ | --------------------------------------- | ------------------------------------------- |
| BOOL 输入信号      | 无前缀，语义词开头                      | `Start_Button`、`E_Stop`、`Inlet_Sensor`    |
| BOOL 内部状态/输出 | 无前缀，语义词开头                      | `System_Run`、`Cylinder_A_Extending`        |
| BOOL 物理阀/输出点 | 无前缀，`_Valve`/`_Motor`/`_Output`结尾 | `Cylinder_A_Extend_Valve`、`Conveyor_Motor` |
| TON 实例           | `Ton_`                                  | `Ton_Cyl_A_Timeout`、`Ton_Jam_Detect`       |
| TOF 实例           | `Tof_`                                  | `Tof_Conveyor_Delay`                        |
| TP 实例            | `Tp_`                                   | `Tp_Alarm_Pulse`                            |
| CTU 实例           | `Ctu_`                                  | `Ctu_Class_A`、`Ctu_Reject`                 |
| CTD 实例           | `Ctd_`                                  | `Ctd_Batch`                                 |
| SR 实例            | `Sr_`                                   | `Sr_Cyl_A`                                  |
| RS 实例            | `Rs_`                                   | `Rs_Alarm`                                  |
| TIME 设定值        | `Time_` + `_Set` 结尾                   | `Time_Cyl_Timeout_Set`、`Time_Jam_Set`      |
| TIME 当前值/输出   | `Time_` + `_Elapsed` 结尾               | `Time_Cyl_A_Elapsed`、`Time_Jam_Elapsed`    |
| INT 计数/数值      | `Int_`                                  | `Int_Class_A_Count`、`Int_Batch_Set`        |

### Step 7：segment 尺寸估算

| 并联支路数  | 串联节点数   | height   | width     |
| ----------- | ------------ | -------- | --------- |
| 0（纯串联） | 1-3          | 82       | 400~600   |
| 0（纯串联） | 4-6          | 82       | 700~1000  |
| 2路并联     | 每路1-2节点  | 218      | 600~900   |
| 3路并联     | 每路1-2节点  | 300      | 800~1100  |
| 4路以上并联 | 任意         | 436~538  | 1200~2000 |
| 含功能块    | 在以上基础上 | +100~150 | +200~400  |

---

## 输出前自检清单（每次生成后必须逐项核对）

- [ ] 顶层是 `[{ segmentList, variableList, pouType, pouName, extensionPath }]` 结构
- [ ] `extensionPath` 固定为空字符串 `""`
- [ ] 每个 segment 必须同时包含 `id` 与 `isExpand`：`id` 格式固定为 `segment-{8位随机数}-{13位时间戳}`，且所有 segment 的 id 全局唯一；`isExpand` 必须存在且固定为布尔值 `true`（不得省略、不得写成字符串 `"true"`）
- [ ] 每个 segment 的 `label` 已填写中文功能描述，不为空
- [ ] `note` 字段：无特殊工艺说明时为空，有关键互锁/时序假设时填写
- [ ] 节点容器字段名是 `nodesObj`（对象），不是 `nodeDataArray` 或其他
- [ ] 每个 segment 有 `edgesObj: {}`
- [ ] `editRect.sourceIds` / `targetIds` 体现当前红色虚线框的真实位置：左母线后、节点之间、并联汇合处、末端输出前都允许；并联后有公共节点时仅使用公共节点，不直接填写各支路末节点
- [ ] **连通性检查**：对每个 segment 从 `start-node-line` 沿 `targetIds` 执行 BFS/DFS；`nodesObj` 中所有节点均被访问到，不存在悬空节点
- [ ] `start-node-line.sourceIds` 固定为 `[]`，且其 `targetIds` 非空；除此以外所有节点的 `sourceIds` 均非空
- [ ] 除线圈和 `endLine` 外，所有节点的 `targetIds` 均非空
- [ ] 双向连接一致：每一条 `A.targetIds -> B.id` 均能在 `B.sourceIds` 中找到 `A.id`，反向关系也完全一致
- [ ] 若 segment 以功能块输出结束，拓扑必须为 `FBDCompartment -> edit-node-rect -> endLine`
- [ ] 功能块 portOutputs 中的 Q、ET、CV、Q1 等变量没有被 coil、setCoil 或 resetCoil 重复写入
- [ ] 每个 FBDCompartment 外层**没有** varName，varName **在** childrenNode 内
- [ ] 每个 port 条目最多包含 name / value / scope / type 四个字段；EN/ENO 的 type 可为空字符串，也可按真实导出格式省略
- [ ] portInputs 第一项是 EN（scope: ""），portOutputs 第一项是 ENO（scope: ""）
- [ ] 所有触点、线圈、FBDCompartment 都有 varName
- [ ] startLine 有 Xlayer: 0 和 Ylayer: 0，无 varName
- [ ] startLine / endLine / editRect 没有 varName
- [ ] 同一变量在同一梯级多次出现时，每次使用不同节点 id
- [ ] variableList 中同名变量只出现一次
- [ ] **变量引用与声明一致性检查**：收集所有 segment 内触点、线圈、FBDCompartment 的 `varName.value`，以及所有功能块 `portInputs` / `portOutputs`（排除 EN、ENO）的 `value`，得到引用变量集合 `UsedVars`；收集 `variableList[*].name` 得到声明变量集合 `DeclaredVars`。必须满足 `UsedVars == DeclaredVars`：`UsedVars - DeclaredVars` 与 `DeclaredVars - UsedVars` 均必须为空。
- [ ] 所有变量引用必须与 `variableList[*].name` **逐字符完全一致**，包括大小写、下划线、单词顺序及全部词段；不允许模糊匹配、自动补全或名称近似视为同一变量。
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

| 用户说                | 对应结构                                                 |
| --------------------- | -------------------------------------------------------- |
| "A 串联 B"            | A.targetIds=[B.id], B.sourceIds=[A.id]                   |
| "从左母线并联A、B、C" | startLine.targetIds=[A,B,C]，三者targetIds均指向汇合节点 |
| "A 并联 B 后串 C"     | 源节点.targetIds=[A,B], A/B.targetIds=[C.id]             |
| "常闭触点"            | type: "negatedContact"                                   |
| "上升沿"              | type: "risingContact"                                    |
| "下降沿"              | type: "fallingContact"                                   |
| "置位线圈"            | type: "setCoil"                                          |
| "复位线圈"            | type: "resetCoil"                                        |
| "启动自保持"          | 见 references/patterns.md → 模式1                        |
| "气缸前进/缩回"       | 见 references/patterns.md → 模式2                        |
| "故障报警"            | 见 references/patterns.md → 模式3                        |
| "计数器CTU"           | type: "FBDCompartment", childrenNode.type: "CTU"         |
| "定时器TON"           | type: "FBDCompartment", childrenNode.type: "TON"         |

---

## 运行时库优先级（覆盖同名旧规则）

`references/runtime-library.md` 是元件定义的唯一真源，优先级高于本 Skill 内的示例、常用元件清单、端口样例和 `function-blocks.md` 的示例。若任何旧示例与运行时库冲突，必须以运行时库为准。

- 运行时库定义只查询 `references/runtime-library.md`；不得自行推断或改写库名称、端口及数据类型。
- 本 Skill 中的 CTU、TON、ABS、GT、PID、类型转换等文字或 JSON 均仅为渲染格式示例，不构成完整端口定义。
- 使用未在示例列出的库函数、功能块或数据类型时同样允许，但必须先查运行时库并遵守其原始定义。

输出前额外核验：

- [ ] 每个使用的运行时元件均在 `runtime-library.md` 中找到，且名称逐字符一致。
- [ ] 业务端口、实例规则、库 type、ID 前缀和 `isFunction` 全部与库条目一致。
- [ ] `struct` 成员、`enum` 值、`derived` 基础类型/默认值均从库文件获取，且未被建模为 FBD 节点。
