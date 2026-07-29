# Runtime Library Reference

> 来源：`data.json`。用于梯形图/FBD 生成时查询库元件的原始名称、类别和定义。

> **强制规则：** `childrenNode.type`、函数 ID 的 `FUN-compartment-{name}-*` 类型段、端口名、端口顺序、端口类型及 `isFunction`，均以本文件为准；禁止自行改写库名称。

## 库 type 含义

| 库 type | 含义 | 在 FBD/变量中的使用 |
|---|---|---|
| `function` | 无内部状态的运算或转换函数，输入确定则输出确定。 | 使用 `FUN-compartment-{name}-*`，`isFunction: true`，不得有 `varName` 或函数实例变量。 |
| `functionBlock` | 有内部状态或执行上下文的功能块，例如计时、计数、触发、PID、运动控制。 | 使用 `FBD-compartment-{name}-*`，`isFunction: false`，必须在 `childrenNode.varName` 中声明实例。 |
| `struct` | 由多个有名称、类型及可选默认值的**结构体成员/字段**组成的复合数据类型。 | 可声明为变量类型，并通过 `实例名.成员名` 访问；此处不作为普通 FBD 节点。 |
| `enum` | 取值限定为预定义枚举成员的类型。 | 可声明为变量类型；变量值仅应使用条目列出的枚举成员。 |
| `derived` | 基于一个基础类型定义的别名，可带默认值。 | 可声明为变量类型；其底层存储类型和默认值按本条目。 |

## 字段说明

- **输入/输出**：`端口名: 类型`；`[rising]` 表示库定义的上升沿输入。
- **可扩展**：仅在 `true` 时显示，表示可追加同类输入；未显示即不可扩展。
- **筛选器**：仅保留库的非空类型约束。
- **结构体成员**：保留成员名、类型、默认值与非空说明。

## Standard function blocks

### `SR`
- 库类型：`functionBlock`
- 输入：`S1: BOOL`，`R: BOOL`
- 输出：`Q1: BOOL`
- 说明：The SR bistable is a latch where the Set dominates.

### `RS`
- 库类型：`functionBlock`
- 输入：`S: BOOL`，`R1: BOOL`
- 输出：`Q1: BOOL`
- 说明：The RS bistable is a latch where the Reset dominates.

### `SEMA`
- 库类型：`functionBlock`
- 输入：`CLAIM: BOOL`，`RELEASE: BOOL`
- 输出：`BUSY: BOOL`
- 说明：The semaphore provides a mechanism to allow software elements mutually exclusive access to certain resources.

### `R_TRIG`
- 库类型：`functionBlock`
- 输入：`CLK: BOOL`
- 输出：`Q: BOOL`
- 说明：The output produces a single pulse when a rising edge is detected.

### `F_TRIG`
- 库类型：`functionBlock`
- 输入：`CLK: BOOL`
- 输出：`Q: BOOL`
- 说明：The output produces a single pulse when a falling edge is detected.

### `CTU`
- 库类型：`functionBlock`
- 输入：`CU: BOOL` [rising]，`R: BOOL`，`PV: INT`
- 输出：`Q: BOOL`，`CV: INT`
- 说明：The up-counter can be used to signal when a count has reached a maximum value.

### `CTU_DINT`
- 库类型：`functionBlock`
- 输入：`CU: BOOL` [rising]，`R: BOOL`，`PV: DINT`
- 输出：`Q: BOOL`，`CV: DINT`
- 说明：The up-counter can be used to signal when a count has reached a maximum value.

### `CTU_LINT`
- 库类型：`functionBlock`
- 输入：`CU: BOOL` [rising]，`R: BOOL`，`PV: LINT`
- 输出：`Q: BOOL`，`CV: LINT`
- 说明：The up-counter can be used to signal when a count has reached a maximum value.

### `CTU_UDINT`
- 库类型：`functionBlock`
- 输入：`CU: BOOL` [rising]，`R: BOOL`，`PV: UDINT`
- 输出：`Q: BOOL`，`CV: UDINT`
- 说明：The up-counter can be used to signal when a count has reached a maximum value.

### `CTU_ULINT`
- 库类型：`functionBlock`
- 输入：`CU: BOOL` [rising]，`R: BOOL`，`PV: ULINT`
- 输出：`Q: BOOL`，`CV: ULINT`
- 说明：The up-counter can be used to signal when a count has reached a maximum value.

### `CTD`
- 库类型：`functionBlock`
- 输入：`CD: BOOL` [rising]，`LD: BOOL`，`PV: INT`
- 输出：`Q: BOOL`，`CV: INT`
- 说明：The down-counter can be used to signal when a count has reached zero, on counting down from a preset value.

### `CTD_DINT`
- 库类型：`functionBlock`
- 输入：`CD: BOOL` [rising]，`LD: BOOL`，`PV: DINT`
- 输出：`Q: BOOL`，`CV: DINT`
- 说明：The down-counter can be used to signal when a count has reached zero, on counting down from a preset value.

### `CTD_LINT`
- 库类型：`functionBlock`
- 输入：`CD: BOOL` [rising]，`LD: BOOL`，`PV: LINT`
- 输出：`Q: BOOL`，`CV: LINT`
- 说明：The down-counter can be used to signal when a count has reached zero, on counting down from a preset value.

### `CTD_UDINT`
- 库类型：`functionBlock`
- 输入：`CD: BOOL` [rising]，`LD: BOOL`，`PV: UDINT`
- 输出：`Q: BOOL`，`CV: UDINT`
- 说明：The down-counter can be used to signal when a count has reached zero, on counting down from a preset value.

### `CTD_ULINT`
- 库类型：`functionBlock`
- 输入：`CD: BOOL` [rising]，`LD: BOOL`，`PV: ULINT`
- 输出：`Q: BOOL`，`CV: ULINT`
- 说明：The down-counter can be used to signal when a count has reached zero, on counting down from a preset value.

### `CTUD`
- 库类型：`functionBlock`
- 输入：`CU: BOOL` [rising]，`CD: BOOL` [rising]，`R: BOOL`，`LD: BOOL`，`PV: INT`
- 输出：`QU: BOOL`，`QD: BOOL`，`CV: INT`，`CD_T: R_TRIG`，`CU_T: R_TRIG`
- 说明：The up-down counter has two inputs CU and CD. It can be used to both count up on one input and down on the other.

### `CTUD_DINT`
- 库类型：`functionBlock`
- 输入：`CU: BOOL` [rising]，`CD: BOOL` [rising]，`R: BOOL`，`LD: BOOL`，`PV: DINT`
- 输出：`QU: BOOL`，`QD: BOOL`，`CV: DINT`，`CD_T: R_TRIG`，`CU_T: R_TRIG`
- 说明：The up-down counter has two inputs CU and CD. It can be used to both count up on one input and down on the other.

### `CTUD_LINT`
- 库类型：`functionBlock`
- 输入：`CU: BOOL` [rising]，`CD: BOOL` [rising]，`R: BOOL`，`LD: BOOL`，`PV: LINT`
- 输出：`QU: BOOL`，`QD: BOOL`，`CV: LINT`，`CD_T: R_TRIG`，`CU_T: R_TRIG`
- 说明：The up-down counter has two inputs CU and CD. It can be used to both count up on one input and down on the other.

### `CTUD_UDINT`
- 库类型：`functionBlock`
- 输入：`CU: BOOL` [rising]，`CD: BOOL` [rising]，`R: BOOL`，`LD: BOOL`，`PV: UDINT`
- 输出：`QU: BOOL`，`QD: BOOL`，`CV: UDINT`，`CD_T: R_TRIG`，`CU_T: R_TRIG`
- 说明：The up-down counter has two inputs CU and CD. It can be used to both count up on one input and down on the other.

### `CTUD_ULINT`
- 库类型：`functionBlock`
- 输入：`CU: BOOL` [rising]，`CD: BOOL` [rising]，`R: BOOL`，`LD: BOOL`，`PV: ULINT`
- 输出：`QU: BOOL`，`QD: BOOL`，`CV: ULINT`，`CD_T: R_TRIG`，`CU_T: R_TRIG`
- 说明：The up-down counter has two inputs CU and CD. It can be used to both count up on one input and down on the other.

### `TP`
- 库类型：`functionBlock`
- 输入：`IN: BOOL`，`PT: TIME`
- 输出：`Q: BOOL`，`ET: TIME`
- 说明：The pulse timer can be used to generate output pulses of a given time duration.

### `TON`
- 库类型：`functionBlock`
- 输入：`IN: BOOL`，`PT: TIME`
- 输出：`Q: BOOL`，`ET: TIME`
- 说明：The on-delay timer can be used to delay setting an output true, for fixed period after an input becomes true.

### `TOF`
- 库类型：`functionBlock`
- 输入：`IN: BOOL`，`PT: TIME`
- 输出：`Q: BOOL`，`ET: TIME`
- 说明：The off-delay timer can be used to delay setting an output false, for fixed period after input goes false.

## Additional function blocks

### `RTC`
- 库类型：`functionBlock`
- 输入：`IN: BOOL`，`PDT: DT`
- 输出：`Q: BOOL`，`CDT: DT`
- 说明：The real time clock has many uses including time stamping, setting dates and times of day in batch reports, in alarm messages and so on.

### `INTEGRAL`
- 库类型：`functionBlock`
- 输入：`RUN: BOOL`，`R1: BOOL`，`XIN: REAL`，`X0: REAL`，`CYCLE: TIME`
- 输出：`Q: BOOL`，`XOUT: REAL`
- 说明：The integral function block integrates the value of input XIN over time.

### `DERIVATIVE`
- 库类型：`functionBlock`
- 输入：`RUN: BOOL`，`XIN: REAL`，`CYCLE: TIME`
- 输出：`XOUT: REAL`
- 说明：The derivative function block produces an output XOUT proportional to the rate of change of the input XIN.

### `PID`
- 库类型：`functionBlock`
- 输入：`AUTO: BOOL`，`PV: REAL`，`SP: REAL`，`X0: REAL`，`KP: REAL`，`TR: REAL`，`TD: REAL`，`CYCLE: TIME`
- 输出：`XOUT: REAL`
- 说明：The PID (proportional, Integral, Derivative) function block provides the classical three term controller for closed loop control.

### `RAMP`
- 库类型：`functionBlock`
- 输入：`RUN: BOOL`，`X0: REAL`，`X1: REAL`，`TR: TIME`，`CYCLE: TIME`
- 输出：`BUSY: BOOL`，`XOUT: REAL`
- 说明：The RAMP function block is modelled on example given in the standard.

### `HYSTERESIS`
- 库类型：`functionBlock`
- 输入：`XIN1: REAL`，`XIN2: REAL`，`EPS: REAL`
- 输出：`Q: BOOL`
- 说明：The hysteresis function block provides a hysteresis boolean output driven by the difference of two floating point (REAL) inputs XIN1 and XIN2.

## Type conversion

> 本分类均为数据类型转换函数：将输入 `IN` 转换为输出 `OUT`。以下仅保留原始名称、源/目标类型与类型筛选器。

### `BOOL_TO_SINT`
- 库类型：`function`
- 输入：`IN: BOOL`
- 输出：`OUT: SINT`
- 筛选器：`ANY_TO_ANY`

### `BOOL_TO_INT`
- 库类型：`function`
- 输入：`IN: BOOL`
- 输出：`OUT: INT`
- 筛选器：`ANY_TO_ANY`

### `BOOL_TO_DINT`
- 库类型：`function`
- 输入：`IN: BOOL`
- 输出：`OUT: DINT`
- 筛选器：`ANY_TO_ANY`

### `BOOL_TO_LINT`
- 库类型：`function`
- 输入：`IN: BOOL`
- 输出：`OUT: LINT`
- 筛选器：`ANY_TO_ANY`

### `BOOL_TO_USINT`
- 库类型：`function`
- 输入：`IN: BOOL`
- 输出：`OUT: USINT`
- 筛选器：`ANY_TO_ANY`

### `BOOL_TO_UINT`
- 库类型：`function`
- 输入：`IN: BOOL`
- 输出：`OUT: UINT`
- 筛选器：`ANY_TO_ANY`

### `BOOL_TO_UDINT`
- 库类型：`function`
- 输入：`IN: BOOL`
- 输出：`OUT: UDINT`
- 筛选器：`ANY_TO_ANY`

### `BOOL_TO_ULINT`
- 库类型：`function`
- 输入：`IN: BOOL`
- 输出：`OUT: ULINT`
- 筛选器：`ANY_TO_ANY`

### `BOOL_TO_REAL`
- 库类型：`function`
- 输入：`IN: BOOL`
- 输出：`OUT: REAL`
- 筛选器：`ANY_TO_ANY`

### `BOOL_TO_LREAL`
- 库类型：`function`
- 输入：`IN: BOOL`
- 输出：`OUT: LREAL`
- 筛选器：`ANY_TO_ANY`

### `BOOL_TO_TIME`
- 库类型：`function`
- 输入：`IN: BOOL`
- 输出：`OUT: TIME`
- 筛选器：`ANY_TO_ANY`

### `BOOL_TO_DATE`
- 库类型：`function`
- 输入：`IN: BOOL`
- 输出：`OUT: DATE`
- 筛选器：`ANY_TO_ANY`

### `BOOL_TO_TOD`
- 库类型：`function`
- 输入：`IN: BOOL`
- 输出：`OUT: TOD`
- 筛选器：`ANY_TO_ANY`

### `BOOL_TO_DT`
- 库类型：`function`
- 输入：`IN: BOOL`
- 输出：`OUT: DT`
- 筛选器：`ANY_TO_ANY`

### `BOOL_TO_STRING`
- 库类型：`function`
- 输入：`IN: BOOL`
- 输出：`OUT: STRING`
- 筛选器：`ANY_TO_ANY`

### `BOOL_TO_BYTE`
- 库类型：`function`
- 输入：`IN: BOOL`
- 输出：`OUT: BYTE`
- 筛选器：`ANY_TO_ANY`

### `BOOL_TO_WORD`
- 库类型：`function`
- 输入：`IN: BOOL`
- 输出：`OUT: WORD`
- 筛选器：`ANY_TO_ANY`

### `BOOL_TO_DWORD`
- 库类型：`function`
- 输入：`IN: BOOL`
- 输出：`OUT: DWORD`
- 筛选器：`ANY_TO_ANY`

### `BOOL_TO_LWORD`
- 库类型：`function`
- 输入：`IN: BOOL`
- 输出：`OUT: LWORD`
- 筛选器：`ANY_TO_ANY`

### `SINT_TO_BOOL`
- 库类型：`function`
- 输入：`IN: SINT`
- 输出：`OUT: BOOL`
- 筛选器：`ANY_TO_ANY`

### `SINT_TO_INT`
- 库类型：`function`
- 输入：`IN: SINT`
- 输出：`OUT: INT`
- 筛选器：`ANY_TO_ANY`

### `SINT_TO_DINT`
- 库类型：`function`
- 输入：`IN: SINT`
- 输出：`OUT: DINT`
- 筛选器：`ANY_TO_ANY`

### `SINT_TO_LINT`
- 库类型：`function`
- 输入：`IN: SINT`
- 输出：`OUT: LINT`
- 筛选器：`ANY_TO_ANY`

### `SINT_TO_USINT`
- 库类型：`function`
- 输入：`IN: SINT`
- 输出：`OUT: USINT`
- 筛选器：`ANY_TO_ANY`

### `SINT_TO_UINT`
- 库类型：`function`
- 输入：`IN: SINT`
- 输出：`OUT: UINT`
- 筛选器：`ANY_TO_ANY`

### `SINT_TO_UDINT`
- 库类型：`function`
- 输入：`IN: SINT`
- 输出：`OUT: UDINT`
- 筛选器：`ANY_TO_ANY`

### `SINT_TO_ULINT`
- 库类型：`function`
- 输入：`IN: SINT`
- 输出：`OUT: ULINT`
- 筛选器：`ANY_TO_ANY`

### `SINT_TO_REAL`
- 库类型：`function`
- 输入：`IN: SINT`
- 输出：`OUT: REAL`
- 筛选器：`ANY_TO_ANY`

### `SINT_TO_LREAL`
- 库类型：`function`
- 输入：`IN: SINT`
- 输出：`OUT: LREAL`
- 筛选器：`ANY_TO_ANY`

### `SINT_TO_TIME`
- 库类型：`function`
- 输入：`IN: SINT`
- 输出：`OUT: TIME`
- 筛选器：`ANY_TO_ANY`

### `SINT_TO_DATE`
- 库类型：`function`
- 输入：`IN: SINT`
- 输出：`OUT: DATE`
- 筛选器：`ANY_TO_ANY`

### `SINT_TO_TOD`
- 库类型：`function`
- 输入：`IN: SINT`
- 输出：`OUT: TOD`
- 筛选器：`ANY_TO_ANY`

### `SINT_TO_DT`
- 库类型：`function`
- 输入：`IN: SINT`
- 输出：`OUT: DT`
- 筛选器：`ANY_TO_ANY`

### `SINT_TO_STRING`
- 库类型：`function`
- 输入：`IN: SINT`
- 输出：`OUT: STRING`
- 筛选器：`ANY_TO_ANY`

### `SINT_TO_BYTE`
- 库类型：`function`
- 输入：`IN: SINT`
- 输出：`OUT: BYTE`
- 筛选器：`ANY_TO_ANY`

### `SINT_TO_WORD`
- 库类型：`function`
- 输入：`IN: SINT`
- 输出：`OUT: WORD`
- 筛选器：`ANY_TO_ANY`

### `SINT_TO_DWORD`
- 库类型：`function`
- 输入：`IN: SINT`
- 输出：`OUT: DWORD`
- 筛选器：`ANY_TO_ANY`

### `SINT_TO_LWORD`
- 库类型：`function`
- 输入：`IN: SINT`
- 输出：`OUT: LWORD`
- 筛选器：`ANY_TO_ANY`

### `INT_TO_BOOL`
- 库类型：`function`
- 输入：`IN: INT`
- 输出：`OUT: BOOL`
- 筛选器：`ANY_TO_ANY`

### `INT_TO_SINT`
- 库类型：`function`
- 输入：`IN: INT`
- 输出：`OUT: SINT`
- 筛选器：`ANY_TO_ANY`

### `INT_TO_DINT`
- 库类型：`function`
- 输入：`IN: INT`
- 输出：`OUT: DINT`
- 筛选器：`ANY_TO_ANY`

### `INT_TO_LINT`
- 库类型：`function`
- 输入：`IN: INT`
- 输出：`OUT: LINT`
- 筛选器：`ANY_TO_ANY`

### `INT_TO_USINT`
- 库类型：`function`
- 输入：`IN: INT`
- 输出：`OUT: USINT`
- 筛选器：`ANY_TO_ANY`

### `INT_TO_UINT`
- 库类型：`function`
- 输入：`IN: INT`
- 输出：`OUT: UINT`
- 筛选器：`ANY_TO_ANY`

### `INT_TO_UDINT`
- 库类型：`function`
- 输入：`IN: INT`
- 输出：`OUT: UDINT`
- 筛选器：`ANY_TO_ANY`

### `INT_TO_ULINT`
- 库类型：`function`
- 输入：`IN: INT`
- 输出：`OUT: ULINT`
- 筛选器：`ANY_TO_ANY`

### `INT_TO_REAL`
- 库类型：`function`
- 输入：`IN: INT`
- 输出：`OUT: REAL`
- 筛选器：`ANY_TO_ANY`

### `INT_TO_LREAL`
- 库类型：`function`
- 输入：`IN: INT`
- 输出：`OUT: LREAL`
- 筛选器：`ANY_TO_ANY`

### `INT_TO_TIME`
- 库类型：`function`
- 输入：`IN: INT`
- 输出：`OUT: TIME`
- 筛选器：`ANY_TO_ANY`

### `INT_TO_DATE`
- 库类型：`function`
- 输入：`IN: INT`
- 输出：`OUT: DATE`
- 筛选器：`ANY_TO_ANY`

### `INT_TO_TOD`
- 库类型：`function`
- 输入：`IN: INT`
- 输出：`OUT: TOD`
- 筛选器：`ANY_TO_ANY`

### `INT_TO_DT`
- 库类型：`function`
- 输入：`IN: INT`
- 输出：`OUT: DT`
- 筛选器：`ANY_TO_ANY`

### `INT_TO_STRING`
- 库类型：`function`
- 输入：`IN: INT`
- 输出：`OUT: STRING`
- 筛选器：`ANY_TO_ANY`

### `INT_TO_BYTE`
- 库类型：`function`
- 输入：`IN: INT`
- 输出：`OUT: BYTE`
- 筛选器：`ANY_TO_ANY`

### `INT_TO_WORD`
- 库类型：`function`
- 输入：`IN: INT`
- 输出：`OUT: WORD`
- 筛选器：`ANY_TO_ANY`

### `INT_TO_DWORD`
- 库类型：`function`
- 输入：`IN: INT`
- 输出：`OUT: DWORD`
- 筛选器：`ANY_TO_ANY`

### `INT_TO_LWORD`
- 库类型：`function`
- 输入：`IN: INT`
- 输出：`OUT: LWORD`
- 筛选器：`ANY_TO_ANY`

### `DINT_TO_BOOL`
- 库类型：`function`
- 输入：`IN: DINT`
- 输出：`OUT: BOOL`
- 筛选器：`ANY_TO_ANY`

### `DINT_TO_SINT`
- 库类型：`function`
- 输入：`IN: DINT`
- 输出：`OUT: SINT`
- 筛选器：`ANY_TO_ANY`

### `DINT_TO_INT`
- 库类型：`function`
- 输入：`IN: DINT`
- 输出：`OUT: INT`
- 筛选器：`ANY_TO_ANY`

### `DINT_TO_LINT`
- 库类型：`function`
- 输入：`IN: DINT`
- 输出：`OUT: LINT`
- 筛选器：`ANY_TO_ANY`

### `DINT_TO_USINT`
- 库类型：`function`
- 输入：`IN: DINT`
- 输出：`OUT: USINT`
- 筛选器：`ANY_TO_ANY`

### `DINT_TO_UINT`
- 库类型：`function`
- 输入：`IN: DINT`
- 输出：`OUT: UINT`
- 筛选器：`ANY_TO_ANY`

### `DINT_TO_UDINT`
- 库类型：`function`
- 输入：`IN: DINT`
- 输出：`OUT: UDINT`
- 筛选器：`ANY_TO_ANY`

### `DINT_TO_ULINT`
- 库类型：`function`
- 输入：`IN: DINT`
- 输出：`OUT: ULINT`
- 筛选器：`ANY_TO_ANY`

### `DINT_TO_REAL`
- 库类型：`function`
- 输入：`IN: DINT`
- 输出：`OUT: REAL`
- 筛选器：`ANY_TO_ANY`

### `DINT_TO_LREAL`
- 库类型：`function`
- 输入：`IN: DINT`
- 输出：`OUT: LREAL`
- 筛选器：`ANY_TO_ANY`

### `DINT_TO_TIME`
- 库类型：`function`
- 输入：`IN: DINT`
- 输出：`OUT: TIME`
- 筛选器：`ANY_TO_ANY`

### `DINT_TO_DATE`
- 库类型：`function`
- 输入：`IN: DINT`
- 输出：`OUT: DATE`
- 筛选器：`ANY_TO_ANY`

### `DINT_TO_TOD`
- 库类型：`function`
- 输入：`IN: DINT`
- 输出：`OUT: TOD`
- 筛选器：`ANY_TO_ANY`

### `DINT_TO_DT`
- 库类型：`function`
- 输入：`IN: DINT`
- 输出：`OUT: DT`
- 筛选器：`ANY_TO_ANY`

### `DINT_TO_STRING`
- 库类型：`function`
- 输入：`IN: DINT`
- 输出：`OUT: STRING`
- 筛选器：`ANY_TO_ANY`

### `DINT_TO_BYTE`
- 库类型：`function`
- 输入：`IN: DINT`
- 输出：`OUT: BYTE`
- 筛选器：`ANY_TO_ANY`

### `DINT_TO_WORD`
- 库类型：`function`
- 输入：`IN: DINT`
- 输出：`OUT: WORD`
- 筛选器：`ANY_TO_ANY`

### `DINT_TO_DWORD`
- 库类型：`function`
- 输入：`IN: DINT`
- 输出：`OUT: DWORD`
- 筛选器：`ANY_TO_ANY`

### `DINT_TO_LWORD`
- 库类型：`function`
- 输入：`IN: DINT`
- 输出：`OUT: LWORD`
- 筛选器：`ANY_TO_ANY`

### `LINT_TO_BOOL`
- 库类型：`function`
- 输入：`IN: LINT`
- 输出：`OUT: BOOL`
- 筛选器：`ANY_TO_ANY`

### `LINT_TO_SINT`
- 库类型：`function`
- 输入：`IN: LINT`
- 输出：`OUT: SINT`
- 筛选器：`ANY_TO_ANY`

### `LINT_TO_INT`
- 库类型：`function`
- 输入：`IN: LINT`
- 输出：`OUT: INT`
- 筛选器：`ANY_TO_ANY`

### `LINT_TO_DINT`
- 库类型：`function`
- 输入：`IN: LINT`
- 输出：`OUT: DINT`
- 筛选器：`ANY_TO_ANY`

### `LINT_TO_USINT`
- 库类型：`function`
- 输入：`IN: LINT`
- 输出：`OUT: USINT`
- 筛选器：`ANY_TO_ANY`

### `LINT_TO_UINT`
- 库类型：`function`
- 输入：`IN: LINT`
- 输出：`OUT: UINT`
- 筛选器：`ANY_TO_ANY`

### `LINT_TO_UDINT`
- 库类型：`function`
- 输入：`IN: LINT`
- 输出：`OUT: UDINT`
- 筛选器：`ANY_TO_ANY`

### `LINT_TO_ULINT`
- 库类型：`function`
- 输入：`IN: LINT`
- 输出：`OUT: ULINT`
- 筛选器：`ANY_TO_ANY`

### `LINT_TO_REAL`
- 库类型：`function`
- 输入：`IN: LINT`
- 输出：`OUT: REAL`
- 筛选器：`ANY_TO_ANY`

### `LINT_TO_LREAL`
- 库类型：`function`
- 输入：`IN: LINT`
- 输出：`OUT: LREAL`
- 筛选器：`ANY_TO_ANY`

### `LINT_TO_TIME`
- 库类型：`function`
- 输入：`IN: LINT`
- 输出：`OUT: TIME`
- 筛选器：`ANY_TO_ANY`

### `LINT_TO_DATE`
- 库类型：`function`
- 输入：`IN: LINT`
- 输出：`OUT: DATE`
- 筛选器：`ANY_TO_ANY`

### `LINT_TO_TOD`
- 库类型：`function`
- 输入：`IN: LINT`
- 输出：`OUT: TOD`
- 筛选器：`ANY_TO_ANY`

### `LINT_TO_DT`
- 库类型：`function`
- 输入：`IN: LINT`
- 输出：`OUT: DT`
- 筛选器：`ANY_TO_ANY`

### `LINT_TO_STRING`
- 库类型：`function`
- 输入：`IN: LINT`
- 输出：`OUT: STRING`
- 筛选器：`ANY_TO_ANY`

### `LINT_TO_BYTE`
- 库类型：`function`
- 输入：`IN: LINT`
- 输出：`OUT: BYTE`
- 筛选器：`ANY_TO_ANY`

### `LINT_TO_WORD`
- 库类型：`function`
- 输入：`IN: LINT`
- 输出：`OUT: WORD`
- 筛选器：`ANY_TO_ANY`

### `LINT_TO_DWORD`
- 库类型：`function`
- 输入：`IN: LINT`
- 输出：`OUT: DWORD`
- 筛选器：`ANY_TO_ANY`

### `LINT_TO_LWORD`
- 库类型：`function`
- 输入：`IN: LINT`
- 输出：`OUT: LWORD`
- 筛选器：`ANY_TO_ANY`

### `USINT_TO_BOOL`
- 库类型：`function`
- 输入：`IN: USINT`
- 输出：`OUT: BOOL`
- 筛选器：`ANY_TO_ANY`

### `USINT_TO_SINT`
- 库类型：`function`
- 输入：`IN: USINT`
- 输出：`OUT: SINT`
- 筛选器：`ANY_TO_ANY`

### `USINT_TO_INT`
- 库类型：`function`
- 输入：`IN: USINT`
- 输出：`OUT: INT`
- 筛选器：`ANY_TO_ANY`

### `USINT_TO_DINT`
- 库类型：`function`
- 输入：`IN: USINT`
- 输出：`OUT: DINT`
- 筛选器：`ANY_TO_ANY`

### `USINT_TO_LINT`
- 库类型：`function`
- 输入：`IN: USINT`
- 输出：`OUT: LINT`
- 筛选器：`ANY_TO_ANY`

### `USINT_TO_UINT`
- 库类型：`function`
- 输入：`IN: USINT`
- 输出：`OUT: UINT`
- 筛选器：`ANY_TO_ANY`

### `USINT_TO_UDINT`
- 库类型：`function`
- 输入：`IN: USINT`
- 输出：`OUT: UDINT`
- 筛选器：`ANY_TO_ANY`

### `USINT_TO_ULINT`
- 库类型：`function`
- 输入：`IN: USINT`
- 输出：`OUT: ULINT`
- 筛选器：`ANY_TO_ANY`

### `USINT_TO_REAL`
- 库类型：`function`
- 输入：`IN: USINT`
- 输出：`OUT: REAL`
- 筛选器：`ANY_TO_ANY`

### `USINT_TO_LREAL`
- 库类型：`function`
- 输入：`IN: USINT`
- 输出：`OUT: LREAL`
- 筛选器：`ANY_TO_ANY`

### `USINT_TO_TIME`
- 库类型：`function`
- 输入：`IN: USINT`
- 输出：`OUT: TIME`
- 筛选器：`ANY_TO_ANY`

### `USINT_TO_DATE`
- 库类型：`function`
- 输入：`IN: USINT`
- 输出：`OUT: DATE`
- 筛选器：`ANY_TO_ANY`

### `USINT_TO_TOD`
- 库类型：`function`
- 输入：`IN: USINT`
- 输出：`OUT: TOD`
- 筛选器：`ANY_TO_ANY`

### `USINT_TO_DT`
- 库类型：`function`
- 输入：`IN: USINT`
- 输出：`OUT: DT`
- 筛选器：`ANY_TO_ANY`

### `USINT_TO_STRING`
- 库类型：`function`
- 输入：`IN: USINT`
- 输出：`OUT: STRING`
- 筛选器：`ANY_TO_ANY`

### `USINT_TO_BYTE`
- 库类型：`function`
- 输入：`IN: USINT`
- 输出：`OUT: BYTE`
- 筛选器：`ANY_TO_ANY`

### `USINT_TO_WORD`
- 库类型：`function`
- 输入：`IN: USINT`
- 输出：`OUT: WORD`
- 筛选器：`ANY_TO_ANY`

### `USINT_TO_DWORD`
- 库类型：`function`
- 输入：`IN: USINT`
- 输出：`OUT: DWORD`
- 筛选器：`ANY_TO_ANY`

### `USINT_TO_LWORD`
- 库类型：`function`
- 输入：`IN: USINT`
- 输出：`OUT: LWORD`
- 筛选器：`ANY_TO_ANY`

### `UINT_TO_BOOL`
- 库类型：`function`
- 输入：`IN: UINT`
- 输出：`OUT: BOOL`
- 筛选器：`ANY_TO_ANY`

### `UINT_TO_SINT`
- 库类型：`function`
- 输入：`IN: UINT`
- 输出：`OUT: SINT`
- 筛选器：`ANY_TO_ANY`

### `UINT_TO_INT`
- 库类型：`function`
- 输入：`IN: UINT`
- 输出：`OUT: INT`
- 筛选器：`ANY_TO_ANY`

### `UINT_TO_DINT`
- 库类型：`function`
- 输入：`IN: UINT`
- 输出：`OUT: DINT`
- 筛选器：`ANY_TO_ANY`

### `UINT_TO_LINT`
- 库类型：`function`
- 输入：`IN: UINT`
- 输出：`OUT: LINT`
- 筛选器：`ANY_TO_ANY`

### `UINT_TO_USINT`
- 库类型：`function`
- 输入：`IN: UINT`
- 输出：`OUT: USINT`
- 筛选器：`ANY_TO_ANY`

### `UINT_TO_UDINT`
- 库类型：`function`
- 输入：`IN: UINT`
- 输出：`OUT: UDINT`
- 筛选器：`ANY_TO_ANY`

### `UINT_TO_ULINT`
- 库类型：`function`
- 输入：`IN: UINT`
- 输出：`OUT: ULINT`
- 筛选器：`ANY_TO_ANY`

### `UINT_TO_REAL`
- 库类型：`function`
- 输入：`IN: UINT`
- 输出：`OUT: REAL`
- 筛选器：`ANY_TO_ANY`

### `UINT_TO_LREAL`
- 库类型：`function`
- 输入：`IN: UINT`
- 输出：`OUT: LREAL`
- 筛选器：`ANY_TO_ANY`

### `UINT_TO_TIME`
- 库类型：`function`
- 输入：`IN: UINT`
- 输出：`OUT: TIME`
- 筛选器：`ANY_TO_ANY`

### `UINT_TO_DATE`
- 库类型：`function`
- 输入：`IN: UINT`
- 输出：`OUT: DATE`
- 筛选器：`ANY_TO_ANY`

### `UINT_TO_TOD`
- 库类型：`function`
- 输入：`IN: UINT`
- 输出：`OUT: TOD`
- 筛选器：`ANY_TO_ANY`

### `UINT_TO_DT`
- 库类型：`function`
- 输入：`IN: UINT`
- 输出：`OUT: DT`
- 筛选器：`ANY_TO_ANY`

### `UINT_TO_STRING`
- 库类型：`function`
- 输入：`IN: UINT`
- 输出：`OUT: STRING`
- 筛选器：`ANY_TO_ANY`

### `UINT_TO_BYTE`
- 库类型：`function`
- 输入：`IN: UINT`
- 输出：`OUT: BYTE`
- 筛选器：`ANY_TO_ANY`

### `UINT_TO_WORD`
- 库类型：`function`
- 输入：`IN: UINT`
- 输出：`OUT: WORD`
- 筛选器：`ANY_TO_ANY`

### `UINT_TO_DWORD`
- 库类型：`function`
- 输入：`IN: UINT`
- 输出：`OUT: DWORD`
- 筛选器：`ANY_TO_ANY`

### `UINT_TO_LWORD`
- 库类型：`function`
- 输入：`IN: UINT`
- 输出：`OUT: LWORD`
- 筛选器：`ANY_TO_ANY`

### `UDINT_TO_BOOL`
- 库类型：`function`
- 输入：`IN: UDINT`
- 输出：`OUT: BOOL`
- 筛选器：`ANY_TO_ANY`

### `UDINT_TO_SINT`
- 库类型：`function`
- 输入：`IN: UDINT`
- 输出：`OUT: SINT`
- 筛选器：`ANY_TO_ANY`

### `UDINT_TO_INT`
- 库类型：`function`
- 输入：`IN: UDINT`
- 输出：`OUT: INT`
- 筛选器：`ANY_TO_ANY`

### `UDINT_TO_DINT`
- 库类型：`function`
- 输入：`IN: UDINT`
- 输出：`OUT: DINT`
- 筛选器：`ANY_TO_ANY`

### `UDINT_TO_LINT`
- 库类型：`function`
- 输入：`IN: UDINT`
- 输出：`OUT: LINT`
- 筛选器：`ANY_TO_ANY`

### `UDINT_TO_USINT`
- 库类型：`function`
- 输入：`IN: UDINT`
- 输出：`OUT: USINT`
- 筛选器：`ANY_TO_ANY`

### `UDINT_TO_UINT`
- 库类型：`function`
- 输入：`IN: UDINT`
- 输出：`OUT: UINT`
- 筛选器：`ANY_TO_ANY`

### `UDINT_TO_ULINT`
- 库类型：`function`
- 输入：`IN: UDINT`
- 输出：`OUT: ULINT`
- 筛选器：`ANY_TO_ANY`

### `UDINT_TO_REAL`
- 库类型：`function`
- 输入：`IN: UDINT`
- 输出：`OUT: REAL`
- 筛选器：`ANY_TO_ANY`

### `UDINT_TO_LREAL`
- 库类型：`function`
- 输入：`IN: UDINT`
- 输出：`OUT: LREAL`
- 筛选器：`ANY_TO_ANY`

### `UDINT_TO_TIME`
- 库类型：`function`
- 输入：`IN: UDINT`
- 输出：`OUT: TIME`
- 筛选器：`ANY_TO_ANY`

### `UDINT_TO_DATE`
- 库类型：`function`
- 输入：`IN: UDINT`
- 输出：`OUT: DATE`
- 筛选器：`ANY_TO_ANY`

### `UDINT_TO_TOD`
- 库类型：`function`
- 输入：`IN: UDINT`
- 输出：`OUT: TOD`
- 筛选器：`ANY_TO_ANY`

### `UDINT_TO_DT`
- 库类型：`function`
- 输入：`IN: UDINT`
- 输出：`OUT: DT`
- 筛选器：`ANY_TO_ANY`

### `UDINT_TO_STRING`
- 库类型：`function`
- 输入：`IN: UDINT`
- 输出：`OUT: STRING`
- 筛选器：`ANY_TO_ANY`

### `UDINT_TO_BYTE`
- 库类型：`function`
- 输入：`IN: UDINT`
- 输出：`OUT: BYTE`
- 筛选器：`ANY_TO_ANY`

### `UDINT_TO_WORD`
- 库类型：`function`
- 输入：`IN: UDINT`
- 输出：`OUT: WORD`
- 筛选器：`ANY_TO_ANY`

### `UDINT_TO_DWORD`
- 库类型：`function`
- 输入：`IN: UDINT`
- 输出：`OUT: DWORD`
- 筛选器：`ANY_TO_ANY`

### `UDINT_TO_LWORD`
- 库类型：`function`
- 输入：`IN: UDINT`
- 输出：`OUT: LWORD`
- 筛选器：`ANY_TO_ANY`

### `ULINT_TO_BOOL`
- 库类型：`function`
- 输入：`IN: ULINT`
- 输出：`OUT: BOOL`
- 筛选器：`ANY_TO_ANY`

### `ULINT_TO_SINT`
- 库类型：`function`
- 输入：`IN: ULINT`
- 输出：`OUT: SINT`
- 筛选器：`ANY_TO_ANY`

### `ULINT_TO_INT`
- 库类型：`function`
- 输入：`IN: ULINT`
- 输出：`OUT: INT`
- 筛选器：`ANY_TO_ANY`

### `ULINT_TO_DINT`
- 库类型：`function`
- 输入：`IN: ULINT`
- 输出：`OUT: DINT`
- 筛选器：`ANY_TO_ANY`

### `ULINT_TO_LINT`
- 库类型：`function`
- 输入：`IN: ULINT`
- 输出：`OUT: LINT`
- 筛选器：`ANY_TO_ANY`

### `ULINT_TO_USINT`
- 库类型：`function`
- 输入：`IN: ULINT`
- 输出：`OUT: USINT`
- 筛选器：`ANY_TO_ANY`

### `ULINT_TO_UINT`
- 库类型：`function`
- 输入：`IN: ULINT`
- 输出：`OUT: UINT`
- 筛选器：`ANY_TO_ANY`

### `ULINT_TO_UDINT`
- 库类型：`function`
- 输入：`IN: ULINT`
- 输出：`OUT: UDINT`
- 筛选器：`ANY_TO_ANY`

### `ULINT_TO_REAL`
- 库类型：`function`
- 输入：`IN: ULINT`
- 输出：`OUT: REAL`
- 筛选器：`ANY_TO_ANY`

### `ULINT_TO_LREAL`
- 库类型：`function`
- 输入：`IN: ULINT`
- 输出：`OUT: LREAL`
- 筛选器：`ANY_TO_ANY`

### `ULINT_TO_TIME`
- 库类型：`function`
- 输入：`IN: ULINT`
- 输出：`OUT: TIME`
- 筛选器：`ANY_TO_ANY`

### `ULINT_TO_DATE`
- 库类型：`function`
- 输入：`IN: ULINT`
- 输出：`OUT: DATE`
- 筛选器：`ANY_TO_ANY`

### `ULINT_TO_TOD`
- 库类型：`function`
- 输入：`IN: ULINT`
- 输出：`OUT: TOD`
- 筛选器：`ANY_TO_ANY`

### `ULINT_TO_DT`
- 库类型：`function`
- 输入：`IN: ULINT`
- 输出：`OUT: DT`
- 筛选器：`ANY_TO_ANY`

### `ULINT_TO_STRING`
- 库类型：`function`
- 输入：`IN: ULINT`
- 输出：`OUT: STRING`
- 筛选器：`ANY_TO_ANY`

### `ULINT_TO_BYTE`
- 库类型：`function`
- 输入：`IN: ULINT`
- 输出：`OUT: BYTE`
- 筛选器：`ANY_TO_ANY`

### `ULINT_TO_WORD`
- 库类型：`function`
- 输入：`IN: ULINT`
- 输出：`OUT: WORD`
- 筛选器：`ANY_TO_ANY`

### `ULINT_TO_DWORD`
- 库类型：`function`
- 输入：`IN: ULINT`
- 输出：`OUT: DWORD`
- 筛选器：`ANY_TO_ANY`

### `ULINT_TO_LWORD`
- 库类型：`function`
- 输入：`IN: ULINT`
- 输出：`OUT: LWORD`
- 筛选器：`ANY_TO_ANY`

### `REAL_TO_BOOL`
- 库类型：`function`
- 输入：`IN: REAL`
- 输出：`OUT: BOOL`
- 筛选器：`ANY_TO_ANY`

### `REAL_TO_SINT`
- 库类型：`function`
- 输入：`IN: REAL`
- 输出：`OUT: SINT`
- 筛选器：`ANY_TO_ANY`

### `REAL_TO_INT`
- 库类型：`function`
- 输入：`IN: REAL`
- 输出：`OUT: INT`
- 筛选器：`ANY_TO_ANY`

### `REAL_TO_DINT`
- 库类型：`function`
- 输入：`IN: REAL`
- 输出：`OUT: DINT`
- 筛选器：`ANY_TO_ANY`

### `REAL_TO_LINT`
- 库类型：`function`
- 输入：`IN: REAL`
- 输出：`OUT: LINT`
- 筛选器：`ANY_TO_ANY`

### `REAL_TO_USINT`
- 库类型：`function`
- 输入：`IN: REAL`
- 输出：`OUT: USINT`
- 筛选器：`ANY_TO_ANY`

### `REAL_TO_UINT`
- 库类型：`function`
- 输入：`IN: REAL`
- 输出：`OUT: UINT`
- 筛选器：`ANY_TO_ANY`

### `REAL_TO_UDINT`
- 库类型：`function`
- 输入：`IN: REAL`
- 输出：`OUT: UDINT`
- 筛选器：`ANY_TO_ANY`

### `REAL_TO_ULINT`
- 库类型：`function`
- 输入：`IN: REAL`
- 输出：`OUT: ULINT`
- 筛选器：`ANY_TO_ANY`

### `REAL_TO_LREAL`
- 库类型：`function`
- 输入：`IN: REAL`
- 输出：`OUT: LREAL`
- 筛选器：`ANY_TO_ANY`

### `REAL_TO_TIME`
- 库类型：`function`
- 输入：`IN: REAL`
- 输出：`OUT: TIME`
- 筛选器：`ANY_TO_ANY`

### `REAL_TO_DATE`
- 库类型：`function`
- 输入：`IN: REAL`
- 输出：`OUT: DATE`
- 筛选器：`ANY_TO_ANY`

### `REAL_TO_TOD`
- 库类型：`function`
- 输入：`IN: REAL`
- 输出：`OUT: TOD`
- 筛选器：`ANY_TO_ANY`

### `REAL_TO_DT`
- 库类型：`function`
- 输入：`IN: REAL`
- 输出：`OUT: DT`
- 筛选器：`ANY_TO_ANY`

### `REAL_TO_STRING`
- 库类型：`function`
- 输入：`IN: REAL`
- 输出：`OUT: STRING`
- 筛选器：`ANY_TO_ANY`

### `REAL_TO_BYTE`
- 库类型：`function`
- 输入：`IN: REAL`
- 输出：`OUT: BYTE`
- 筛选器：`ANY_TO_ANY`

### `REAL_TO_WORD`
- 库类型：`function`
- 输入：`IN: REAL`
- 输出：`OUT: WORD`
- 筛选器：`ANY_TO_ANY`

### `REAL_TO_DWORD`
- 库类型：`function`
- 输入：`IN: REAL`
- 输出：`OUT: DWORD`
- 筛选器：`ANY_TO_ANY`

### `REAL_TO_LWORD`
- 库类型：`function`
- 输入：`IN: REAL`
- 输出：`OUT: LWORD`
- 筛选器：`ANY_TO_ANY`

### `LREAL_TO_BOOL`
- 库类型：`function`
- 输入：`IN: LREAL`
- 输出：`OUT: BOOL`
- 筛选器：`ANY_TO_ANY`

### `LREAL_TO_SINT`
- 库类型：`function`
- 输入：`IN: LREAL`
- 输出：`OUT: SINT`
- 筛选器：`ANY_TO_ANY`

### `LREAL_TO_INT`
- 库类型：`function`
- 输入：`IN: LREAL`
- 输出：`OUT: INT`
- 筛选器：`ANY_TO_ANY`

### `LREAL_TO_DINT`
- 库类型：`function`
- 输入：`IN: LREAL`
- 输出：`OUT: DINT`
- 筛选器：`ANY_TO_ANY`

### `LREAL_TO_LINT`
- 库类型：`function`
- 输入：`IN: LREAL`
- 输出：`OUT: LINT`
- 筛选器：`ANY_TO_ANY`

### `LREAL_TO_USINT`
- 库类型：`function`
- 输入：`IN: LREAL`
- 输出：`OUT: USINT`
- 筛选器：`ANY_TO_ANY`

### `LREAL_TO_UINT`
- 库类型：`function`
- 输入：`IN: LREAL`
- 输出：`OUT: UINT`
- 筛选器：`ANY_TO_ANY`

### `LREAL_TO_UDINT`
- 库类型：`function`
- 输入：`IN: LREAL`
- 输出：`OUT: UDINT`
- 筛选器：`ANY_TO_ANY`

### `LREAL_TO_ULINT`
- 库类型：`function`
- 输入：`IN: LREAL`
- 输出：`OUT: ULINT`
- 筛选器：`ANY_TO_ANY`

### `LREAL_TO_REAL`
- 库类型：`function`
- 输入：`IN: LREAL`
- 输出：`OUT: REAL`
- 筛选器：`ANY_TO_ANY`

### `LREAL_TO_TIME`
- 库类型：`function`
- 输入：`IN: LREAL`
- 输出：`OUT: TIME`
- 筛选器：`ANY_TO_ANY`

### `LREAL_TO_DATE`
- 库类型：`function`
- 输入：`IN: LREAL`
- 输出：`OUT: DATE`
- 筛选器：`ANY_TO_ANY`

### `LREAL_TO_TOD`
- 库类型：`function`
- 输入：`IN: LREAL`
- 输出：`OUT: TOD`
- 筛选器：`ANY_TO_ANY`

### `LREAL_TO_DT`
- 库类型：`function`
- 输入：`IN: LREAL`
- 输出：`OUT: DT`
- 筛选器：`ANY_TO_ANY`

### `LREAL_TO_STRING`
- 库类型：`function`
- 输入：`IN: LREAL`
- 输出：`OUT: STRING`
- 筛选器：`ANY_TO_ANY`

### `LREAL_TO_BYTE`
- 库类型：`function`
- 输入：`IN: LREAL`
- 输出：`OUT: BYTE`
- 筛选器：`ANY_TO_ANY`

### `LREAL_TO_WORD`
- 库类型：`function`
- 输入：`IN: LREAL`
- 输出：`OUT: WORD`
- 筛选器：`ANY_TO_ANY`

### `LREAL_TO_DWORD`
- 库类型：`function`
- 输入：`IN: LREAL`
- 输出：`OUT: DWORD`
- 筛选器：`ANY_TO_ANY`

### `LREAL_TO_LWORD`
- 库类型：`function`
- 输入：`IN: LREAL`
- 输出：`OUT: LWORD`
- 筛选器：`ANY_TO_ANY`

### `TIME_TO_SINT`
- 库类型：`function`
- 输入：`IN: TIME`
- 输出：`OUT: SINT`
- 筛选器：`ANY_TO_ANY`

### `TIME_TO_INT`
- 库类型：`function`
- 输入：`IN: TIME`
- 输出：`OUT: INT`
- 筛选器：`ANY_TO_ANY`

### `TIME_TO_DINT`
- 库类型：`function`
- 输入：`IN: TIME`
- 输出：`OUT: DINT`
- 筛选器：`ANY_TO_ANY`

### `TIME_TO_LINT`
- 库类型：`function`
- 输入：`IN: TIME`
- 输出：`OUT: LINT`
- 筛选器：`ANY_TO_ANY`

### `TIME_TO_USINT`
- 库类型：`function`
- 输入：`IN: TIME`
- 输出：`OUT: USINT`
- 筛选器：`ANY_TO_ANY`

### `TIME_TO_UINT`
- 库类型：`function`
- 输入：`IN: TIME`
- 输出：`OUT: UINT`
- 筛选器：`ANY_TO_ANY`

### `TIME_TO_UDINT`
- 库类型：`function`
- 输入：`IN: TIME`
- 输出：`OUT: UDINT`
- 筛选器：`ANY_TO_ANY`

### `TIME_TO_ULINT`
- 库类型：`function`
- 输入：`IN: TIME`
- 输出：`OUT: ULINT`
- 筛选器：`ANY_TO_ANY`

### `TIME_TO_REAL`
- 库类型：`function`
- 输入：`IN: TIME`
- 输出：`OUT: REAL`
- 筛选器：`ANY_TO_ANY`

### `TIME_TO_LREAL`
- 库类型：`function`
- 输入：`IN: TIME`
- 输出：`OUT: LREAL`
- 筛选器：`ANY_TO_ANY`

### `TIME_TO_STRING`
- 库类型：`function`
- 输入：`IN: TIME`
- 输出：`OUT: STRING`
- 筛选器：`ANY_TO_ANY`

### `TIME_TO_BYTE`
- 库类型：`function`
- 输入：`IN: TIME`
- 输出：`OUT: BYTE`
- 筛选器：`ANY_TO_ANY`

### `TIME_TO_WORD`
- 库类型：`function`
- 输入：`IN: TIME`
- 输出：`OUT: WORD`
- 筛选器：`ANY_TO_ANY`

### `TIME_TO_DWORD`
- 库类型：`function`
- 输入：`IN: TIME`
- 输出：`OUT: DWORD`
- 筛选器：`ANY_TO_ANY`

### `TIME_TO_LWORD`
- 库类型：`function`
- 输入：`IN: TIME`
- 输出：`OUT: LWORD`
- 筛选器：`ANY_TO_ANY`

### `DATE_TO_SINT`
- 库类型：`function`
- 输入：`IN: DATE`
- 输出：`OUT: SINT`
- 筛选器：`ANY_TO_ANY`

### `DATE_TO_INT`
- 库类型：`function`
- 输入：`IN: DATE`
- 输出：`OUT: INT`
- 筛选器：`ANY_TO_ANY`

### `DATE_TO_DINT`
- 库类型：`function`
- 输入：`IN: DATE`
- 输出：`OUT: DINT`
- 筛选器：`ANY_TO_ANY`

### `DATE_TO_LINT`
- 库类型：`function`
- 输入：`IN: DATE`
- 输出：`OUT: LINT`
- 筛选器：`ANY_TO_ANY`

### `DATE_TO_USINT`
- 库类型：`function`
- 输入：`IN: DATE`
- 输出：`OUT: USINT`
- 筛选器：`ANY_TO_ANY`

### `DATE_TO_UINT`
- 库类型：`function`
- 输入：`IN: DATE`
- 输出：`OUT: UINT`
- 筛选器：`ANY_TO_ANY`

### `DATE_TO_UDINT`
- 库类型：`function`
- 输入：`IN: DATE`
- 输出：`OUT: UDINT`
- 筛选器：`ANY_TO_ANY`

### `DATE_TO_ULINT`
- 库类型：`function`
- 输入：`IN: DATE`
- 输出：`OUT: ULINT`
- 筛选器：`ANY_TO_ANY`

### `DATE_TO_REAL`
- 库类型：`function`
- 输入：`IN: DATE`
- 输出：`OUT: REAL`
- 筛选器：`ANY_TO_ANY`

### `DATE_TO_LREAL`
- 库类型：`function`
- 输入：`IN: DATE`
- 输出：`OUT: LREAL`
- 筛选器：`ANY_TO_ANY`

### `DATE_TO_STRING`
- 库类型：`function`
- 输入：`IN: DATE`
- 输出：`OUT: STRING`
- 筛选器：`ANY_TO_ANY`

### `DATE_TO_BYTE`
- 库类型：`function`
- 输入：`IN: DATE`
- 输出：`OUT: BYTE`
- 筛选器：`ANY_TO_ANY`

### `DATE_TO_WORD`
- 库类型：`function`
- 输入：`IN: DATE`
- 输出：`OUT: WORD`
- 筛选器：`ANY_TO_ANY`

### `DATE_TO_DWORD`
- 库类型：`function`
- 输入：`IN: DATE`
- 输出：`OUT: DWORD`
- 筛选器：`ANY_TO_ANY`

### `DATE_TO_LWORD`
- 库类型：`function`
- 输入：`IN: DATE`
- 输出：`OUT: LWORD`
- 筛选器：`ANY_TO_ANY`

### `TOD_TO_SINT`
- 库类型：`function`
- 输入：`IN: TOD`
- 输出：`OUT: SINT`
- 筛选器：`ANY_TO_ANY`

### `TOD_TO_INT`
- 库类型：`function`
- 输入：`IN: TOD`
- 输出：`OUT: INT`
- 筛选器：`ANY_TO_ANY`

### `TOD_TO_DINT`
- 库类型：`function`
- 输入：`IN: TOD`
- 输出：`OUT: DINT`
- 筛选器：`ANY_TO_ANY`

### `TOD_TO_LINT`
- 库类型：`function`
- 输入：`IN: TOD`
- 输出：`OUT: LINT`
- 筛选器：`ANY_TO_ANY`

### `TOD_TO_USINT`
- 库类型：`function`
- 输入：`IN: TOD`
- 输出：`OUT: USINT`
- 筛选器：`ANY_TO_ANY`

### `TOD_TO_UINT`
- 库类型：`function`
- 输入：`IN: TOD`
- 输出：`OUT: UINT`
- 筛选器：`ANY_TO_ANY`

### `TOD_TO_UDINT`
- 库类型：`function`
- 输入：`IN: TOD`
- 输出：`OUT: UDINT`
- 筛选器：`ANY_TO_ANY`

### `TOD_TO_ULINT`
- 库类型：`function`
- 输入：`IN: TOD`
- 输出：`OUT: ULINT`
- 筛选器：`ANY_TO_ANY`

### `TOD_TO_REAL`
- 库类型：`function`
- 输入：`IN: TOD`
- 输出：`OUT: REAL`
- 筛选器：`ANY_TO_ANY`

### `TOD_TO_LREAL`
- 库类型：`function`
- 输入：`IN: TOD`
- 输出：`OUT: LREAL`
- 筛选器：`ANY_TO_ANY`

### `TOD_TO_STRING`
- 库类型：`function`
- 输入：`IN: TOD`
- 输出：`OUT: STRING`
- 筛选器：`ANY_TO_ANY`

### `TOD_TO_BYTE`
- 库类型：`function`
- 输入：`IN: TOD`
- 输出：`OUT: BYTE`
- 筛选器：`ANY_TO_ANY`

### `TOD_TO_WORD`
- 库类型：`function`
- 输入：`IN: TOD`
- 输出：`OUT: WORD`
- 筛选器：`ANY_TO_ANY`

### `TOD_TO_DWORD`
- 库类型：`function`
- 输入：`IN: TOD`
- 输出：`OUT: DWORD`
- 筛选器：`ANY_TO_ANY`

### `TOD_TO_LWORD`
- 库类型：`function`
- 输入：`IN: TOD`
- 输出：`OUT: LWORD`
- 筛选器：`ANY_TO_ANY`

### `DT_TO_SINT`
- 库类型：`function`
- 输入：`IN: DT`
- 输出：`OUT: SINT`
- 筛选器：`ANY_TO_ANY`

### `DT_TO_INT`
- 库类型：`function`
- 输入：`IN: DT`
- 输出：`OUT: INT`
- 筛选器：`ANY_TO_ANY`

### `DT_TO_DINT`
- 库类型：`function`
- 输入：`IN: DT`
- 输出：`OUT: DINT`
- 筛选器：`ANY_TO_ANY`

### `DT_TO_LINT`
- 库类型：`function`
- 输入：`IN: DT`
- 输出：`OUT: LINT`
- 筛选器：`ANY_TO_ANY`

### `DT_TO_USINT`
- 库类型：`function`
- 输入：`IN: DT`
- 输出：`OUT: USINT`
- 筛选器：`ANY_TO_ANY`

### `DT_TO_UINT`
- 库类型：`function`
- 输入：`IN: DT`
- 输出：`OUT: UINT`
- 筛选器：`ANY_TO_ANY`

### `DT_TO_UDINT`
- 库类型：`function`
- 输入：`IN: DT`
- 输出：`OUT: UDINT`
- 筛选器：`ANY_TO_ANY`

### `DT_TO_ULINT`
- 库类型：`function`
- 输入：`IN: DT`
- 输出：`OUT: ULINT`
- 筛选器：`ANY_TO_ANY`

### `DT_TO_REAL`
- 库类型：`function`
- 输入：`IN: DT`
- 输出：`OUT: REAL`
- 筛选器：`ANY_TO_ANY`

### `DT_TO_LREAL`
- 库类型：`function`
- 输入：`IN: DT`
- 输出：`OUT: LREAL`
- 筛选器：`ANY_TO_ANY`

### `DT_TO_STRING`
- 库类型：`function`
- 输入：`IN: DT`
- 输出：`OUT: STRING`
- 筛选器：`ANY_TO_ANY`

### `DT_TO_BYTE`
- 库类型：`function`
- 输入：`IN: DT`
- 输出：`OUT: BYTE`
- 筛选器：`ANY_TO_ANY`

### `DT_TO_WORD`
- 库类型：`function`
- 输入：`IN: DT`
- 输出：`OUT: WORD`
- 筛选器：`ANY_TO_ANY`

### `DT_TO_DWORD`
- 库类型：`function`
- 输入：`IN: DT`
- 输出：`OUT: DWORD`
- 筛选器：`ANY_TO_ANY`

### `DT_TO_LWORD`
- 库类型：`function`
- 输入：`IN: DT`
- 输出：`OUT: LWORD`
- 筛选器：`ANY_TO_ANY`

### `STRING_TO_BOOL`
- 库类型：`function`
- 输入：`IN: STRING`
- 输出：`OUT: BOOL`
- 筛选器：`ANY_TO_ANY`

### `STRING_TO_SINT`
- 库类型：`function`
- 输入：`IN: STRING`
- 输出：`OUT: SINT`
- 筛选器：`ANY_TO_ANY`

### `STRING_TO_INT`
- 库类型：`function`
- 输入：`IN: STRING`
- 输出：`OUT: INT`
- 筛选器：`ANY_TO_ANY`

### `STRING_TO_DINT`
- 库类型：`function`
- 输入：`IN: STRING`
- 输出：`OUT: DINT`
- 筛选器：`ANY_TO_ANY`

### `STRING_TO_LINT`
- 库类型：`function`
- 输入：`IN: STRING`
- 输出：`OUT: LINT`
- 筛选器：`ANY_TO_ANY`

### `STRING_TO_USINT`
- 库类型：`function`
- 输入：`IN: STRING`
- 输出：`OUT: USINT`
- 筛选器：`ANY_TO_ANY`

### `STRING_TO_UINT`
- 库类型：`function`
- 输入：`IN: STRING`
- 输出：`OUT: UINT`
- 筛选器：`ANY_TO_ANY`

### `STRING_TO_UDINT`
- 库类型：`function`
- 输入：`IN: STRING`
- 输出：`OUT: UDINT`
- 筛选器：`ANY_TO_ANY`

### `STRING_TO_ULINT`
- 库类型：`function`
- 输入：`IN: STRING`
- 输出：`OUT: ULINT`
- 筛选器：`ANY_TO_ANY`

### `STRING_TO_REAL`
- 库类型：`function`
- 输入：`IN: STRING`
- 输出：`OUT: REAL`
- 筛选器：`ANY_TO_ANY`

### `STRING_TO_LREAL`
- 库类型：`function`
- 输入：`IN: STRING`
- 输出：`OUT: LREAL`
- 筛选器：`ANY_TO_ANY`

### `STRING_TO_TIME`
- 库类型：`function`
- 输入：`IN: STRING`
- 输出：`OUT: TIME`
- 筛选器：`ANY_TO_ANY`

### `STRING_TO_DATE`
- 库类型：`function`
- 输入：`IN: STRING`
- 输出：`OUT: DATE`
- 筛选器：`ANY_TO_ANY`

### `STRING_TO_TOD`
- 库类型：`function`
- 输入：`IN: STRING`
- 输出：`OUT: TOD`
- 筛选器：`ANY_TO_ANY`

### `STRING_TO_DT`
- 库类型：`function`
- 输入：`IN: STRING`
- 输出：`OUT: DT`
- 筛选器：`ANY_TO_ANY`

### `STRING_TO_BYTE`
- 库类型：`function`
- 输入：`IN: STRING`
- 输出：`OUT: BYTE`
- 筛选器：`ANY_TO_ANY`

### `STRING_TO_WORD`
- 库类型：`function`
- 输入：`IN: STRING`
- 输出：`OUT: WORD`
- 筛选器：`ANY_TO_ANY`

### `STRING_TO_DWORD`
- 库类型：`function`
- 输入：`IN: STRING`
- 输出：`OUT: DWORD`
- 筛选器：`ANY_TO_ANY`

### `STRING_TO_LWORD`
- 库类型：`function`
- 输入：`IN: STRING`
- 输出：`OUT: LWORD`
- 筛选器：`ANY_TO_ANY`

### `BYTE_TO_BOOL`
- 库类型：`function`
- 输入：`IN: BYTE`
- 输出：`OUT: BOOL`
- 筛选器：`ANY_TO_ANY`

### `BYTE_TO_SINT`
- 库类型：`function`
- 输入：`IN: BYTE`
- 输出：`OUT: SINT`
- 筛选器：`ANY_TO_ANY`

### `BYTE_TO_INT`
- 库类型：`function`
- 输入：`IN: BYTE`
- 输出：`OUT: INT`
- 筛选器：`ANY_TO_ANY`

### `BYTE_TO_DINT`
- 库类型：`function`
- 输入：`IN: BYTE`
- 输出：`OUT: DINT`
- 筛选器：`ANY_TO_ANY`

### `BYTE_TO_LINT`
- 库类型：`function`
- 输入：`IN: BYTE`
- 输出：`OUT: LINT`
- 筛选器：`ANY_TO_ANY`

### `BYTE_TO_USINT`
- 库类型：`function`
- 输入：`IN: BYTE`
- 输出：`OUT: USINT`
- 筛选器：`ANY_TO_ANY`

### `BYTE_TO_UINT`
- 库类型：`function`
- 输入：`IN: BYTE`
- 输出：`OUT: UINT`
- 筛选器：`ANY_TO_ANY`

### `BYTE_TO_UDINT`
- 库类型：`function`
- 输入：`IN: BYTE`
- 输出：`OUT: UDINT`
- 筛选器：`ANY_TO_ANY`

### `BYTE_TO_ULINT`
- 库类型：`function`
- 输入：`IN: BYTE`
- 输出：`OUT: ULINT`
- 筛选器：`ANY_TO_ANY`

### `BYTE_TO_REAL`
- 库类型：`function`
- 输入：`IN: BYTE`
- 输出：`OUT: REAL`
- 筛选器：`ANY_TO_ANY`

### `BYTE_TO_LREAL`
- 库类型：`function`
- 输入：`IN: BYTE`
- 输出：`OUT: LREAL`
- 筛选器：`ANY_TO_ANY`

### `BYTE_TO_TIME`
- 库类型：`function`
- 输入：`IN: BYTE`
- 输出：`OUT: TIME`
- 筛选器：`ANY_TO_ANY`

### `BYTE_TO_DATE`
- 库类型：`function`
- 输入：`IN: BYTE`
- 输出：`OUT: DATE`
- 筛选器：`ANY_TO_ANY`

### `BYTE_TO_TOD`
- 库类型：`function`
- 输入：`IN: BYTE`
- 输出：`OUT: TOD`
- 筛选器：`ANY_TO_ANY`

### `BYTE_TO_DT`
- 库类型：`function`
- 输入：`IN: BYTE`
- 输出：`OUT: DT`
- 筛选器：`ANY_TO_ANY`

### `BYTE_TO_STRING`
- 库类型：`function`
- 输入：`IN: BYTE`
- 输出：`OUT: STRING`
- 筛选器：`ANY_TO_ANY`

### `BYTE_TO_WORD`
- 库类型：`function`
- 输入：`IN: BYTE`
- 输出：`OUT: WORD`
- 筛选器：`ANY_TO_ANY`

### `BYTE_TO_DWORD`
- 库类型：`function`
- 输入：`IN: BYTE`
- 输出：`OUT: DWORD`
- 筛选器：`ANY_TO_ANY`

### `BYTE_TO_LWORD`
- 库类型：`function`
- 输入：`IN: BYTE`
- 输出：`OUT: LWORD`
- 筛选器：`ANY_TO_ANY`

### `WORD_TO_BOOL`
- 库类型：`function`
- 输入：`IN: WORD`
- 输出：`OUT: BOOL`
- 筛选器：`ANY_TO_ANY`

### `WORD_TO_SINT`
- 库类型：`function`
- 输入：`IN: WORD`
- 输出：`OUT: SINT`
- 筛选器：`ANY_TO_ANY`

### `WORD_TO_INT`
- 库类型：`function`
- 输入：`IN: WORD`
- 输出：`OUT: INT`
- 筛选器：`ANY_TO_ANY`

### `WORD_TO_DINT`
- 库类型：`function`
- 输入：`IN: WORD`
- 输出：`OUT: DINT`
- 筛选器：`ANY_TO_ANY`

### `WORD_TO_LINT`
- 库类型：`function`
- 输入：`IN: WORD`
- 输出：`OUT: LINT`
- 筛选器：`ANY_TO_ANY`

### `WORD_TO_USINT`
- 库类型：`function`
- 输入：`IN: WORD`
- 输出：`OUT: USINT`
- 筛选器：`ANY_TO_ANY`

### `WORD_TO_UINT`
- 库类型：`function`
- 输入：`IN: WORD`
- 输出：`OUT: UINT`
- 筛选器：`ANY_TO_ANY`

### `WORD_TO_UDINT`
- 库类型：`function`
- 输入：`IN: WORD`
- 输出：`OUT: UDINT`
- 筛选器：`ANY_TO_ANY`

### `WORD_TO_ULINT`
- 库类型：`function`
- 输入：`IN: WORD`
- 输出：`OUT: ULINT`
- 筛选器：`ANY_TO_ANY`

### `WORD_TO_REAL`
- 库类型：`function`
- 输入：`IN: WORD`
- 输出：`OUT: REAL`
- 筛选器：`ANY_TO_ANY`

### `WORD_TO_LREAL`
- 库类型：`function`
- 输入：`IN: WORD`
- 输出：`OUT: LREAL`
- 筛选器：`ANY_TO_ANY`

### `WORD_TO_TIME`
- 库类型：`function`
- 输入：`IN: WORD`
- 输出：`OUT: TIME`
- 筛选器：`ANY_TO_ANY`

### `WORD_TO_DATE`
- 库类型：`function`
- 输入：`IN: WORD`
- 输出：`OUT: DATE`
- 筛选器：`ANY_TO_ANY`

### `WORD_TO_TOD`
- 库类型：`function`
- 输入：`IN: WORD`
- 输出：`OUT: TOD`
- 筛选器：`ANY_TO_ANY`

### `WORD_TO_DT`
- 库类型：`function`
- 输入：`IN: WORD`
- 输出：`OUT: DT`
- 筛选器：`ANY_TO_ANY`

### `WORD_TO_STRING`
- 库类型：`function`
- 输入：`IN: WORD`
- 输出：`OUT: STRING`
- 筛选器：`ANY_TO_ANY`

### `WORD_TO_BYTE`
- 库类型：`function`
- 输入：`IN: WORD`
- 输出：`OUT: BYTE`
- 筛选器：`ANY_TO_ANY`

### `WORD_TO_DWORD`
- 库类型：`function`
- 输入：`IN: WORD`
- 输出：`OUT: DWORD`
- 筛选器：`ANY_TO_ANY`

### `WORD_TO_LWORD`
- 库类型：`function`
- 输入：`IN: WORD`
- 输出：`OUT: LWORD`
- 筛选器：`ANY_TO_ANY`

### `DWORD_TO_BOOL`
- 库类型：`function`
- 输入：`IN: DWORD`
- 输出：`OUT: BOOL`
- 筛选器：`ANY_TO_ANY`

### `DWORD_TO_SINT`
- 库类型：`function`
- 输入：`IN: DWORD`
- 输出：`OUT: SINT`
- 筛选器：`ANY_TO_ANY`

### `DWORD_TO_INT`
- 库类型：`function`
- 输入：`IN: DWORD`
- 输出：`OUT: INT`
- 筛选器：`ANY_TO_ANY`

### `DWORD_TO_DINT`
- 库类型：`function`
- 输入：`IN: DWORD`
- 输出：`OUT: DINT`
- 筛选器：`ANY_TO_ANY`

### `DWORD_TO_LINT`
- 库类型：`function`
- 输入：`IN: DWORD`
- 输出：`OUT: LINT`
- 筛选器：`ANY_TO_ANY`

### `DWORD_TO_USINT`
- 库类型：`function`
- 输入：`IN: DWORD`
- 输出：`OUT: USINT`
- 筛选器：`ANY_TO_ANY`

### `DWORD_TO_UINT`
- 库类型：`function`
- 输入：`IN: DWORD`
- 输出：`OUT: UINT`
- 筛选器：`ANY_TO_ANY`

### `DWORD_TO_UDINT`
- 库类型：`function`
- 输入：`IN: DWORD`
- 输出：`OUT: UDINT`
- 筛选器：`ANY_TO_ANY`

### `DWORD_TO_ULINT`
- 库类型：`function`
- 输入：`IN: DWORD`
- 输出：`OUT: ULINT`
- 筛选器：`ANY_TO_ANY`

### `DWORD_TO_REAL`
- 库类型：`function`
- 输入：`IN: DWORD`
- 输出：`OUT: REAL`
- 筛选器：`ANY_TO_ANY`

### `DWORD_TO_LREAL`
- 库类型：`function`
- 输入：`IN: DWORD`
- 输出：`OUT: LREAL`
- 筛选器：`ANY_TO_ANY`

### `DWORD_TO_TIME`
- 库类型：`function`
- 输入：`IN: DWORD`
- 输出：`OUT: TIME`
- 筛选器：`ANY_TO_ANY`

### `DWORD_TO_DATE`
- 库类型：`function`
- 输入：`IN: DWORD`
- 输出：`OUT: DATE`
- 筛选器：`ANY_TO_ANY`

### `DWORD_TO_TOD`
- 库类型：`function`
- 输入：`IN: DWORD`
- 输出：`OUT: TOD`
- 筛选器：`ANY_TO_ANY`

### `DWORD_TO_DT`
- 库类型：`function`
- 输入：`IN: DWORD`
- 输出：`OUT: DT`
- 筛选器：`ANY_TO_ANY`

### `DWORD_TO_STRING`
- 库类型：`function`
- 输入：`IN: DWORD`
- 输出：`OUT: STRING`
- 筛选器：`ANY_TO_ANY`

### `DWORD_TO_BYTE`
- 库类型：`function`
- 输入：`IN: DWORD`
- 输出：`OUT: BYTE`
- 筛选器：`ANY_TO_ANY`

### `DWORD_TO_WORD`
- 库类型：`function`
- 输入：`IN: DWORD`
- 输出：`OUT: WORD`
- 筛选器：`ANY_TO_ANY`

### `DWORD_TO_LWORD`
- 库类型：`function`
- 输入：`IN: DWORD`
- 输出：`OUT: LWORD`
- 筛选器：`ANY_TO_ANY`

### `LWORD_TO_BOOL`
- 库类型：`function`
- 输入：`IN: LWORD`
- 输出：`OUT: BOOL`
- 筛选器：`ANY_TO_ANY`

### `LWORD_TO_SINT`
- 库类型：`function`
- 输入：`IN: LWORD`
- 输出：`OUT: SINT`
- 筛选器：`ANY_TO_ANY`

### `LWORD_TO_INT`
- 库类型：`function`
- 输入：`IN: LWORD`
- 输出：`OUT: INT`
- 筛选器：`ANY_TO_ANY`

### `LWORD_TO_DINT`
- 库类型：`function`
- 输入：`IN: LWORD`
- 输出：`OUT: DINT`
- 筛选器：`ANY_TO_ANY`

### `LWORD_TO_LINT`
- 库类型：`function`
- 输入：`IN: LWORD`
- 输出：`OUT: LINT`
- 筛选器：`ANY_TO_ANY`

### `LWORD_TO_USINT`
- 库类型：`function`
- 输入：`IN: LWORD`
- 输出：`OUT: USINT`
- 筛选器：`ANY_TO_ANY`

### `LWORD_TO_UINT`
- 库类型：`function`
- 输入：`IN: LWORD`
- 输出：`OUT: UINT`
- 筛选器：`ANY_TO_ANY`

### `LWORD_TO_UDINT`
- 库类型：`function`
- 输入：`IN: LWORD`
- 输出：`OUT: UDINT`
- 筛选器：`ANY_TO_ANY`

### `LWORD_TO_ULINT`
- 库类型：`function`
- 输入：`IN: LWORD`
- 输出：`OUT: ULINT`
- 筛选器：`ANY_TO_ANY`

### `LWORD_TO_REAL`
- 库类型：`function`
- 输入：`IN: LWORD`
- 输出：`OUT: REAL`
- 筛选器：`ANY_TO_ANY`

### `LWORD_TO_LREAL`
- 库类型：`function`
- 输入：`IN: LWORD`
- 输出：`OUT: LREAL`
- 筛选器：`ANY_TO_ANY`

### `LWORD_TO_TIME`
- 库类型：`function`
- 输入：`IN: LWORD`
- 输出：`OUT: TIME`
- 筛选器：`ANY_TO_ANY`

### `LWORD_TO_DATE`
- 库类型：`function`
- 输入：`IN: LWORD`
- 输出：`OUT: DATE`
- 筛选器：`ANY_TO_ANY`

### `LWORD_TO_TOD`
- 库类型：`function`
- 输入：`IN: LWORD`
- 输出：`OUT: TOD`
- 筛选器：`ANY_TO_ANY`

### `LWORD_TO_DT`
- 库类型：`function`
- 输入：`IN: LWORD`
- 输出：`OUT: DT`
- 筛选器：`ANY_TO_ANY`

### `LWORD_TO_STRING`
- 库类型：`function`
- 输入：`IN: LWORD`
- 输出：`OUT: STRING`
- 筛选器：`ANY_TO_ANY`

### `LWORD_TO_BYTE`
- 库类型：`function`
- 输入：`IN: LWORD`
- 输出：`OUT: BYTE`
- 筛选器：`ANY_TO_ANY`

### `LWORD_TO_WORD`
- 库类型：`function`
- 输入：`IN: LWORD`
- 输出：`OUT: WORD`
- 筛选器：`ANY_TO_ANY`

### `LWORD_TO_DWORD`
- 库类型：`function`
- 输入：`IN: LWORD`
- 输出：`OUT: DWORD`
- 筛选器：`ANY_TO_ANY`

### `TRUNC`
- 库类型：`function`
- 输入：`IN: ANY_REAL`
- 输出：`OUT: ANY_INT`
- 说明：_("Rounding up/down")

### `BCD_TO_USINT`
- 库类型：`function`
- 输入：`IN: BYTE`
- 输出：`OUT: USINT`
- 筛选器：`BCD_TO_ANY`
- 说明：_("Conversion from BCD")

### `BCD_TO_UINT`
- 库类型：`function`
- 输入：`IN: WORD`
- 输出：`OUT: UINT`
- 筛选器：`BCD_TO_ANY`
- 说明：_("Conversion from BCD")

### `BCD_TO_UDINT`
- 库类型：`function`
- 输入：`IN: DWORD`
- 输出：`OUT: UDINT`
- 筛选器：`BCD_TO_ANY`
- 说明：_("Conversion from BCD")

### `BCD_TO_ULINT`
- 库类型：`function`
- 输入：`IN: LWORD`
- 输出：`OUT: ULINT`
- 筛选器：`BCD_TO_ANY`
- 说明：_("Conversion from BCD")

### `USINT_TO_BCD`
- 库类型：`function`
- 输入：`IN: USINT`
- 输出：`OUT: BYTE`
- 筛选器：`ANY_TO_BCD`
- 说明：_("Conversion to BCD")

### `UINT_TO_BCD`
- 库类型：`function`
- 输入：`IN: UINT`
- 输出：`OUT: WORD`
- 筛选器：`ANY_TO_BCD`
- 说明：_("Conversion to BCD")

### `UDINT_TO_BCD`
- 库类型：`function`
- 输入：`IN: UDINT`
- 输出：`OUT: DWORD`
- 筛选器：`ANY_TO_BCD`
- 说明：_("Conversion to BCD")

### `ULINT_TO_BCD`
- 库类型：`function`
- 输入：`IN: ULINT`
- 输出：`OUT: LWORD`
- 筛选器：`ANY_TO_BCD`
- 说明：_("Conversion to BCD")

### `DATE_AND_TIME_TO_TIME_OF_DAY`
- 库类型：`function`
- 输入：`IN: DT`
- 输出：`OUT: TOD`
- 说明：_("Conversion to time-of-day")

### `DATE_AND_TIME_TO_DATE`
- 库类型：`function`
- 输入：`IN: DT`
- 输出：`OUT: DATE`
- 说明：_("Conversion to date")

## Numerical

### `ABS`
- 库类型：`function`
- 输入：`IN: ANY_NUM`
- 输出：`OUT: ANY_NUM`
- 说明：_("Absolute number")

### `SQRT`
- 库类型：`function`
- 输入：`IN: ANY_REAL`
- 输出：`OUT: ANY_REAL`
- 说明：_("Square root (base 2)")

### `LN`
- 库类型：`function`
- 输入：`IN: ANY_REAL`
- 输出：`OUT: ANY_REAL`
- 说明：_("Natural logarithm")

### `LOG`
- 库类型：`function`
- 输入：`IN: ANY_REAL`
- 输出：`OUT: ANY_REAL`
- 说明：_("Logarithm to base 10")

### `EXP`
- 库类型：`function`
- 输入：`IN: ANY_REAL`
- 输出：`OUT: ANY_REAL`
- 说明：_("Exponentiation")

### `SIN`
- 库类型：`function`
- 输入：`IN: ANY_REAL`
- 输出：`OUT: ANY_REAL`
- 说明：_("Sine")

### `COS`
- 库类型：`function`
- 输入：`IN: ANY_REAL`
- 输出：`OUT: ANY_REAL`
- 说明：_("Cosine")

### `TAN`
- 库类型：`function`
- 输入：`IN: ANY_REAL`
- 输出：`OUT: ANY_REAL`
- 说明：_("Tangent")

### `ASIN`
- 库类型：`function`
- 输入：`IN: ANY_REAL`
- 输出：`OUT: ANY_REAL`
- 说明：_("Arc sine")

### `ACOS`
- 库类型：`function`
- 输入：`IN: ANY_REAL`
- 输出：`OUT: ANY_REAL`
- 说明：_("Arc cosine")

### `ATAN`
- 库类型：`function`
- 输入：`IN: ANY_REAL`
- 输出：`OUT: ANY_REAL`
- 说明：_("Arc tangent")

## Arithmetic

### `ADD`
- 库类型：`function`
- 输入：`IN1: ANY_NUM`，`IN2: ANY_NUM`
- 输出：`OUT: ANY_NUM`
- 可扩展：`true`
- 说明：_("Addition")

### `MUL`
- 库类型：`function`
- 输入：`IN1: ANY_NUM`，`IN2: ANY_NUM`
- 输出：`OUT: ANY_NUM`
- 可扩展：`true`
- 说明：_("Multiplication")

### `SUB`
- 库类型：`function`
- 输入：`IN1: ANY_NUM`，`IN2: ANY_NUM`
- 输出：`OUT: ANY_NUM`
- 说明：_("Subtraction")

### `DIV`
- 库类型：`function`
- 输入：`IN1: ANY_NUM`，`IN2: ANY_NUM`
- 输出：`OUT: ANY_NUM`
- 说明：_("Division")

### `MOD`
- 库类型：`function`
- 输入：`IN1: ANY_INT`，`IN2: ANY_INT`
- 输出：`OUT: ANY_INT`
- 说明：_("Remainder (modulo)")

### `EXPT`
- 库类型：`function`
- 输入：`IN1: ANY_REAL`，`IN2: ANY_NUM`
- 输出：`OUT: ANY_REAL`
- 说明：_("Exponent")

### `MOVE`
- 库类型：`function`
- 输入：`IN: ANY`
- 输出：`OUT: ANY`
- 说明：_("Assignment")

## Time

### `ADD`
- 库类型：`function`
- 输入：`IN1: TIME`，`IN2: TIME`
- 输出：`OUT: TIME`
- 说明：_("Time addition")

### `ADD_TIME`
- 库类型：`function`
- 输入：`IN1: TIME`，`IN2: TIME`
- 输出：`OUT: TIME`
- 说明：_("Time addition")

### `ADD`
- 库类型：`function`
- 输入：`IN1: TOD`，`IN2: TIME`
- 输出：`OUT: TOD`
- 说明：_("Time-of-day addition")+" "+_("DEPRECATED")

### `ADD_TOD_TIME`
- 库类型：`function`
- 输入：`IN1: TOD`，`IN2: TIME`
- 输出：`OUT: TOD`
- 说明：_("Time-of-day addition")

### `ADD`
- 库类型：`function`
- 输入：`IN1: DT`，`IN2: TIME`
- 输出：`OUT: DT`
- 说明：_("Date addition")+" "+_("DEPRECATED")

### `ADD_DT_TIME`
- 库类型：`function`
- 输入：`IN1: DT`，`IN2: TIME`
- 输出：`OUT: DT`
- 说明：_("Date addition")

### `MUL`
- 库类型：`function`
- 输入：`IN1: TIME`，`IN2: ANY_NUM`
- 输出：`OUT: TIME`
- 说明：_("Time multiplication")+" "+_("DEPRECATED")

### `MULTIME`
- 库类型：`function`
- 输入：`IN1: TIME`，`IN2: ANY_NUM`
- 输出：`OUT: TIME`
- 说明：_("Time multiplication")

### `SUB_TIME`
- 库类型：`function`
- 输入：`IN1: TIME`，`IN2: TIME`
- 输出：`OUT: TIME`
- 说明：_("Time subtraction")

### `SUB`
- 库类型：`function`
- 输入：`IN1: TIME`，`IN2: TIME`
- 输出：`OUT: TIME`
- 说明：_("Time subtraction")

### `SUB`
- 库类型：`function`
- 输入：`IN1: DATE`，`IN2: DATE`
- 输出：`OUT: TIME`
- 说明：_("Date subtraction")+" "+_("DEPRECATED")

### `SUB_DATE_DATE`
- 库类型：`function`
- 输入：`IN1: DATE`，`IN2: DATE`
- 输出：`OUT: TIME`
- 说明：_("Date subtraction")

### `SUB`
- 库类型：`function`
- 输入：`IN1: TOD`，`IN2: TIME`
- 输出：`OUT: TOD`
- 说明：_("Time-of-day subtraction")+" "+_("DEPRECATED")

### `SUB_TOD_TIME`
- 库类型：`function`
- 输入：`IN1: TOD`，`IN2: TIME`
- 输出：`OUT: TOD`
- 说明：_("Time-of-day subtraction")

### `SUB`
- 库类型：`function`
- 输入：`IN1: TOD`，`IN2: TOD`
- 输出：`OUT: TIME`
- 说明：_("Time-of-day subtraction")+" "+_("DEPRECATED")

### `SUB_TOD_TOD`
- 库类型：`function`
- 输入：`IN1: TOD`，`IN2: TOD`
- 输出：`OUT: TIME`
- 说明：_("Time-of-day subtraction")

### `SUB`
- 库类型：`function`
- 输入：`IN1: DT`，`IN2: TIME`
- 输出：`OUT: DT`
- 说明：_("Date and time subtraction")+" "+_("DEPRECATED")

### `SUB_DT_TIME`
- 库类型：`function`
- 输入：`IN1: DT`，`IN2: TIME`
- 输出：`OUT: DT`
- 说明：_("Date and time subtraction")

### `SUB`
- 库类型：`function`
- 输入：`IN1: DT`，`IN2: DT`
- 输出：`OUT: TIME`
- 说明：_("Date and time subtraction")+" "+_("DEPRECATED")

### `SUB_DT_DT`
- 库类型：`function`
- 输入：`IN1: DT`，`IN2: DT`
- 输出：`OUT: TIME`
- 说明：_("Date and time subtraction")

### `DIV`
- 库类型：`function`
- 输入：`IN1: TIME`，`IN2: ANY_NUM`
- 输出：`OUT: TIME`
- 说明：_("Time division")+" "+_("DEPRECATED")

### `DIVTIME`
- 库类型：`function`
- 输入：`IN1: TIME`，`IN2: ANY_NUM`
- 输出：`OUT: TIME`
- 说明：_("Time division")

## Bit-shift

### `SHL`
- 库类型：`function`
- 输入：`IN: ANY_BIT`，`N: ANY_INT`
- 输出：`OUT: ANY_BIT`
- 说明：_("Shift left")

### `SHR`
- 库类型：`function`
- 输入：`IN: ANY_BIT`，`N: ANY_INT`
- 输出：`OUT: ANY_BIT`
- 说明：_("Shift right")

### `ROR`
- 库类型：`function`
- 输入：`IN: ANY_NBIT`，`N: ANY_INT`
- 输出：`OUT: ANY_NBIT`
- 说明：_("Rotate right")

### `ROL`
- 库类型：`function`
- 输入：`IN: ANY_NBIT`，`N: ANY_INT`
- 输出：`OUT: ANY_NBIT`
- 说明：_("Rotate left")

## Bitwise

### `AND`
- 库类型：`function`
- 输入：`IN1: ANY_BIT`，`IN2: ANY_BIT`
- 输出：`OUT: ANY_BIT`
- 可扩展：`true`
- 说明：_("Bitwise AND")

### `OR`
- 库类型：`function`
- 输入：`IN1: ANY_BIT`，`IN2: ANY_BIT`
- 输出：`OUT: ANY_BIT`
- 可扩展：`true`
- 说明：_("Bitwise OR")

### `XOR`
- 库类型：`function`
- 输入：`IN1: ANY_BIT`，`IN2: ANY_BIT`
- 输出：`OUT: ANY_BIT`
- 可扩展：`true`
- 说明：_("Bitwise XOR")

### `NOT`
- 库类型：`function`
- 输入：`IN: ANY_BIT`
- 输出：`OUT: ANY_BIT`
- 说明：_("Bitwise inverting")

## Selection

### `SEL`
- 库类型：`function`
- 输入：`G: BOOL`，`IN0: ANY`，`IN1: ANY`
- 输出：`OUT: ANY`
- 说明：_("Binary selection (1 of 2)")

### `MAX`
- 库类型：`function`
- 输入：`IN1: ANY`，`IN2: ANY`
- 输出：`OUT: ANY`
- 可扩展：`true`
- 说明：_("Maximum")

### `MIN`
- 库类型：`function`
- 输入：`IN1: ANY`，`IN2: ANY`
- 输出：`OUT: ANY`
- 可扩展：`true`
- 说明：_("Minimum")

### `LIMIT`
- 库类型：`function`
- 输入：`MN: ANY`，`IN: ANY`，`MX: ANY`
- 输出：`OUT: ANY`
- 说明：_("Limitation")

### `MUX`
- 库类型：`function`
- 输入：`K: ANY_INT`，`IN0: ANY`，`IN1: ANY`
- 输出：`OUT: ANY`
- 可扩展：`true`
- 说明：_("Multiplexer (select 1 of N)")

## Comparison

### `GT`
- 库类型：`function`
- 输入：`IN1: ANY`，`IN2: ANY`
- 输出：`OUT: BOOL`
- 可扩展：`true`
- 说明：_("Greater than")

### `GE`
- 库类型：`function`
- 输入：`IN1: ANY`，`IN2: ANY`
- 输出：`OUT: BOOL`
- 可扩展：`true`
- 说明：_("Greater than or equal to")

### `EQ`
- 库类型：`function`
- 输入：`IN1: ANY`，`IN2: ANY`
- 输出：`OUT: BOOL`
- 可扩展：`true`
- 说明：_("Equal to")

### `LT`
- 库类型：`function`
- 输入：`IN1: ANY`，`IN2: ANY`
- 输出：`OUT: BOOL`
- 可扩展：`true`
- 说明：_("Less than")

### `LE`
- 库类型：`function`
- 输入：`IN1: ANY`，`IN2: ANY`
- 输出：`OUT: BOOL`
- 可扩展：`true`
- 说明：_("Less than or equal to")

### `NE`
- 库类型：`function`
- 输入：`IN1: ANY`，`IN2: ANY`
- 输出：`OUT: BOOL`
- 说明：_("Not equal to")

## Character string

### `LEN`
- 库类型：`function`
- 输入：`IN: STRING`
- 输出：`OUT: INT`
- 说明：_("Length of string")

### `LEFT`
- 库类型：`function`
- 输入：`IN: STRING`，`L: ANY_INT`
- 输出：`OUT: STRING`
- 说明：_("string left of")

### `RIGHT`
- 库类型：`function`
- 输入：`IN: STRING`，`L: ANY_INT`
- 输出：`OUT: STRING`
- 说明：_("string right of")

### `MID`
- 库类型：`function`
- 输入：`IN: STRING`，`L: ANY_INT`，`P: ANY_INT`
- 输出：`OUT: STRING`
- 说明：_("string from the middle")

### `CONCAT`
- 库类型：`function`
- 输入：`IN1: STRING`，`IN2: STRING`
- 输出：`OUT: STRING`
- 可扩展：`true`
- 说明：_("Concatenation")

### `CONCAT_DATE_TOD`
- 库类型：`function`
- 输入：`IN1: DATE`，`IN2: TOD`
- 输出：`OUT: DT`
- 说明：_("Time concatenation")

### `INSERT`
- 库类型：`function`
- 输入：`IN1: STRING`，`IN2: STRING`，`P: ANY_INT`
- 输出：`OUT: STRING`
- 说明：_("Insertion (into)")

### `DELETE`
- 库类型：`function`
- 输入：`IN: STRING`，`L: ANY_INT`，`P: ANY_INT`
- 输出：`OUT: STRING`
- 说明：_("Deletion (within)")

### `REPLACE`
- 库类型：`function`
- 输入：`IN1: STRING`，`IN2: STRING`，`L: ANY_INT`，`P: ANY_INT`
- 输出：`OUT: STRING`
- 说明：_("Replacement (within)")

### `FIND`
- 库类型：`function`
- 输入：`IN1: STRING`，`IN2: STRING`
- 输出：`OUT: INT`
- 说明：_("Find position")

## SMC_Basic function blocks

### `MC_Power`
- 库类型：`functionBlock`
- 输入：`Axis: AXIS_REF`，`Enable: BOOL`，`bRegulatorOn: BOOL`，`bDriveStart: BOOL`
- 输出：`Axis: AXIS_REF`，`Status: BOOL`，`bRegulatorRealState: BOOL`，`bDriveStartRealState: BOOL`，`Busy: BOOL`，`Error: BOOL`，`ErrorID: SMC_ERROR`

### `MC_ReadActualPosition`
- 库类型：`functionBlock`
- 输入：`Axis: AXIS_REF`，`Enable: BOOL`
- 输出：`Axis: AXIS_REF`，`Valid: BOOL`，`Busy: BOOL`，`Error: BOOL`，`ErrorID: SMC_ERROR`，`Position: LREAL`

### `MC_MoveAbsolute`
- 库类型：`functionBlock`
- 输入：`Axis: AXIS_REF`，`Execute: BOOL`，`Position: LREAL`，`Velocity: LREAL`，`Acceleration: LREAL`，`Deceleration: LREAL`，`Jerk: LREAL`，`Direction: MC_Direction`，`BufferMode: MC_BUFFER_MODE`
- 输出：`Axis: AXIS_REF`，`Done: BOOL`，`Busy: BOOL`，`Active: BOOL`，`CommandAborted: BOOL`，`Error: BOOL`，`ErrorID: SMC_ERROR`

### `MC_MoveRelative`
- 库类型：`functionBlock`
- 输入：`Axis: AXIS_REF`，`Execute: BOOL`，`Distance: LREAL`，`Velocity: LREAL`，`Acceleration: LREAL`，`Deceleration: LREAL`，`Jerk: LREAL`，`BufferMode: MC_BUFFER_MODE`
- 输出：`Axis: AXIS_REF`，`Done: BOOL`，`Busy: BOOL`，`Active: BOOL`，`CommandAborted: BOOL`，`Error: BOOL`，`ErrorID: SMC_ERROR`

### `MC_MoveAdditive`
- 库类型：`functionBlock`
- 输入：`Axis: AXIS_REF`，`Execute: BOOL`，`Distance: LREAL`，`Velocity: LREAL`，`Acceleration: LREAL`，`Deceleration: LREAL`，`Jerk: LREAL`
- 输出：`Axis: AXIS_REF`，`Done: BOOL`，`Busy: BOOL`，`CommandAborted: BOOL`，`Error: BOOL`，`ErrorID: BOOL`

### `MC_MoveSuperImposed`
- 库类型：`functionBlock`
- 输入：`Axis: AXIS_REF`，`Execute: BOOL`，`Abort: BOOL`，`Distance: LREAL`，`VelocityDiff: LREAL`，`Acceleration: LREAL`，`Deceleration: LREAL`，`Jerk: LREAL`
- 输出：`Axis: AXIS_REF`，`Done: BOOL`，`Busy: BOOL`，`CommandAborted: BOOL`，`Error: BOOL`，`ErrorID: SMC_ERROR`，`DistanceTravelled: LREAL`，`SuperImposedVelocity: LREAL`，`SuperImposedAcceleration: LREAL`

### `MC_MoveVelocity`
- 库类型：`functionBlock`
- 输入：`Axis: AXIS_REF`，`Execute: BOOL`，`Velocity: LREAL`，`Acceleration: LREAL`，`Deceleration: LREAL`，`Jerk: LREAL`，`Direction: MC_Direction`，`BufferMode: MC_BUFFER_MODE`
- 输出：`Axis: AXIS_REF`，`InVelocity: BOOL`，`Busy: BOOL`，`Active: BOOL`，`CommandAborted: BOOL`，`Error: BOOL`，`ErrorID: SMC_ERROR`

### `MC_PositionProfile`
- 库类型：`functionBlock`
- 输入：`Axis: AXIS_REF`，`TimePosition: MC_TP_REF`，`Execute: BOOL`，`ArraySize: INT`，`PositionScale: LREAL`，`Offset: LREAL`
- 输出：`Axis: AXIS_REF`，`TimePosition: MC_TP_REF`，`Done: BOOL`，`Busy: BOOL`，`CommandAborted: BOOL`，`Error: BOOL`，`ErrorID: SMC_ERROR`，`Section: INT`

### `MC_VelocityProfile`
- 库类型：`functionBlock`
- 输入：`Axis: AXIS_REF`，`TimeVelocity: MC_TV_REF`，`Execute: BOOL`，`ArraySize: INT`，`VelocityScale: LREAL`，`Offset: LREAL`
- 输出：`Axis: AXIS_REF`，`TimeVelocity: MC_TV_REF`，`Done: BOOL`，`Busy: BOOL`，`CommandAborted: BOOL`，`Error: BOOL`，`ErrorID: SMC_ERROR`，`Section: INT`

### `MC_ReadActualVelocity`
- 库类型：`functionBlock`
- 输入：`Axis: AXIS_REF`，`Enable: BOOL`
- 输出：`Axis: AXIS_REF`，`Valid: BOOL`，`Busy: BOOL`，`Error: BOOL`，`ErrorID: SMC_ERROR`，`Velocity: LREAL`

### `MC_AccelerationProfile`
- 库类型：`functionBlock`
- 输入：`Axis: AXIS_REF`，`TimeAcceleration: MC_TA_REF`，`Execute: BOOL`，`ArraySize: INT`，`AccelerationScale: LREAL`，`Offset: LREAL`
- 输出：`Axis: AXIS_REF`，`TimeAcceleration: MC_TA_REF`，`Done: BOOL`，`Busy: BOOL`，`CommandAborted: BOOL`，`Error: BOOL`，`ErrorID: SMC_ERROR`，`Section: INT`

### `MC_SetPosition`
- 库类型：`functionBlock`
- 输入：`Axis: AXIS_REF`，`Execute: BOOL`，`Position: LREAL`，`Mode: BOOL`
- 输出：`Axis: AXIS_REF`，`Done: BOOL`，`Busy: BOOL`，`Error: BOOL`，`ErrorID: SMC_ERROR`

### `MC_ReadParameter`
- 库类型：`functionBlock`
- 输入：`Axis: AXIS_REF`，`Enable: BOOL`，`ParameterNumber: DINT`
- 输出：`Axis: AXIS_REF`，`Valid: BOOL`，`Busy: BOOL`，`Error: BOOL`，`ErrorID: SMC_ERROR`，`Value: LREAL`

### `MC_ReadBoolParameter`
- 库类型：`functionBlock`
- 输入：`Axis: AXIS_REF`，`Enable: BOOL`，`ParameterNumber: DINT`
- 输出：`Axis: AXIS_REF`，`Valid: BOOL`，`Busy: BOOL`，`Error: BOOL`，`ErrorID: SMC_ERROR`，`Value: BOOL`

### `MC_WriteParameter`
- 库类型：`functionBlock`
- 输入：`Axis: AXIS_REF`，`Execute: BOOL`，`ParameterNumber: DINT`，`Value: LREAL`
- 输出：`Axis: AXIS_REF`，`Done: BOOL`，`Busy: BOOL`，`Error: BOOL`，`ErrorID: SMC_ERROR`

### `MC_WriteBoolParameter`
- 库类型：`functionBlock`
- 输入：`Axis: AXIS_REF`，`Execute: BOOL`，`ParameterNumber: DINT`，`Value: BOOL`
- 输出：`Axis: AXIS_REF`，`Done: BOOL`，`Busy: BOOL`，`Error: BOOL`，`ErrorID: SMC_ERROR`

### `MC_ReadActualTorque`
- 库类型：`functionBlock`
- 输入：`Axis: AXIS_REF`，`Enable: BOOL`
- 输出：`Axis: AXIS_REF`，`Valid: BOOL`，`Busy: BOOL`，`Error: BOOL`，`ErrorID: SMC_ERROR`，`Torque: LREAL`

### `MC_ReadStatus`
- 库类型：`functionBlock`
- 输入：`Axis: AXIS_REF`，`Enable: BOOL`
- 输出：`Axis: AXIS_REF`，`Valid: BOOL`，`Busy: BOOL`，`Error: BOOL`，`ErrorID: SMC_ERROR`，`Disabled: BOOL`，`Errorstop: BOOL`，`Stopping: BOOL`，`StandStill: BOOL`，`DiscreteMotion: BOOL`，`ContinuousMotion: BOOL`，`SynchronizedMotion: BOOL`，`Homing: BOOL`，`ConstantVelocity: BOOL`，`Accelerating: BOOL`，`Decelerating: BOOL`，`FBErrorOccured: BOOL`

### `MC_ReadAxisError`
- 库类型：`functionBlock`
- 输入：`Axis: AXIS_REF`，`Enable: BOOL`
- 输出：`Axis: AXIS_REF`，`Valid: BOOL`，`Busy: BOOL`，`Error: BOOL`，`ErrorID: SMC_ERROR`，`AxisError: BOOL`，`AxisErrorID: DWORD`，`SWEndSwitchActive: BOOL`

### `MC_Reset`
- 库类型：`functionBlock`
- 输入：`Axis: AXIS_REF`，`Execute: BOOL`
- 输出：`Axis: AXIS_REF`，`Done: BOOL`，`Busy: BOOL`，`Error: BOOL`，`ErrorID: SMC_ERROR`

### `MC_DigitalCamSwitch`
- 库类型：`functionBlock`
- 输入：`Axis: AXIS_REF`，`Switches: MC_CAMSWITCH_REF`，`Outputs: ARRAY`，`TrackOptions: ARRAY`，`Enable: BOOL`，`EnableMask: DWORD`，`TappetMode: MC_TAPPETMODE`
- 输出：`Axis: AXIS_REF`，`Switches: MC_CAMSWITCH_REF`，`Outputs: ARRAY`，`TrackOptions: ARRAY`

### `MC_TouchProbe`
- 库类型：`functionBlock`
- 输入：`Axis: AXIS_REF`，`TriggerInput: TRIGGER_REF`，`Execute: BOOL`，`WindowOnly: BOOL`，`FirstPosition: LREAL`，`LastPosition: LREAL`
- 输出：`Axis: AXIS_REF`，`TriggerInput: TRIGGER_REF`，`Done: BOOL`，`Busy: BOOL`，`Error: BOOL`，`ErrorID: SMC_ERROR`，`RecordedPosition: LREAL`，`CommandAborted: BOOL`

### `MC_AbortTrigger`
- 库类型：`functionBlock`
- 输入：`Axis: AXIS_REF`，`TriggerInput: TRIGGER_REF`，`Execute: BOOL`
- 输出：`Axis: AXIS_REF`，`TriggerInput: TRIGGER_REF`，`Done: BOOL`，`Busy: BOOL`，`Error: BOOL`，`ErrorID: SMC_ERROR`

### `MC_Stop`
- 库类型：`functionBlock`
- 输入：`Axis: AXIS_REF`，`Execute: BOOL`，`Deceleration: LREAL`，`Jerk: LREAL`
- 输出：`Axis: AXIS_REF`，`Done: BOOL`，`Busy: BOOL`，`Error: BOOL`，`ErrorID: SMC_ERROR`

### `MC_Halt`
- 库类型：`functionBlock`
- 输入：`Axis: AXIS_REF`，`Execute: BOOL`，`Deceleration: LREAL`，`Jerk: LREAL`
- 输出：`Axis: AXIS_REF`，`Done: BOOL`，`Busy: BOOL`，`CommandAborted: BOOL`，`Error: BOOL`，`ErrorID: SMC_ERROR`

### `MC_Home`
- 库类型：`functionBlock`
- 输入：`Axis: AXIS_REF`，`Execute: BOOL`，`Position: LREAL`
- 输出：`Axis: AXIS_REF`，`Done: BOOL`，`Busy: BOOL`，`CommandAborted: BOOL`，`Error: BOOL`，`ErrorID: SMC_ERROR`

### `MC_CamTableSelect`
- 库类型：`functionBlock`
- 输入：`Master: AXIS_REF`，`Slave: AXIS_REF`，`CamTable: MC_CAM_REF`，`Execute: BOOL`，`Periodic: BOOL`，`MasterAbsolute: BOOL`，`SlaveAbsolute: BOOL`
- 输出：`Master: AXIS_REF`，`Slave: AXIS_REF`，`CamTable: MC_CAM_REF`，`Done: BOOL`，`Busy: BOOL`，`Error: BOOL`，`ErrorID: SMC_ERROR`，`CamTableID: MC_CAM_ID`

### `MC_CamIn`
- 库类型：`functionBlock`
- 输入：`Master: AXIS_REF`，`Slave: AXIS_REF`，`Execute: BOOL`，`MasterOffset: LREAL`，`SlaveOffset: LREAL`，`MasterScaling: LREAL`，`SlaveScaling: LREAL`，`StartMode: MC_STARTMODE`，`CamTableID: MC_CAM_ID`，`VelocityDiff: LREAL`，`Acceleration: LREAL`，`Deceleration: LREAL`，`Jerk: LREAL`，`TappetHysteresis: LREAL`
- 输出：`Master: AXIS_REF`，`Slave: AXIS_REF`，`InSync: BOOL`，`Busy: BOOL`，`CommandAborted: BOOL`，`Error: BOOL`，`ErrorID: SMC_ERROR`，`EndOfProfile: BOOL`，`Tappets: SMC_TAPPETDATA`

### `MC_CamOut`
- 库类型：`functionBlock`
- 输入：`Slave: AXIS_REF`，`Execute: BOOL`
- 输出：`Slave: AXIS_REF`，`Done: BOOL`，`Busy: BOOL`，`Error: BOOL`，`ErrorID: SMC_ERROR`

### `MC_GearIn`
- 库类型：`functionBlock`
- 输入：`Master: AXIS_REF`，`Slave: AXIS_REF`，`Execute: BOOL`，`RatioNumerator: DINT`，`RatioDenominator: UDINT`，`Acceleration: LREAL`，`Deceleration: LREAL`，`Jerk: LREAL`，`BufferMode: MC_BUFFER_MODE`
- 输出：`Master: AXIS_REF`，`Slave: AXIS_REF`，`InGear: BOOL`，`Busy: BOOL`，`Active: BOOL`，`CommandAborted: BOOL`，`Error: BOOL`，`ErrorID: BOOL`

### `MC_GearOut`
- 库类型：`functionBlock`
- 输入：`Slave: AXIS_REF`，`Execute: BOOL`
- 输出：`Slave: AXIS_REF`，`Done: BOOL`，`Busy: BOOL`，`Error: BOOL`，`ErrorID: SMC_ERROR`

### `MC_GearInPos`
- 库类型：`functionBlock`
- 输入：`Master: AXIS_REF`，`Slave: AXIS_REF`，`Execute: BOOL`，`RatioNumerator: DINT`，`RatioDenominator: DINT`，`MasterSyncPosition: LREAL`，`SlaveSyncPosition: LREAL`，`MasterStartDistance: LREAL`，`BufferMode: MC_BUFFER_MODE`，`AvoidReversal: BOOL`
- 输出：`Master: AXIS_REF`，`Slave: AXIS_REF`，`StartSync: BOOL`，`InSync: BOOL`，`Busy: BOOL`，`Active: BOOL`，`CommandAborted: BOOL`，`Error: BOOL`，`ErrorID: SMC_ERROR`

### `MC_Phasing`
- 库类型：`functionBlock`
- 输入：`Master: AXIS_REF`，`Slave: AXIS_REF`，`Execute: BOOL`，`PhaseShift: LREAL`，`Velocity: LREAL`，`Acceleration: LREAL`，`Deceleration: LREAL`，`Jerk: LREAL`
- 输出：`Master: AXIS_REF`，`Slave: AXIS_REF`，`Done: BOOL`，`Busy: BOOL`，`CommandAborted: BOOL`，`Error: BOOL`，`ErrorID: SMC_ERROR`

### `SMC_TrackAxis`
- 库类型：`functionBlock`
- 输入：`Master: AXIS_REF`，`Slave: AXIS_REF`，`bExecute: BOOL`，`Velocity: LREAL`，`Acceleration: LREAL`，`Deceleration: LREAL`，`Jerk: LREAL`
- 输出：`Master: AXIS_REF`，`Slave: AXIS_REF`，`bBusy: BOOL`，`bCommandAborted: BOOL`，`bError: BOOL`，`iErrorID: SMC_ERROR`，`bInSync: BOOL`

### `SMC_TrackSetValues`
- 库类型：`functionBlock`
- 输入：`Axis: AXIS_REF`，`bExecute: BOOL`，`fSetPosition: LREAL`，`fSetVelocity: LREAL`，`fSetAcceleration: LREAL`，`fSetJerk: LREAL`，`Velocity: LREAL`，`Acceleration: LREAL`，`Deceleration: LREAL`，`Jerk: LREAL`，`SignalModuloPeriod: LREAL`
- 输出：`Axis: AXIS_REF`，`bBusy: BOOL`，`bCommandAborted: BOOL`，`bError: BOOL`，`iErrorID: SMC_ERROR`，`bInSync: BOOL`

### `MC_StartTrace`
- 库类型：`functionBlock`
- 输入：`Axis: AXIS_REF`，`bStartTrace: BOOL`
- 输出：无

### `SMC_MoveContinuousAbsolute`
- 库类型：`functionBlock`
- 输入：`Axis: AXIS_REF`，`Execute: BOOL`，`Position: LREAL`，`Velocity: LREAL`，`EndVelocity: LREAL`，`EndVelocityDirection: MC_Direction`，`Acceleration: LREAL`，`Deceleration: LREAL`，`Jerk: LREAL`，`Direction: MC_Direction`，`AdaptEndVelToAvoidOvershoot: BOOL`
- 输出：`Axis: AXIS_REF`，`InEndVelocity: BOOL`，`PositionReached: BOOL`，`Busy: BOOL`，`CommandAborted: BOOL`，`Error: BOOL`，`ErrorID: SMC_ERROR`

### `SMC_MoveContinuousRelative`
- 库类型：`functionBlock`
- 输入：`Axis: AXIS_REF`，`Execute: BOOL`，`Distance: LREAL`，`Velocity: LREAL`，`EndVelocity: LREAL`，`EndVelocityDirection: MC_Direction`，`Acceleration: LREAL`，`Deceleration: LREAL`，`Jerk: LREAL`，`AdaptEndVelToAvoidOvershoot: BOOL`
- 输出：`Axis: AXIS_REF`，`InEndVelocity: BOOL`，`DistanceTravelled: BOOL`，`Busy: BOOL`，`CommandAborted: BOOL`，`Error: BOOL`，`ErrorID: SMC_ERROR`

### `SMC_GetTappetValue`
- 库类型：`functionBlock`
- 输入：`Tappets: SMC_TAPPETDATA`，`iID: INT`，`bInitValue: BOOL`，`bSetInitValueAtReset: BOOL`
- 输出：`Tappets: SMC_TAPPETDATA`，`bTappet: BOOL`

## SMC_Basic functions

### `SMC_ReadAxisInfo`
- 库类型：`function`
- 输入：`AxisInfo: Axis_Ref_Info`，`Axis: AXIS_REF`
- 输出：`OUT: BOOL`，`AxisInfo: Axis_Ref_Info`

### `SMC_GetTimeNS`
- 库类型：`function`
- 输入：无
- 输出：`OUT: ULINT`

### `SMC_ParameterNumber_CoE`
- 库类型：`function`
- 输入：`index: UINT`，`subIndex: USINT`，`dataLength: USINT`
- 输出：`OUT: DINT`

## extra_library

### `SMC_ERROR`
- 库类型：`enum`
- 枚举成员：`SMC_NO_ERROR`

### `AXIS_REF`
- 库类型：`derived`
- 基础类型：`INT`
- 默认值：`-1`

### `MC_Direction`
- 库类型：`enum`
- 枚举成员：`fastest`，`current`，`positive`，`shortest`，`negative`

### `MC_BUFFER_MODE`
- 库类型：`enum`
- 枚举成员：`Aborting`，`Buffered`，`BlendingLow`，`BlendingPrevious`，`BlendingNext`，`BlendingHigh`

### `SMC_TP`
- 库类型：`struct`
- 结构体成员：
  - `delta_time: TIME`
  - `position: LREAL`

### `MC_TP_REF`
- 库类型：`struct`
- 结构体成员：
  - `Number_of_pairs: INT`，默认值：`0`
  - `IsAbsolute: BOOL`，默认值：`TRUE`
  - `MC_TP_Array: ARRAY [1..100] OF SMC_TP`

### `SMC_TV`
- 库类型：`struct`
- 结构体成员：
  - `delta_time: TIME`
  - `velocity: LREAL`

### `MC_TV_REF`
- 库类型：`struct`
- 结构体成员：
  - `Number_of_pairs: INT`
  - `IsAbsolute: BOOL`，默认值：`TRUE`
  - `MC_TV_Array: ARRAY [1..100] OF SMC_TV`

### `SMC_TA`
- 库类型：`struct`
- 结构体成员：
  - `delta_time: TIME`
  - `acceleration: LREAL`

### `MC_TA_REF`
- 库类型：`struct`
- 结构体成员：
  - `Number_of_pairs: INT`
  - `IsAbsolute: BOOL`，默认值：`true`
  - `MC_TA_Array: ARRAY [1..100] OF SMC_TA`

### `SMC_AXIS_STATE`
- 库类型：`enum`
- 枚举成员：`power_off`，`errorstop`，`stopping`，`standstill`，`discrete_motion`，`continuous_motion`，`synchronized_motion`，`homing`

### `AXIS_REF_SM3`
- 库类型：`struct`
- 结构体成员：
  - `nAxisState: SMC_AXIS_STATE`

### `MC_CAMSWITCH_TR`
- 库类型：`struct`
- 结构体成员：
  - `TrackNumber: INT`
  - `FirstOnPosition: LREAL`
  - `LastOnPosition: LREAL`
  - `AxisDirection: INT`
  - `CamSwitchMode: INT`
  - `Duration: TIME`
  - `bOn: BOOL`
  - `CounterOff: INT`

### `MC_CAMSWITCH_REF`
- 库类型：`struct`
- 结构体成员：
  - `NoOfSwitches: BYTE`
  - `CamSwitchPtr: ref_to MC_CAMSWITCH_TR`

### `MC_TRACK_TR`
- 库类型：`struct`
- 结构体成员：
  - `OnCompensation: LREAL`
  - `OffCompensation: LREAL`
  - `Hysteresi: LREAL`

### `MC_TAPPETMODE`
- 库类型：`enum`
- 枚举成员：`tp_mode_auto`，`tp_mode_demandposition`，`tp_mode_actualposition`

### `TRIGGER_REF`
- 库类型：`struct`
- 结构体成员：
  - `iTriggerNumber: INT`
  - `bFastLatching: BOOL`，默认值：`TRUE`
  - `bInput: BOOL`
  - `bActive: BOOL`

### `SMC_CAM_TYPE`
- 库类型：`enum`
- 枚举成员：`POLY`，`X`，`XY`，`XYVA`

### `MC_CAM_REF1`
- 库类型：`struct`
- 结构体成员：
  - `wCamStructID: WORD`，默认值：`16#DC34`
  - `byType: SMC_CAM_TYPE`
  - `byVarType: BYTE`
  - `xStart: LREAL`
  - `xEnd: LREAL`
  - `nElements: INT`
  - `nTappets: INT`
  - `pce: LWORD`
  - `pt: LWORD`
  - `dwTappetActiveBits: DWORD`
  - `byInterpolationQuality: BYTE`，默认值：`1`
  - `byCompatibilityMode: BYTE`
  - `bChangedOnline: BOOL`
  - `xPartofLM: BOOL`

### `MC_CAM_REF`
- 库类型：`derived`
- 基础类型：`UINT`
- 默认值：`0`

### `MC_STARTMODE`
- 库类型：`enum`
- 枚举成员：`absolute`，`relative`，`ramp_in`，`ramp_in_pos`，`ramp_in_neg`

### `MC_CAM_ID`
- 库类型：`struct`
- 结构体成员：
  - `pCT: LWORD`，默认值：`0`
  - `Periodic: BOOL`，默认值：`FALSE`
  - `MasterAbsolute: BOOL`，默认值：`FALSE`
  - `SlaveAbsolute: BOOL`，默认值：`FALSE`
  - `StartMaster: LREAL`，默认值：`0.0`
  - `EndMaster: LREAL`，默认值：`0.0`
  - `StartSlave: LREAL`，默认值：`0.0`
  - `EndSlave: LREAL`，默认值：`0.0`
  - `byCompatibilityMode: BYTE`，默认值：`0`

### `SMC_TAPPETDATA`
- 库类型：`struct`
- 结构体成员：
  - `pTaps: ARRAY [0..2] OF LWORD`
  - `dwCycleTime: DWORD`
  - `byChannels: BYTE`，默认值：`3`
  - `bRestart: BOOL`

### `Axis_Ref_Info`
- 库类型：`struct`
- 结构体成员：
  - `fActPosition: LREAL`，默认值：`0.0`
  - `dwActPosition: DWORD`
  - `fActVelocity: LREAL`，默认值：`0.0`
  - `fSetVelocity: LREAL`，默认值：`0.0`
  - `fActAcceleration: LREAL`，默认值：`0.0`
  - `fSetAcceleration: LREAL`，默认值：`0.0`
  - `fActJerk: LREAL`，默认值：`0.0`
  - `fSetJerk: LREAL`，默认值：`0.0`
  - `nAxisState: SMC_AXIS_STATE`
  - `nDirection: MC_Direction`
  - `fOffsetPosition: LREAL`
  - `fMarkPosition: LREAL`
  - `fSetPosition: LREAL`
  - `fSavePosition: LREAL`
  - `diSetPosition: DINT`
  - `diActPosition: DINT`
  - `dwLastPosition: DWORD`
  - `dwPosOffsetForResiduals: DWORD`
