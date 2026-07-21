# 功能块（FBDCompartment）完整规范

## FBDCompartment 节点结构

### ❌ 错误写法（严禁）
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
> varName 出现在 FBDCompartment 外层 → 严禁

### ✅ 正确写法（必须严格遵守）
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
> varName 在 childrenNode 内部最后一个字段 → 正确

---

## portInputs / portOutputs 字段规则

### ❌ 错误写法（严禁）
```json
{"name": "CU", "value": "x", "type": "BOOL", "scope": "VAR_INPUT", "comment": "计数输入"}
```
> 出现了第5个字段 → 严禁，port 条目只能有4个字段

### ✅ 正确写法
```json
{"name": "CU", "value": "x", "scope": "VAR_INPUT", "type": "BOOL"}
```
> 严格只有 name / value / scope / type 四个字段

### scope 取值规则

| scope 值 | 适用引脚 |
|----------|---------|
| `""` | EN 和 ENO 固定用空字符串 |
| `"VAR_INPUT"` | 功能块输入引脚（除EN外） |
| `"VAR_OUTPUT"` | 功能块输出引脚（除ENO外） |

### portInputs / portOutputs 首位固定项

- **portInputs 第一个** 固定是 EN：
```json
{"name": "EN", "value": "", "scope": "", "type": ""}
```

- **portOutputs 第一个** 固定是 ENO：
```json
{"name": "ENO", "value": "", "scope": "", "type": ""}
```

---

## 各功能块引脚详细定义

### CTU（加计数器）

```json
"portInputs": [
  {"name": "EN",  "value": "",       "scope": "",           "type": ""},
  {"name": "CU",  "value": "变量名", "scope": "VAR_INPUT",  "type": "BOOL"},
  {"name": "R",   "value": "变量名", "scope": "VAR_INPUT",  "type": "BOOL"},
  {"name": "PV",  "value": "变量名", "scope": "VAR_INPUT",  "type": "INT"}
],
"portOutputs": [
  {"name": "ENO", "value": "",       "scope": "",           "type": ""},
  {"name": "Q",   "value": "变量名", "scope": "VAR_OUTPUT", "type": "BOOL"},
  {"name": "CV",  "value": "变量名", "scope": "VAR_OUTPUT", "type": "INT"}
],
"varName": {"name": "", "value": "实例名", "type": "CTU", "scope": "VAR"}
```

### CTD（减计数器）

```json
"portInputs": [
  {"name": "EN",  "value": "",       "scope": "",           "type": ""},
  {"name": "CD",  "value": "变量名", "scope": "VAR_INPUT",  "type": "BOOL"},
  {"name": "LD",  "value": "变量名", "scope": "VAR_INPUT",  "type": "BOOL"},
  {"name": "PV",  "value": "变量名", "scope": "VAR_INPUT",  "type": "INT"}
],
"portOutputs": [
  {"name": "ENO", "value": "",       "scope": "",           "type": ""},
  {"name": "Q",   "value": "变量名", "scope": "VAR_OUTPUT", "type": "BOOL"},
  {"name": "CV",  "value": "变量名", "scope": "VAR_OUTPUT", "type": "INT"}
],
"varName": {"name": "", "value": "实例名", "type": "CTD", "scope": "VAR"}
```

### TON（延时接通定时器）

```json
"portInputs": [
  {"name": "EN",  "value": "",       "scope": "",           "type": ""},
  {"name": "IN",  "value": "变量名", "scope": "VAR_INPUT",  "type": "BOOL"},
  {"name": "PT",  "value": "变量名", "scope": "VAR_INPUT",  "type": "TIME"}
],
"portOutputs": [
  {"name": "ENO", "value": "",       "scope": "",           "type": ""},
  {"name": "Q",   "value": "变量名", "scope": "VAR_OUTPUT", "type": "BOOL"},
  {"name": "ET",  "value": "变量名", "scope": "VAR_OUTPUT", "type": "TIME"}
],
"varName": {"name": "", "value": "实例名", "type": "TON", "scope": "VAR"}
```

### TOF（延时断开定时器）

```json
"portInputs": [
  {"name": "EN",  "value": "",       "scope": "",           "type": ""},
  {"name": "IN",  "value": "变量名", "scope": "VAR_INPUT",  "type": "BOOL"},
  {"name": "PT",  "value": "变量名", "scope": "VAR_INPUT",  "type": "TIME"}
],
"portOutputs": [
  {"name": "ENO", "value": "",       "scope": "",           "type": ""},
  {"name": "Q",   "value": "变量名", "scope": "VAR_OUTPUT", "type": "BOOL"},
  {"name": "ET",  "value": "变量名", "scope": "VAR_OUTPUT", "type": "TIME"}
],
"varName": {"name": "", "value": "实例名", "type": "TOF", "scope": "VAR"}
```

### TP（脉冲定时器）

```json
"portInputs": [
  {"name": "EN",  "value": "",       "scope": "",           "type": ""},
  {"name": "IN",  "value": "变量名", "scope": "VAR_INPUT",  "type": "BOOL"},
  {"name": "PT",  "value": "变量名", "scope": "VAR_INPUT",  "type": "TIME"}
],
"portOutputs": [
  {"name": "ENO", "value": "",       "scope": "",           "type": ""},
  {"name": "Q",   "value": "变量名", "scope": "VAR_OUTPUT", "type": "BOOL"},
  {"name": "ET",  "value": "变量名", "scope": "VAR_OUTPUT", "type": "TIME"}
],
"varName": {"name": "", "value": "实例名", "type": "TP", "scope": "VAR"}
```

### SR（置位优先双稳态）

```json
"portInputs": [
  {"name": "EN",  "value": "",       "scope": "",           "type": ""},
  {"name": "S1",  "value": "变量名", "scope": "VAR_INPUT",  "type": "BOOL"},
  {"name": "R",   "value": "变量名", "scope": "VAR_INPUT",  "type": "BOOL"}
],
"portOutputs": [
  {"name": "ENO", "value": "",       "scope": "",           "type": ""},
  {"name": "Q1",  "value": "变量名", "scope": "VAR_OUTPUT", "type": "BOOL"}
],
"varName": {"name": "", "value": "实例名", "type": "SR", "scope": "VAR"}
```

### RS（复位优先双稳态）

```json
"portInputs": [
  {"name": "EN",  "value": "",       "scope": "",           "type": ""},
  {"name": "S",   "value": "变量名", "scope": "VAR_INPUT",  "type": "BOOL"},
  {"name": "R1",  "value": "变量名", "scope": "VAR_INPUT",  "type": "BOOL"}
],
"portOutputs": [
  {"name": "ENO", "value": "",       "scope": "",           "type": ""},
  {"name": "Q1",  "value": "变量名", "scope": "VAR_OUTPUT", "type": "BOOL"}
],
"varName": {"name": "", "value": "实例名", "type": "RS", "scope": "VAR"}
```

---

## 功能块 ID 命名规则

```
FBD-compartment-{TYPE}-{8位随机数}-{13位时间戳}
```

示例：
- `FBD-compartment-CTU-90012318-1782348611830`
- `FBD-compartment-TON-45231876-1782348700123`
- `FBD-compartment-SR-54108979-1781743599081`
