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

- `portInputs` 第一项固定是 `EN`，`portOutputs` 第一项固定是 `ENO`；两者均为 `{"name":"EN/ENO","value":"","scope":"","type":""}`。
- 除 EN/ENO 外，端口名称、顺序、数量、库类型及边沿属性必须逐项取自 `runtime-library.md`。
- 每个端口对象严格只能有四个字段：`name`、`value`、`scope`、`type`。
- 非 EN 输入使用 `scope: "VAR_INPUT"`；非 ENO 输出使用 `scope: "VAR_OUTPUT"`。
- 库中的 `ANY`、`ANYNUM`、`ANYREAL`、`ANYINT`、`ANYBIT` 等泛型类型必须原样保留。
  JSON 中端口的 `type` 必须逐字使用 `runtime-library.md` 对该端口声明的原始类型。
  禁止根据业务场景、变量名称或连接变量的工程类型，将 `ANY`、`ANYNUM`、`ANYREAL`、
  `ANYINT`、`ANYBIT` 具体化或改写为 `REAL`、`INT`、`DINT`、`LREAL` 等类型。

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
- [ ] EN/ENO 后的全部端口名、顺序、数量、类型与库条目一致
- [ ] 功能块有且仅有 `childrenNode.varName`；函数完全没有 `varName`
- [ ] 每个 port 对象仅含四个规定字段
