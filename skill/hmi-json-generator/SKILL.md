---
name: hmi-json-generator
description: 将工控/HMI 用户的中文自然语言需求转换为可由现有图形渲染器直接渲染的 graph JSON。适用于画面设计、PLC 变量绑定占位、基础图形、控件、仪表、图表、表格、容器和选项卡。
version: 1.0.0
language: zh-CN
output: json
---

# HMI JSON Generator Skill

## 目标

将用户的自然语言 HMI 需求转换为**单个合法 JSON 对象**。输出根节点必须是 `graph`，组件位于根节点或允许嵌套的节点的 `children` 中。最终输出只能包含 JSON，不得使用 Markdown 代码块、解释、注释或省略号。

本 Skill 只使用本文档已确认的组件类型、字段和资源名。未确认的资源、字段、路径命令或运行时绑定协议不得凭空编造。

## 工作流程

1. 解析用户需求：画布、组件、数量、层级、文本、位置、尺寸、颜色、状态、变量、数据范围、图表数据和交互方式。
2. 为每项需求选择最贴合语义的组件类型。优先区分显示/输入/切换/设定/趋势/结构容器。
3. 生成 JSON：创建根 `graph`；为每个组件生成唯一 `id` 和同值 `name`；根据类型填充必需字段及安全默认值。
4. 布局：遵守明确坐标；对于相对位置使用画布区域换算；未指定位置时使用不重叠网格布局。
5. 校验：JSON 合法、ID 唯一、子组件归属正确、数值范围合理、点集坐标合法、组件不超出画布。
6. 只输出最终 JSON。

## 根节点

始终以如下结构开始。用户未指定时使用 800×600、白色背景：

```json
{
  "type": "graph",
  "id": "graph",
  "name": "screen",
  "size": { "width": 800, "height": 600 },
  "backgroundColor": "#ffffff",
  "children": []
}
```

## 全局规则

- `id` 格式：`<type-safe>_<5位随机小写字母或数字>`；`name` 默认与 `id` 相同。`base:circle` 等含冒号的 type 在 ID 中保留冒号，例如 `base:circle_a1b2c`。
- `visible` 默认 `true`。
- 颜色使用 `#RRGGBB`，保留用户指定的合法颜色。默认画布为 `#ffffff`，默认文字/描边为 `#000000`。
- `position` 是组件在所属画布/父节点坐标空间的左上角：`{"x": number,"y": number}`。
- 没有给出尺寸时，根据组件默认尺寸；默认布局的间距至少 16 px。
- 如果用户给出绝对点坐标且需要 `base:polyline` / `base:shape`，用点集的最小 x、最小 y 作为 `position`，将 `points` 转为局部坐标；`size`、`pointsSize` 为局部点集包围盒。
- 坐标和尺寸可为小数；避免无必要的超长浮点数，优先整数或最多两位小数。
- 对要求变量绑定的控件，写入 `value.variableName`；`variableType` 在用户未提供协议时写 `""`。
- 不知道变量数据类型时：BOOL 控件用 `["BOOL"]`；整数数值控件用 `NUMERIC_INT_TYPES`；支持浮点的数字输入用 `NUMERIC_REAL_TYPES`；字符串文本域用 `"STRING"`；其他示例定义为空数组时保留 `[]`。
- `value.value` 作为预览/初值，必须在用户提供的量程内；未提供时按组件默认值。
- 不要杜撰 PLC 变量名、趋势生产数据、图像资源名或图表扩展字段。用户没给变量时使用空字符串；用户没给数据时保留相应默认预览数据。

```text
NUMERIC_INT_TYPES = ["BYTE","WORD","DWORD","LWORD","SINT","USINT","INT","UINT","DINT","UDINT","LINT"]
NUMERIC_REAL_TYPES = NUMERIC_INT_TYPES + ["REAL","LREAL"]
```

## 布局规则

- “左/中/右”分别表示大约 15%/50%/85% 画布宽度区域；“上/中/下”分别表示大约 15%/50%/85% 画布高度区域。组件位置应结合自身尺寸且不越界。
- “居中”使组件中心对齐画布中心；“右侧”按右边距 24 px；“底部”按下边距 24 px。
- “并排”从左到右，间距 16 px；“上下排列”从上到下，间距 12 px。
- 未给坐标也未给布局词：从 `(40, 40)` 起按网格排布。避免重叠，超过右边界时换行。
- 父容器或 Tab 内部组件的坐标默认相对于父节点左上角；若目标运行时不支持该坐标规则，必须以运行时约定为准。

## 组件选择表

| 用户意图 | type |
|---|---|
| 圆、圆形 | `base:circle` |
| 矩形、正方形、面板底板 | `base:rect` |
| 椭圆 | `base:ellipse` |
| 自由多边形、星形、任意封闭轮廓、等边三角形 | `base:shape` |
| 管道、开放折线、多线段 | `base:polyline` |
| 扇形、半圆扇形、饼图扇区 | `base:sector` |
| 指示灯、运行灯、故障灯 | `light` |
| 拨动开关 | `open` |
| DIP/操纵杆开关 | `dipSwitch` |
| 电源开关 | `powerSwitch` |
| 启动/停止/复位按钮 | `button` |
| 复选项 | `checkbox` |
| 紧凑 Toggle | `switch` |
| 通用输入值 | `input` |
| 精确数字/小数输入 | `numberInput` |
| 多行字符串输入 | `textarea` |
| 下拉枚举选择 | `select` |
| 旋钮/电位器设定 | `potentiometer360` |
| 半圆仪表 | `meter180` |
| 圆弧/圆形仪表 | `meter360` |
| 标尺/液位条 | `barDisplay` |
| 水平滑动设定 | `slider` |
| 水平只读进度 | `progress` |
| 圆弧只读进度 | `arc` |
| 圆弧可调滑块 | `arcSlider` |
| 静态文字/标签/标题 | `text` |
| 只读变量读数 | `output` |
| 一维趋势曲线 | `trace` |
| XY 坐标关系图 | `xyChart` |
| 二维表格 | `table` |
| 面板/分组容器 | `node:container` |
| 多页签 | `node:tabView`，内部使用 `node:tab` |

### 相近组件的强制区分

- 只读状态灯使用 `light`；能被用户操作的 BOOL 使用 `button` / `switch` / `checkbox` / `open` / `dipSwitch` / `powerSwitch`。
- 只读线性进度用 `progress`；拖动调节用 `slider`。
- 只读圆弧进度用 `arc`；拖动调节用 `arcSlider`。
- 通用值输入用 `input`；含整数/小数位数约束的精确数值输入用 `numberInput`。
- 一维 y 序列用 `trace`；显式 `[x,y]` 点对用 `xyChart`。
- 用户明确说“圆”用 `base:circle`，明确说“椭圆”用 `base:ellipse`，即使宽高恰好相等也不替换类型。

## 类型模板与字段

详细可复制 JSON 模板位于 `references/component-templates.json`。严格按模板字段生成。

### 基础图形

- `base:circle`：`size={width,height,r}`、`backgroundColor`、`position`。
- `base:rect`：`size={width,height}`、`backgroundColor`、`position`。
- `base:ellipse`：`size={width,height,r}`、`backgroundColor`、`position`。
- `base:sector`：`size={width,height}`、`backgroundColor`、`strokeColor`、`strokeWidth`、`startAngle`、`endAngle`、`position`。
- `base:shape` 和 `base:polyline`：使用 `PATH_STYLE_FIELDS` 加 `size`、`pointsSize`、`segments`、`points`、`position`。

`PATH_STYLE_FIELDS`：`backgroundColor`、`strokeColor`、`strokeWidth`、`isDashed`、`dashLength`、`dashGap`、`dashGapColor`、`isDashFlowing`、`dashFlowDirection`、`dashFlowDistance`、`isImageFlowing`、`flowDirection`、`flowImage`、`flowImageSize`、`flowImageCount`、`flowImageDistance`、`flowImageDuration`。

安全默认值：白色填充、黑色 4 px 描边、非虚线、非流动；流动图片默认 `./img/radioCkecked.png`，仅在启用图像流动时使用。

### 等边三角形

使用 `base:shape`。边长/宽度为 `w` 时，高度 `h=round(0.866*w,2)`；点集：`[{x:w/2,y:0},{x:0,y:h},{x:w,y:h}]`，`segments:[1,2,2]`，且 `size` 与 `pointsSize` 为 `{width:w,height:h}`。

### 路径安全规则

- 标准直线点集模板：`segments` 长度必须与 `points` 长度一致，首项为 `1`，其余项为 `2`。
- 只生成已验证的直线路径模式，不生成未定义的贝塞尔、弧线或闭合命令。
- 点必须满足 `0 <= x <= pointsSize.width` 且 `0 <= y <= pointsSize.height`。
- `base:polyline` 默认是开放路径；若用户明确要求闭合，优先用 `base:shape`，不要依赖未知的闭合 segment 语义。

### BOOL 控件

`light`、`open`、`dipSwitch`、`powerSwitch`、`button`、`checkbox`、`switch` 的绑定均使用：

```json
{"valueType":["BOOL"],"variableType":"","variableName":"","value":false}
```

`open`、`dipSwitch`、`powerSwitch`、`button`、`checkbox`、`switch` 都应设置 `event:"toggler"`。`light` 不设置 toggler。

- `open` 额外带 `rotate:{"a":0,"x":0,"y":0}`。
- 灯的资源仅使用已知的 `Green` 或 `Gray`，默认 `Green`；开关资源默认 `Gray`。

### 数值控件

- `potentiometer360`：可交互旋钮，整数值，`startValue/endValue/splitNumber/pointerIcon`。
- `meter180` / `meter360`：只读仪表。色带格式为 `[[0.3,"#67e0e3"],[0.7,"#37a2da"],[1,"#fd666d"]]`。`meter360` 额外有 `startAngle/endAngle`。
- `barDisplay`：单值、带刻度线性显示。
- `slider`：可交互线性数值设定。
- `progress`：只读线性数值显示。
- `arc`：只读圆弧显示。
- `arcSlider`：可交互圆弧调节，额外有 `sliderColor/sliderSize`。
- 数值量程未说明时默认 0–100，初值 10；初值必须在量程内。

### 文本、输入与选择

- `input`：有 `numberRadix:10`，用于通用输入。
- `output`：只读数值；有 `textAlign`。
- `text`：静态 `content`，不含 `value`。
- `numberInput`：`value.value` 是字符串；默认 `"0"`，`intLength:2`，`decimalLength:2`。
- `textarea`：`valueType:"STRING"`；`value.maxLength` 与根级 `textLength` 必须一致。
- `select`：`options` 为 `[{"name":string,"value":number|string}]`；当前 `value.value` 必须存在于 options 中。

### 图表、表格和结构

- `trace.option.series[].data` 为一维 y 值数组。用户未提供数据时使用 `[150,230,224,218,135,147]` 作为设计预览，不将其表述为真实数据。
- `xyChart.option.series[].data` 为 `[x,y]` 数组。用户未提供数据时使用 `[[1,3],[2,4]]`。
- `table.rowData` 为二维数组；每个单元格为 `{"variable":"","value":...}`。第一行通常为表头。
- `node:container` 可有背景、边框、圆角、裁剪和 `children`。
- `node:tabView.children` 只能为 `node:tab`；每个 tab 均包含唯一 `id`、唯一 `name`、`titleText`、`visible` 和 `children`。`currentItem` 必须是有效索引。

## 默认尺寸

| type | 默认宽×高 |
|---|---|
| `base:circle`, `base:rect` | 100×100 |
| `base:ellipse` | 100×60 |
| `light`, `dipSwitch`, `powerSwitch` | 100×100 |
| `open` | 78×104 |
| `button` | 88×32 |
| `input`, `output` | 100×34 |
| `text` | 70×24 |
| `checkbox` | 120×24 |
| `switch` | 58×24 |
| `textarea` | 100×50 |
| `numberInput`, `select` | 150×30 / 150×24 |
| `slider`, `progress` | 200×10 |
| `arc`, `arcSlider` | 100×100 |
| `potentiometer360` | 200×200 |
| `meter180` | 252×139 |
| `meter360` | 300×300 |
| `barDisplay` | 350×50 |
| `trace`, `xyChart` | 200×200 |
| `table` | 150×90 |
| `node:container` | 150×150 |
| `node:tabView` | 254×254 |

## 输出前校验清单

- 输出是单个可解析 JSON 对象，不含注释或 Markdown。
- 根节点是 `graph`，具有 `id/name/size/backgroundColor/children`。
- 全部 `id` 唯一；默认 `name === id`。
- `position`、`size` 数值合法；组件没有越过画布或父节点边界。
- BOOL 控件使用 BOOL value；数值组件使用数值类型集合；文本域用 STRING。
- 所有数值初值位于 `[startValue,endValue]` 内。
- `select.value.value` 属于 `options[].value`。
- `textarea.textLength === textarea.value.maxLength`。
- `segments.length === points.length`，首段为 1，其余为 2。
- `node:tabView` 仅含 `node:tab`；`currentItem` 索引有效。
- 仅使用已确认字段、资源和 type；不要添加猜测字段。

## 示例

用户：“创建一个电机控制面板：左侧放启动和停止按钮，运行灯绑定 `PLC.Motor.Run`，故障灯绑定 `PLC.Motor.Fault`；右侧用半圆仪表显示转速，量程 0 到 3000。”

生成策略：创建 `node:container`；内部放两个 `button`、两个 `light`、一个 `meter180`。按钮 BOOL 绑定留空，灯绑定对应变量，仪表绑定在用户明确变量后填写；否则变量名留空但量程设为 0–3000。使用不会重叠的布局。
