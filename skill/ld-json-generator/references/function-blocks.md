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

---

## 功能块 ID 命名
```
FBD-compartment-{TYPE}-{8位随机数}-{13位时间戳}
```
