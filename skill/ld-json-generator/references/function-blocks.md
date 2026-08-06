# FBDCompartment 渲染规范

> 本文件只定义 FBD JSON 的渲染格式、实例规则和端口对象格式。运行时库元件名称、类别、业务端口、数据类型、结构体成员、枚举值和派生类型定义，**唯一以** `references/runtime-library.md` **为准**。

## 职责边界

- `runtime-library.md`：查询 `function`、`functionBlock`、`struct`、`enum`、`derived` 的原始定义。
- 本文件：将库中的 `function` 或 `functionBlock` 映射为 `FBDCompartment` JSON 节点。
- 不得在本文件或生成逻辑中重新维护 CTU、TON、PID、SEL、转换函数等元件的端口表；示例只说明 JSON 形状，不能替代库查询。

## FBD 节点

所有可执行库元件在梯形图 JSON 中的外层节点都为 `"type": "FBDCompartment"`。外层不得存在 `varName`，实例名只能放入 `childrenNode.varName`。

```json
{
  "id": "FBD-compartment-TYPE-随机串-13位时间戳",
  "type": "FBDCompartment",
  "sourceIds": ["前置节点id"],
  "targetIds": ["后续节点id"],
  "childrenNode": {
    "type": "TYPE",
    "isFunction": false,
    "portInputs": [],
    "portOutputs": [],
    "varName": {"name": "", "value": "实例名", "type": "TYPE", "scope": "VAR"}
  }
}
```

## 函数与功能块

| 库 `type` | 节点 ID | `isFunction` | `varName` |
|---|---|---:|---|
| `function` | `FUN-compartment-{name}-{随机串}-{13位时间戳}` | `true` | 禁止，外层和 `childrenNode` 均不得有 |
| `functionBlock` | `FBD-compartment-{name}-{随机串}-{13位时间戳}` | `false` | 必须在 `childrenNode` 内；同时在 `variableList` 声明该实例 |

生成前必须在 `runtime-library.md` 找到同名条目。`childrenNode.type` 必须与库的原始 `name` 逐字符相同；不得把连写名称改成下划线形式，也不得按 IEC 习惯臆测端口。

函数格式示例：

```json
{
  "id": "FUN-compartment-库函数名-随机串-13位时间戳",
  "type": "FBDCompartment",
  "sourceIds": ["前置节点id"],
  "targetIds": ["后续节点id"],
  "childrenNode": {
    "type": "库函数名",
    "isFunction": true,
    "portInputs": [
      {"name":"EN","value":"","scope":"","type":""}
    ],
    "portOutputs": [
      {"name":"ENO","value":"","scope":"","type":""}
    ]
  }
}
```

## 端口规则

- `portInputs` 第一项固定是 `EN`，`portOutputs` 第一项固定是 `ENO`；两者的 `value`、`scope` 为空，`type` 可为空字符串，也可按真实前端导出格式省略。
- 除 EN/ENO 外，端口名称、顺序、数量、库类型及边沿属性必须逐项取自 `runtime-library.md`。
- 每个端口对象最多包含四个字段：`name`、`value`、`scope`、`type`。EN/ENO 的 `type` 可为空字符串，也可按真实前端导出格式省略。
- 普通非 EN 输入使用 `scope: "VAR_INPUT"`；普通非 ENO 输出使用 `scope: "VAR_OUTPUT"`。
- 库中的 `ANY`、`ANYNUM`、`ANYREAL`、`ANYINT`、`ANYBIT` 等泛型类型必须原样保留。
  JSON 中端口的 `type` 必须逐字使用 `runtime-library.md` 对该端口声明的原始类型。
  禁止根据业务场景、变量名称或连接变量的工程类型，将 `ANY`、`ANYNUM`、`ANYREAL`、
  `ANYINT`、`ANYBIT` 具体化或改写为 `REAL`、`INT`、`DINT`、`LREAL` 等类型。

### VAR_IN_OUT 归一化

`runtime-library.md` 分别列出源库的输入和输出。若同一 `function` 或
`functionBlock` 的输入、输出中存在**名称和类型完全相同**的端口，将这两个条目
视为同一个 `VAR_IN_OUT` 端口，并按以下前端格式生成：

- 只在 `childrenNode.portInputs` 中保留一次，位置沿用该端口在输入表中的顺序；
- 设置 `scope: "VAR_IN_OUT"`；
- 不得在 `childrenNode.portOutputs` 中再次生成该端口；
- `value` 使用同一个变量，且该变量只在 `variableList` 中声明一次；
- 该判断仅依据端口名称与类型的精确匹配，不得依据元件名称前缀或数据类型猜测；
- 名称相同但类型不同的端口不得合并，应视为库定义冲突。

例如 `MC_Power` 的库条目在输入和输出中都包含 `Axis: AXIS_REF`，对应 JSON
片段必须为：

```json
{
  "portInputs": [
    {"name":"EN","value":"","scope":"","type":""},
    {"name":"Axis","value":"Main_Axis","scope":"VAR_IN_OUT","type":"AXIS_REF"},
    {"name":"Enable","value":"Axis_Enable","scope":"VAR_INPUT","type":"BOOL"}
  ],
  "portOutputs": [
    {"name":"ENO","value":"","scope":"","type":""},
    {"name":"Status","value":"Axis_Powered","scope":"VAR_OUTPUT","type":"BOOL"}
  ]
}
```

示例只展示端口方向和对象形状；生成完整节点时，仍须按 `runtime-library.md`
补齐该元件的全部普通输入、普通输出，并保持各自原始顺序。

## 输出与实例

- FBD 输出端口写入的变量（例如库定义的 `Q`、`ET`、`CV`、`OUT`）不得再由 `coil`、`setCoil` 或 `resetCoil` 写入。
- 若梯级在 FBD 输出处结束，拓扑固定为 `FBDCompartment -> edit-node-rect -> endLine`。
- 功能块实例的 `varName.value`、端口变量和所有引用变量都必须在 `variableList` 中恰好声明一次；函数没有实例变量。

## 类型定义

`struct`、`enum`、`derived` 是库数据类型，不创建 `FBDCompartment`：

- `struct`：按库中“结构体成员”声明和访问，成员名、类型、默认值不可改写。
- `enum`：变量只能使用库列出的枚举成员。
- `derived`：按库中的基础类型与默认值声明。

## 生成前检查

- [ ] 每个 FBD 节点均能在 `runtime-library.md` 查到同名 `function` 或 `functionBlock`
- [ ] ID 前缀、`childrenNode.type`、`isFunction` 与库 `type` 一致
- [ ] 先完成 `VAR_IN_OUT` 归一化，再校验 EN/ENO 后的全部端口名、顺序、数量、scope 和类型
- [ ] 每个输入输出同名同类型端口只存在于 portInputs，scope 为 `VAR_IN_OUT`，portOutputs 中没有副本
- [ ] 功能块有且仅有 `childrenNode.varName`；函数完全没有 `varName`
- [ ] 每个 port 对象仅含四个规定字段
