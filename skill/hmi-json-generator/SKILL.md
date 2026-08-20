---
name: hmi-json-generator
description: 根据中文工控/HMI业务需求自动生成可渲染的 graph JSON。
version: 1.1.0
language: zh-CN
output: json
---

# HMI JSON Generator

## 目标

将用户用自然语言描述的工控/HMI画面需求，自动转换为单个合法 `graph` JSON。用户只需说明业务场景、功能、信息、视觉偏好及可选的真实变量；Skill 自动完成组件选型、界面分区、布局、尺寸、默认样式与合法 JSON 输出。

最终输出只能是单个 JSON 对象，不要输出 Markdown、说明、注释或省略号。

## 变量绑定规则

1. 只有用户明确提供项目中存在的变量完整路径，或上游变量目录同时确认变量名及兼容类型时，才可以填写 `value.variableName`。
2. 用户只描述“启动、停止、复位、液位、温度、压力、运行状态”等业务语义时，必须生成空绑定：

```json
"value":{"variableType":"","variableName":""}
```

3. 不得依据业务含义推测或生成 PLC 变量路径，例如 `PLC.Motor.StartCmd`、`PLC.Motor.StopCmd`、`PLC.Tank.Level`。
4. `valueType` 仅表示组件支持的数据类型，不能证明变量存在或可以绑定。
5. `button`、`switch`、`checkbox`、`open`、`dipSwitch`、`powerSwitch` 等写入型控件，只有在目标变量确认是可写 `BOOL` 时才可以绑定。
6. 变量路径无法解析、类型未知、类型不兼容或变量不可写时，也必须保持 `variableName:""`。

```text
NUMERIC_INT_TYPES = ["BYTE","WORD","DWORD","LWORD","SINT","USINT","INT","UINT","DINT","UDINT","LINT"]
NUMERIC_REAL_TYPES = NUMERIC_INT_TYPES + ["REAL","LREAL"]
```

## 根节点

默认生成 800×600 画布：

```json
{"type":"graph","id":"graph","name":"screen","size":{"width":800,"height":600},"backgroundColor":"#ffffff","children":[]}
```

## 生成流程

1. 解析业务对象及功能，例如电机控制、水箱监控、温控、空压机、输送线。
2. 识别控制、状态、设定、读数、报警、趋势和页面结构需求。
3. 根据组件语义选择组件，优先区分显示、操作、数值设定及趋势图。
4. 自动布局：顶部标题；控制放左侧或下方；状态紧邻控制；主要工艺图或仪表置于中心/右侧；保持对齐、不重叠并留出 16 px 以上间距。
5. 默认使用 800×600 和工业蓝灰配色。用户明确要求画布尺寸、位置、颜色、样式时优先采用用户要求。
6. 为每个组件生成唯一 `id` 和 `name`，默认 `name===id`，默认 `visible:true`。
7. 按“输出前校验”检查后，只输出 JSON。

## 组件选择

| 意图 | type |
|---|---|
| 圆、圆形 | `base:circle` |
| 矩形、面板、方块 | `base:rect` |
| 椭圆 | `base:ellipse` |
| 自由多边形、星形、等边三角形 | `base:shape` |
| 管道、折线、多线段 | `base:polyline` |
| 扇形、半圆扇形 | `base:sector` |
| 指示灯 | `light` |
| 普通、DIP、电源开关 | `open`、`dipSwitch`、`powerSwitch` |
| 启动、停止、复位等按钮 | `button` |
| 复选项、紧凑开关 | `checkbox`、`switch` |
| 通用输入、精确数字输入、多行文本 | `input`、`numberInput`、`textarea` |
| 下拉选择 | `select` |
| 旋钮设定 | `potentiometer360` |
| 半圆、圆弧仪表 | `meter180`、`meter360` |
| 标尺、可调滑条、只读进度 | `barDisplay`、`slider`、`progress` |
| 圆弧可调、圆弧进度 | `arcSlider`、`arc` |
| 标签、只读值 | `text`、`output` |
| 趋势、XY 图 | `trace`、`xyChart` |
| 表格、容器、选项卡 | `table`、`node:container`、`node:tabView` |

## 关键语义

- `light` 是只读 BOOL 状态显示；`button`、`switch`、`checkbox`、`open`、`dipSwitch`、`powerSwitch` 是可操作 BOOL 控件，使用 `event:"toggler"`。
- `progress`、`arc` 是只读数值显示；`slider`、`arcSlider` 是数值设定。
- `trace` 使用一维数据 `[y1,y2,...]`；`xyChart` 使用点对 `[[x1,y1],...]`。
- 用户明确说“圆”使用 `base:circle`，说“椭圆”使用 `base:ellipse`。
- 等边三角形使用 `base:shape`：宽度为 `w`，高度为 `round(0.866*w,2)`，点集 `[{x:w/2,y:0},{x:0,y:h},{x:w,y:h}]`，`segments:[1,2,2]`。
- `base:polyline` 可用于工艺管路及流向：虚线用 `isDashed:true`；虚线流动用 `isDashFlowing:true`。仅使用已确认的直线路径模式：首个 `segments` 值为 `1`，其余为 `2`。

## 默认规则

详细默认尺寸、支持类型和字段约束见 `references/component-defaults.json`。

- 未指定数值量程时，默认 `startValue:0`、`endValue:100`、预览值 `10`。
- 预览值必须位于量程内。
- `numberInput.value.value` 是字符串，例如 `"0"`。
- `textarea.textLength` 必须等于 `textarea.value.maxLength`。
- `select.value.value` 必须与某项 `options[].value` 相同。
- 运行灯图片默认 `Green`，未激活/故障预览可使用 `Gray`；不得创造未知资源名。
- 无真实趋势数据时可使用设计预览数据，但不得说它是生产数据，也不得虚构实时绑定字段。
- `node:tabView.children` 只允许 `node:tab`；`currentItem` 必须是有效索引。

## 输出前校验

- 输出为一个合法 JSON 对象，根节点是 `graph`。
- `id` 全局唯一，`name` 默认与 `id` 一致。
- 组件位置和尺寸合法，默认画布中不越界、不重叠。
- 未由用户明确提供或变量目录验证的变量，所有 `value.variableName` 必须为空字符串。
- BOOL 控件使用 BOOL 类型声明；数值初值在范围内；文本域、选择器和 Tab 满足对应约束。
- 仅生成已确认的组件 type、字段和资源。

## 空绑定示例

用户：“生成启动、停止、复位按钮。”

正确做法：按钮 `value` 必须包含：

```json
{"valueType":["BOOL"],"variableType":"","variableName":"","value":false}
```

而不是自动生成任何 PLC 变量路径。用户后续明确提供且确认类型兼容的变量后，才填写 `variableName`。
