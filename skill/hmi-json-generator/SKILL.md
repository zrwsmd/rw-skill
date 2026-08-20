---
name: hmi-json-generator
description: 将工控/HMI中文自然语言需求转换为现有渲染器可加载的 graph JSON。
version: 1.1.0
language: zh-CN
output: json
---

# HMI JSON Generator Skill

## 目标

根据用户描述的工控业务画面生成一个合法 `graph` JSON。用户只需描述业务对象、功能、信息、视觉偏好及（可选）真实变量；不要要求用户提供坐标、尺寸、颜色或 JSON 字段。Skill 自动完成组件选型、信息分区、布局、尺寸和默认样式。

最终回答只能输出一个 JSON 对象，不包含 Markdown、解释、注释或省略号。

## 首要规则：变量绑定显式确认

1. 仅当用户明确给出项目中的真实变量完整路径，或上游变量目录同时提供变量名与兼容类型时，才填写 `value.variableName`。
2. 用户只说“启动、停止、复位、液位、温度、压力、运行状态”等业务语义时，所有组件必须使用 `"variableName": ""`；绝不推测 `PLC.Motor.StartCmd`、`PLC.Tank.Level` 等路径。
3. `valueType` 是组件可支持的数据类型声明，不能证明变量存在。无法确认变量存在或类型时，保持空绑定。
4. BOOL 写入/显示组件使用 `["BOOL"]`；整数数值组件用 `NUMERIC_INT_TYPES`；`numberInput` 用 `NUMERIC_REAL_TYPES`；`textarea` 使用 `"STRING"`。
5. 对按钮、开关等可写 BOOL 控件，只有已确认的可写 BOOL 变量才允许绑定；否则保留空绑定。

```text
NUMERIC_INT_TYPES = ["BYTE","WORD","DWORD","LWORD","SINT","USINT","INT","UINT","DINT","UDINT","LINT"]
NUMERIC_REAL_TYPES = NUMERIC_INT_TYPES + ["REAL","LREAL"]
```

## 根节点

默认画布为 800×600，白色或浅灰背景：

```json
{"type":"graph","id":"graph","name":"screen","size":{"width":800,"height":600},"backgroundColor":"#ffffff","children":[]}
```

## 生成流程

1. 理解业务场景，例如电机、水箱、温控、空压机、输送线。
2. 识别控制、状态、设定、读数、趋势和报警需求。
3. 按组件语义选择类型；不要仅按外观替换组件。
4. 自动采用清晰的工控布局：标题在顶部；主要控制放左侧或底部；关键状态靠近控制；主要工艺图/仪表位于中心或右侧；同类控件对齐且不重叠。
5. 根据 800×600 默认画布自动生成合理尺寸、间距和位置。用户明确画布、位置或视觉风格时再覆盖默认布局。
6. 为所有组件创建唯一 `id` 和同值 `name`；除 `graph` 外默认 `visible:true`。
7. 输出前按“校验清单”校验。

## 组件选择

| 用户意图 | 组件 type |
|---|---|
| 圆、圆形 | `base:circle` |
| 矩形、正方形、面板底板 | `base:rect` |
| 椭圆 | `base:ellipse` |
| 多边形、星形、等边三角形、封闭轮廓 | `base:shape` |
| 管道、开放折线、多线段 | `base:polyline` |
| 扇形、半圆扇形 | `base:sector` |
| 指示灯 | `light` |
| 拨动/DIP/电源开关 | `open` / `dipSwitch` / `powerSwitch` |
| 常规控制按钮 | `button` |
| 复选项/紧凑 Toggle | `checkbox` / `switch` |
| 通用值输入/精确数值输入/多行文本 | `input` / `numberInput` / `textarea` |
| 下拉枚举 | `select` |
| 数值旋钮 | `potentiometer360` |
| 半圆/圆弧仪表 | `meter180` / `meter360` |
| 标尺/线性可调/线性只读进度 | `barDisplay` / `slider` / `progress` |
| 圆弧可调/圆弧只读进度 | `arcSlider` / `arc` |
| 静态标签/只读变量值 | `text` / `output` |
| 一维趋势/XY关系 | `trace` / `xyChart` |
| 表格/容器/Tab页 | `table` / `node:container` / `node:tabView` |

## 关键区别

- `light` 只显示 BOOL 状态；`button`、`switch`、`checkbox`、`open`、`dipSwitch`、`powerSwitch` 是可操作 BOOL 控件并设置 `event:"toggler"`。
- `progress`、`arc` 是只读显示；`slider`、`arcSlider` 是用户设定。
- `trace` 的数据是 `[y1,y2,...]`；`xyChart` 数据是 `[[x1,y1],...]`。
- 用户说圆用 `base:circle`，说椭圆用 `base:ellipse`。
- 用户说等边三角形用 `base:shape`，宽度为 w 时高度为 `round(0.866*w,2)`，点集为 `[{x:w/2,y:0},{x:0,y:h},{x:w,y:h}]`，`segments:[1,2,2]`。

## 默认布局与样式

- 默认 800×600；外边距 32 px；组件间距至少 16 px。
- 用户不指定尺寸时采用 `references/component-defaults.json` 的默认值。
- 默认工业蓝灰样式：文字 `#333333`，主控件 `#409eff`，背景 `#ffffff` 或 `#f6f8fb`。
- 运行灯默认资源 `Green`，其他灯可使用 `Gray`；不得生成未知资源名。
- 路径仅使用已验证的直线段模式：`segments` 数量与 `points` 相同，首元素为 `1`，其余为 `2`。

## 数据与结构规则

- 数值量程未指定时使用 0–100，预览值 10，并保证预览值落在量程内。
- `numberInput.value.value` 保持字符串，例如 `"0"`。
- `textarea.value.maxLength` 必须等于 `textLength`。
- `select.value.value` 必须存在于 `options[].value`。
- `node:tabView.children` 只包含 `node:tab`；`currentItem` 是有效索引。
- 表格 `rowData` 是二维数组，单元格为 `{"variable":"","value":...}`；只有确认变量时才填 `variable`。
- 图表没有真实数据时仅使用设计预览数据，不宣称为生产数据；不得虚构实时绑定字段。

## 校验清单

- 输出为单一合法 JSON 对象，根节点是 `graph`。
- 所有 id 唯一，name 默认等于 id。
- 坐标、尺寸合法，默认画布下组件不重叠且不越界。
- 未明确提供或验证的变量，所有 `variableName` 必须是空字符串。
- BOOL 控件仅使用 BOOL 支持声明；数值值在量程内。
- 仅使用已确认的 type、字段和资源。

## 示例：无变量绑定

用户：“做一个电机控制画面，有启动、停止、复位按钮，显示运行和故障状态。”

即使按钮和灯有明确业务含义，在用户未提供真实工程变量时，必须生成：

```json
"value":{"valueType":["BOOL"],"variableType":"","variableName":"","value":false}
```

不要生成假设路径。后续用户提供例如 `GVL_Motor.bStopCmd` 且确认其为可写 BOOL 后，才可写入 `variableName`。
