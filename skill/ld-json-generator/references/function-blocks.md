# 功能块（FBDCompartment）完整规范

## FBDCompartment 节点结构

### ❌ 错误写法（严禁）
```json
{
  "id": "FBD-compartment-CTU-xxx",
  "type": "FBDCompartment",
  "varName": { ... },
  "childrenNode": { "type": "CTU", ... }
}
```
> varName 在外层 → 严禁

### ✅ 正确写法
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
    "varName": { "name": "", "value": "Ctu_Class_A", "type": "CTU", "scope": "VAR" }
  }
}
```


## 函数节点的渲染器格式（强制）

函数不能实例化。函数的外层节点仍为 `"type": "FBDCompartment"`，但节点 id 必须是 `FUN-compartment-{FUNCTION}-{随机串}-{13位时间戳}`；例如：`FUN-compartment-SEL-W42NCi-1785289130639`、`FUN-compartment-GT-VStfPf-1785289136383`。

```json
{
  "id": "FUN-compartment-GT-VStfPf-1785289136383",
  "type": "FBDCompartment",
  "sourceIds": ["FUN-compartment-SEL-W42NCi-1785289130639"],
  "targetIds": ["edit-node-rect"],
  "childrenNode": {
    "type": "GT",
    "isFunction": true,
    "portInputs": [
      {"name":"EN","value":"","scope":"","type":""},
      {"name":"IN1","value":"e","scope":"VAR_INPUT","type":"ANY"},
      {"name":"IN2","value":"f","scope":"VAR_INPUT","type":"ANY"}
    ],
    "portOutputs": [
      {"name":"ENO","value":"","scope":"","type":""},
      {"name":"OUT","value":"g","scope":"VAR_OUTPUT","type":"BOOL"}
    ]
  }
}
```

函数的 `childrenNode` 内**绝不能**有 `varName`；因此画面只显示 `GT`、`SEL`、`ABS` 等函数名，不显示任何实例名。只有有状态功能块使用 `FBD-compartment-` ID 和 `childrenNode.varName`。

## 函数与功能块区分

运行时库中的 `type` 用于区分函数和功能块；但在梯形图 JSON 中，两者的外层节点 `type` **一律**为 `FBDCompartment`。

| 运行时库类别 | JSON 外层 `type` | `childrenNode.isFunction` | 示例 |
|---|---|---:|---|
| `functionBlock` | `FBDCompartment` | `false` | TON、TOF、TP、CTU、CTD、SR、RS |
| `function` | `FBDCompartment` | `true` | ABS、SUB、ADD、MUL、DIV、GT、GE、EQ、LT、LE、NE |

函数型节点完整结构示例（GT）：

```json
{
  "id": "FUN-compartment-GT-xxxxxxxx-xxxxxxxxxxxxx",
  "type": "FBDCompartment",
  "sourceIds": ["前置节点id"],
  "targetIds": ["后续节点id"],
  "childrenNode": {
    "type": "GT",
    "isFunction": true,
    "portInputs": [
      {"name": "EN", "value": "", "scope": "", "type": ""},
      {"name": "IN1", "value": "Real_Sync_Deviation", "scope": "VAR_INPUT", "type": "REAL"},
      {"name": "IN2", "value": "Real_Sync_Deviation_Limit", "scope": "VAR_INPUT", "type": "REAL"}
    ],
    "portOutputs": [
      {"name": "ENO", "value": "", "scope": "", "type": ""},
      {"name": "OUT", "value": "Sync_Deviation_Exceeded", "scope": "VAR_OUTPUT", "type": "BOOL"}
    ],
    "varName": {"name": "", "value": "Gt_Sync_Deviation", "type": "GT", "scope": "VAR"}
  }
}
```

- 功能块外层不得出现 `varName`，其实例 `varName` 必须置于 `childrenNode` 内。
- **函数不可实例化**：函数外层和 `childrenNode` 内均不得出现 `varName`，也不得在 `variableList` 中声明函数实例变量。
- `childrenNode.type` 必须使用运行时库中的准确元件名。
- EN / ENO 以外的业务端口名称、数量、顺序和类型必须严格匹配 `data.json` 的对应条目。


---

## portInputs / portOutputs 字段规则

每个 port 条目**严格只有 4 个字段**：`name` / `value` / `scope` / `type`

### ❌ 错误（第5个字段）
```json
{"name": "CU", "value": "x", "type": "BOOL", "scope": "VAR_INPUT", "comment": "..."}
```

### ✅ 正确
```json
{"name": "CU", "value": "Sort_A_Trigger", "scope": "VAR_INPUT", "type": "BOOL"}
```

### scope 规则
| scope | 适用 |
|-------|------|
| `""` | EN 和 ENO |
| `"VAR_INPUT"` | 除EN外的输入引脚 |
| `"VAR_OUTPUT"` | 除ENO外的输出引脚 |

### 首位固定项
```json
// portInputs 第一个
{"name": "EN",  "value": "", "scope": "", "type": ""}
// portOutputs 第一个
{"name": "ENO", "value": "", "scope": "", "type": ""}
```

---

## 各功能块引脚定义

### CTU（加计数器）
> CU 引脚建议接上升沿中间变量，避免一次动作重复计数

```json
"portInputs": [
  {"name": "EN",  "value": "",                    "scope": "",           "type": ""},
  {"name": "CU",  "value": "Sort_A_Trigger",       "scope": "VAR_INPUT",  "type": "BOOL"},
  {"name": "R",   "value": "Counter_Reset",         "scope": "VAR_INPUT",  "type": "BOOL"},
  {"name": "PV",  "value": "Int_Class_A_Batch_Set", "scope": "VAR_INPUT",  "type": "INT"}
],
"portOutputs": [
  {"name": "ENO", "value": "",                    "scope": "",           "type": ""},
  {"name": "Q",   "value": "Class_A_Count_Done",   "scope": "VAR_OUTPUT", "type": "BOOL"},
  {"name": "CV",  "value": "Int_Class_A_Count",     "scope": "VAR_OUTPUT", "type": "INT"}
],
"varName": {"name": "", "value": "Ctu_Class_A", "type": "CTU", "scope": "VAR"}
```

### CTD（减计数器）
```json
"portInputs": [
  {"name": "EN",  "value": "", "scope": "", "type": ""},
  {"name": "CD",  "value": "变量名", "scope": "VAR_INPUT",  "type": "BOOL"},
  {"name": "LD",  "value": "变量名", "scope": "VAR_INPUT",  "type": "BOOL"},
  {"name": "PV",  "value": "变量名", "scope": "VAR_INPUT",  "type": "INT"}
],
"portOutputs": [
  {"name": "ENO", "value": "", "scope": "", "type": ""},
  {"name": "Q",   "value": "变量名", "scope": "VAR_OUTPUT", "type": "BOOL"},
  {"name": "CV",  "value": "变量名", "scope": "VAR_OUTPUT", "type": "INT"}
],
"varName": {"name": "", "value": "Ctd_实例名", "type": "CTD", "scope": "VAR"}
```

### TON（延时接通定时器）
```json
"portInputs": [
  {"name": "EN",  "value": "", "scope": "", "type": ""},
  {"name": "IN",  "value": "变量名",                   "scope": "VAR_INPUT",  "type": "BOOL"},
  {"name": "PT",  "value": "Time_Xxx_Set",              "scope": "VAR_INPUT",  "type": "TIME"}
],
"portOutputs": [
  {"name": "ENO", "value": "", "scope": "", "type": ""},
  {"name": "Q",   "value": "变量名",                   "scope": "VAR_OUTPUT", "type": "BOOL"},
  {"name": "ET",  "value": "Time_Xxx_Elapsed",          "scope": "VAR_OUTPUT", "type": "TIME"}
],
"varName": {"name": "", "value": "Ton_实例名", "type": "TON", "scope": "VAR"}
```

### TOF（延时断开定时器）
```json
"portInputs": [
  {"name": "EN",  "value": "", "scope": "", "type": ""},
  {"name": "IN",  "value": "变量名",          "scope": "VAR_INPUT",  "type": "BOOL"},
  {"name": "PT",  "value": "Time_Xxx_Set",    "scope": "VAR_INPUT",  "type": "TIME"}
],
"portOutputs": [
  {"name": "ENO", "value": "", "scope": "", "type": ""},
  {"name": "Q",   "value": "变量名",          "scope": "VAR_OUTPUT", "type": "BOOL"},
  {"name": "ET",  "value": "Time_Xxx_Elapsed","scope": "VAR_OUTPUT", "type": "TIME"}
],
"varName": {"name": "", "value": "Tof_实例名", "type": "TOF", "scope": "VAR"}
```

### TP（脉冲定时器）
```json
"portInputs": [
  {"name": "EN",  "value": "", "scope": "", "type": ""},
  {"name": "IN",  "value": "变量名",          "scope": "VAR_INPUT",  "type": "BOOL"},
  {"name": "PT",  "value": "Time_Xxx_Set",    "scope": "VAR_INPUT",  "type": "TIME"}
],
"portOutputs": [
  {"name": "ENO", "value": "", "scope": "", "type": ""},
  {"name": "Q",   "value": "变量名",          "scope": "VAR_OUTPUT", "type": "BOOL"},
  {"name": "ET",  "value": "Time_Xxx_Elapsed","scope": "VAR_OUTPUT", "type": "TIME"}
],
"varName": {"name": "", "value": "Tp_实例名", "type": "TP", "scope": "VAR"}
```

### SR（置位优先双稳态）
```json
"portInputs": [
  {"name": "EN",  "value": "", "scope": "", "type": ""},
  {"name": "S1",  "value": "变量名", "scope": "VAR_INPUT",  "type": "BOOL"},
  {"name": "R",   "value": "变量名", "scope": "VAR_INPUT",  "type": "BOOL"}
],
"portOutputs": [
  {"name": "ENO", "value": "", "scope": "", "type": ""},
  {"name": "Q1",  "value": "变量名", "scope": "VAR_OUTPUT", "type": "BOOL"}
],
"varName": {"name": "", "value": "Sr_实例名", "type": "SR", "scope": "VAR"}
```

### RS（复位优先双稳态）
```json
"portInputs": [
  {"name": "EN",  "value": "", "scope": "", "type": ""},
  {"name": "S",   "value": "变量名", "scope": "VAR_INPUT",  "type": "BOOL"},
  {"name": "R1",  "value": "变量名", "scope": "VAR_INPUT",  "type": "BOOL"}
],
"portOutputs": [
  {"name": "ENO", "value": "", "scope": "", "type": ""},
  {"name": "Q1",  "value": "变量名", "scope": "VAR_OUTPUT", "type": "BOOL"}
],
"varName": {"name": "", "value": "Rs_实例名", "type": "RS", "scope": "VAR"}
```


## 数值与比较函数引脚定义

以下运行时元件类别为 `function`，因此 `childrenNode.isFunction` 必须为 `true`；外层 `type` 仍为 `FBDCompartment`。

### ABS（绝对值）

业务端口：`IN: ANY_NUM -> OUT: ANY_NUM`。

```json
"type": "ABS",
"isFunction": true,
"portInputs": [
  {"name": "EN", "value": "", "scope": "", "type": ""},
  {"name": "IN", "value": "Real_Sync_Difference", "scope": "VAR_INPUT", "type": "REAL"}
],
"portOutputs": [
  {"name": "ENO", "value": "", "scope": "", "type": ""},
  {"name": "OUT", "value": "Real_Sync_Deviation", "scope": "VAR_OUTPUT", "type": "REAL"}
],
```

### SUB（减法）

业务端口：`IN1: ANY_NUM, IN2: ANY_NUM -> OUT: ANY_NUM`。

```json
"type": "SUB",
"isFunction": true,
"portInputs": [
  {"name": "EN", "value": "", "scope": "", "type": ""},
  {"name": "IN1", "value": "Real_Cylinder_A_Position", "scope": "VAR_INPUT", "type": "REAL"},
  {"name": "IN2", "value": "Real_Cylinder_B_Position", "scope": "VAR_INPUT", "type": "REAL"}
],
"portOutputs": [
  {"name": "ENO", "value": "", "scope": "", "type": ""},
  {"name": "OUT", "value": "Real_Sync_Difference", "scope": "VAR_OUTPUT", "type": "REAL"}
],
```

### GT / GE / EQ / LT / LE / NE（比较）

业务端口：`IN1: ANY, IN2: ANY -> OUT: BOOL`。比较结果端口名固定为 `OUT`，不得写成 `Q`。

```json
"type": "GT",
"isFunction": true,
"portInputs": [
  {"name": "EN", "value": "", "scope": "", "type": ""},
  {"name": "IN1", "value": "Real_Sync_Deviation", "scope": "VAR_INPUT", "type": "REAL"},
  {"name": "IN2", "value": "Real_Sync_Deviation_Limit", "scope": "VAR_INPUT", "type": "REAL"}
],
"portOutputs": [
  {"name": "ENO", "value": "", "scope": "", "type": ""},
  {"name": "OUT", "value": "Sync_Deviation_Exceeded", "scope": "VAR_OUTPUT", "type": "BOOL"}
],
```

### 函数无实例约束

- `ABS`、`SUB`、`ADD`、`MUL`、`DIV`、`GT`、`GE`、`EQ`、`LT`、`LE`、`NE` 都是 IEC 61131-3 函数，不保存内部状态，不得命名或实例化。
- 图形块标题只能显示函数类型，例如 `GT`；函数输入、输出通过 port 的 `value` 变量连接。

### 函数输出约束

- `ABS`、`SUB` 的输入和 OUT 必须使用一致的实际数值类型，例如均为 `REAL`。
- 比较函数的 IN1 与 IN2 必须类型兼容，OUT 必须为 `BOOL`。
- Q、ET、CV、Q1 与函数 OUT 均由 FBDCompartment 直接写入；严禁再用 `coil`、`setCoil` 或 `resetCoil` 写入同名变量。


---

## 功能块 ID 命名
```
功能块：FBD-compartment-{TYPE}-{随机串}-{13位时间戳}
函数：FUN-compartment-{TYPE}-{随机串}-{13位时间戳}
```
