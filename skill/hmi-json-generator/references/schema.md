# HMI JSON 严格 Schema

本文件是 HMI JSON 的唯一权威协议。所有字段大小写敏感。任何没有列出的字段都视为**禁止字段**。

## 1. 根节点 graph

根节点固定为：

```json
{
  "type": "graph",
  "id": "graph",
  "name": "screen",
  "size": {
    "width": 800,
    "height": 600
  },
  "backgroundColor": "#ffffff",
  "children": [],
  "htmlCode": {
    "codeHeadValue": "",
    "codeBodyValue": ""
  }
}
```

允许字段仅为：

```text
type
id
name
size
backgroundColor
children
htmlCode
```

`htmlCode` 为可选根级字段；出现时只能包含：

```json
{
  "codeHeadValue": "",
  "codeBodyValue": ""
}
```

规则：

- `codeHeadValue` 与 `codeBodyValue` 必须为字符串，可为空字符串。
- `htmlCode` 不属于 `children`。
- `htmlCode` 不包含 `type`、`id`、`name`、`size`、`position`、`visible`。
- `htmlCode` 内容中的换行、双引号、反斜杠必须按 JSON 字符串规则正确转义。
- 禁止根级 `width`、`height`、`x`、`y`、`background`、`version`、`style`。

## 2. HTML 页面与混合模式

### HTML 页面能力

已验证渲染器支持：

- 常见 HTML 页面结构、常见 HTML 标签及常见属性。
- `<!DOCTYPE html>`、`<html>`、`<head>`、`<body>` 完整文档结构。
- `<meta>`、`<title>`、`<style>`、`<link>` 等头部内容。
- 文本、布局、列表、表格、表单、按钮、图片、链接、iframe、SVG、Canvas 等正文内容。
- 内联 `<script>`。
- 外部 `<script src="..."></script>`。
- DOM 查询和修改。
- `onclick`、`addEventListener(...)` 等元素事件。
- 定时器，例如 `setInterval(...)`。
- `<iframe>` 嵌入页面。

常规 HTML 组织方式：

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <title>页面标题</title>
  <style>
    /* CSS */
  </style>
</head>
<body>
  <!-- 页面内容 -->

  <script>
    /* JavaScript */
  </script>
</body>
</html>
```

### 原生组件与 HTML 混合

已验证：

```text
graph.children 与 graph.htmlCode 可以在同一个 graph JSON 中并列存在，并分别由独立的渲染环境处理。
```

混合页面职责：

- 原生组件负责现场 PLC 变量绑定、设备启停、参数设定、报警确认、现场状态、仪表、趋势、输入控件、标准工艺图形和原生工艺动态。
- HTML 负责复杂展示、复杂报表、筛选表格、时间轴、SVG/Canvas 图形、复杂动画、摄像头、iframe、第三方 API、外部系统和网页化交互。
- 原生组件与 HTML 可以共同组成一个 HMI 页面。

混合页面渲染层规则：

- `graph.children` 是原生组件渲染层，`graph.htmlCode` 是 HTML 页面渲染层；二者不是同一图层上的两个区域。
- 两层分别拥有自己的画布或视口、坐标系、布局上下文、编辑环境和渲染结果。
- 生成、布局或校验原生组件层时，必须假设 HTML 层不存在；处理 HTML 层时，必须假设原生组件层不存在。
- 每层只依据自身需求正常使用本层的完整可用区域，不得参考另一层的坐标、尺寸或布局。
- 禁止为了另一层而避让、留白、缩小内容或预留区域；禁止建立左右、上下、侧边、页签或其他跨层空间分区。
- 不执行原生组件层与 HTML 页面层之间的包围盒碰撞、视觉遮挡、点击冲突或滚动冲突校验。
- 原生组件仅在原生组件层内进行边界、重叠、文字可读性和交互可用性检查。
- HTML 内容仅在 HTML 页面层内进行页面边界、内部重叠、文字可读性和交互可用性检查。
- 独立渲染层不代表数据互通；HTML 与原生组件之间的数据边界仍以本节“HTML 数据边界”为准。

### HTML 数据边界

当前 HTML 不支持：

- 读取现场 PLC 变量。
- 订阅现场 PLC 变量变化。
- 写入现场 PLC 变量。
- 读取或同步原生组件已绑定的 PLC 变量。
- 调用未确认的 HMI 宿主 API。
- 猜测 PLC JavaScript 接口。
- 伪造现场实时状态。

因此：

- HTML 不能被写成与原生组件 PLC 数据实时同步。
- HTML 不能读取、写入、订阅、同步或控制现场 PLC 变量。
- HTML 不得伪造 PLC 实时数值、设备实时状态、真实工艺流动或实时报警。

### 第三方数据与外部接口

HTML 可用于：

- 摄像头视频流。
- 第三方 API。
- MES、ERP、WMS、QMS 等业务系统。
- 云平台、数据库、地图、天气。
- 外部设备。
- 非现场 PLC。
- 外部网页或内部系统 iframe。
- 外部 JavaScript 图表、动画、表格或可视化库。

但只有用户明确提供以下信息后，才可生成真实接口调用：

```text
接口地址
请求方式
鉴权方式
请求参数
返回数据格式
视频流地址
访问说明
```

用户未提供真实接口配置时：

- 只能生成接口占位区域。
- 只能生成模拟数据。
- 只能生成静态设计预览。
- 不得猜测真实接口地址、Token、鉴权方法、数据字段或返回结构。
- 不得把模拟数据称为实时数据。

`iframe` 标签已验证支持，但外部页面是否允许嵌入由目标站点的 CSP、X-Frame-Options 或其他访问策略决定。

## 3. 通用节点规则

除 `node:tab` 外，每个原生可视组件必须含有：

```json
{
  "id": "唯一字符串",
  "name": "唯一字符串",
  "visible": true,
  "size": {
    "width": 100,
    "height": 100
  },
  "position": {
    "x": 0,
    "y": 0
  }
}
```

规则：

- 只能使用 `size.width`、`size.height`。
- 禁止 `w`、`h`。
- 禁止根级 `width`、`height`。
- 只能使用 `position.x`、`position.y`。
- 禁止组件根级 `x`、`y`。
- 默认 `name === id`。
- 每个组件 id 必须全局唯一。
- 色彩使用 `#RRGGBB`。
- 所有未确认变量使用空绑定。

## 4. 允许的 type 与意图

| 意图 | type |
|---|---|
| 圆、圆形 | `base:circle` |
| 矩形、面板底图 | `base:rect` |
| 椭圆 | `base:ellipse` |
| 自由多边形、等边三角形 | `base:shape` |
| 管道、开放折线、流向线 | `base:polyline` |
| 扇形 | `base:sector` |
| 状态指示灯 | `light` |
| 拨动/DIP/电源开关 | `open` / `dipSwitch` / `powerSwitch` |
| 常规按钮 | `button` |
| 复选框/紧凑开关 | `checkbox` / `switch` |
| 输入、数值输入、多行文本、下拉选择 | `input` / `numberInput` / `textarea` / `select` |
| 旋钮、半圆仪表、圆弧仪表 | `potentiometer360` / `meter180` / `meter360` |
| 标尺、滑条、进度条、圆弧进度 | `barDisplay` / `slider` / `progress` / `arc` / `arcSlider` |
| 标签、只读值 | `text` / `output` |
| 趋势、XY 图 | `trace` / `xyChart` |
| 表格、容器、页签 | `table` / `node:container` / `node:tabView` / `node:tab` |

禁止 type：

```text
rect
circle
ellipse
line
container
group
svg
path
```

以及其他未登记 type。

注意：

- HTML 内可以使用 `<svg>` 标签。
- 原生 JSON `children` 中不得使用 `type: "svg"`。

## 5. 层级规则

仅允许以下层级：

```text
graph.children → 常规组件、node:container、node:tabView
graph.htmlCode → codeHeadValue、codeBodyValue
node:tabView.children → node:tab
node:tab.children → 常规组件
```

规则：

- `node:container` 在已验证示例中仅作为根级背景/边框区域使用。
- 禁止生成 `node:container.children`。
- 普通组件必须与容器并列放入 `graph.children`。
- 容器应先于覆盖其视觉区域的组件出现，以作为背景层。
- `node:tabView.children` 只能包含 `node:tab`。
- `node:tab.children` 可包含常规组件。
- `node:tab` 不可再嵌套 `node:tab`。
- `graph.children` 与 `graph.htmlCode` 是根节点的并列字段，不构成父子包含、原生 z-index 叠放、跨层坐标避让或变量访问关系。

## 6. 类型字段白名单

下表列出每个 type 在通用字段之外允许的专有字段。不得增添其他字段。

| type | 专有允许字段 |
|---|---|
| `base:circle` | `backgroundColor`；`size` 可额外含 `r` |
| `base:rect` | `backgroundColor` |
| `base:ellipse` | `backgroundColor`；`size` 可额外含 `r` |
| `base:sector` | `backgroundColor`、`strokeColor`、`strokeWidth`、`startAngle`、`endAngle` |
| `base:shape` | 所有路径字段、`pointsSize`、`segments`、`points` |
| `base:polyline` | 所有路径字段、`pointsSize`、`segments`、`points` |
| `light` | `value`、`startColor`、`backgroundImage` |
| `open` | `value`、`rotate`、`backgroundImage`、`event` |
| `dipSwitch`、`powerSwitch` | `event`、`value`、`backgroundImage` |
| `button` | `event`、`value`、`text`、`backgroundColor`、`fontColor`、`fontSize`、`selectedBackgroundColor`、`selectedFontColor`、`selectedFontSize`、`borderWidth`、`borderColor`、`borderRadius` |
| `checkbox` | `event`、`text`、`value`、`borderWidth`、`borderColor`、`borderRadius`、`fontSize`、`fontColor` |
| `switch` | `event`、`value`、`borderWidth`、`color`、`backgroundColor`、`selectedBackgroundColor`、`controllerColor`、`selectedControllerColor`、`borderColor`、`borderRadius` |
| `input` | `backgroundColor`、`fontColor`、`borderColor`、`borderWidth`、`borderRadius`、`fontSize`、`value` |
| `output` | `backgroundColor`、`fontColor`、`borderColor`、`borderWidth`、`borderRadius`、`fontSize`、`textAlign`、`value` |
| `text` | `color`、`content`、`fontSize`、`borderWidth`、`borderColor`、`borderRadius`、`backgroundColor`、`mode`、`textAlign` |
| `textarea` | `backgroundColor`、`value`、`borderWidth`、`borderColor`、`borderRadius`、`fontSize`、`fontColor`、`textLength` |
| `numberInput` | `value`、`intLength`、`decimalLength`、`color`、`fontSize`、`fontColor`、`backgroundColor`、`selectedBackgroundColor`、`selectedFontColor`、`selectedFontSize` |
| `select` | `value`、`backgroundColor`、`color`、`fontSize`、`fontColor`、`borderColor`、`options` |
| `slider` | `backgroundColor`、`controllerColor`、`selectedBackgroundColor`、`value`、`startValue`、`endValue`、`fontSize`、`fontColor`、`isShowText` |
| `progress` | `backgroundColor`、`selectedBackgroundColor`、`value`、`startValue`、`endValue`、`fontSize`、`fontColor`、`isShowText` |
| `arc` | `value`、`startValue`、`endValue`、`backgroundColor`、`selectedBackgroundColor`、`color`、`fontSize`、`fontColor`、`rotateAngle`、`startAngle`、`endAngle`、`strokeWidth`、`isShowText` |
| `arcSlider` | `value`、`startValue`、`endValue`、`backgroundColor`、`selectedBackgroundColor`、`fontSize`、`fontColor`、`rotateAngle`、`startAngle`、`endAngle`、`strokeWidth`、`isShowText`、`sliderColor`、`sliderSize` |
| `potentiometer360` | `value`、`backgroundImage`、`splitNumber`、`startValue`、`endValue`、`pointerIcon` |
| `meter180`、`meter360` | `radius`、`value`、`startValue`、`endValue`、`splitNumber`、`startAngle`、`endAngle`、`axisLine.lineStyle.color`、`splitLine.show`、`splitLine.length`、`splitLine.lineStyle.color`、`splitLine.lineStyle.width`、`axisTick.show`、`axisTick.length`、`axisTick.splitNumber`、`axisTick.lineStyle.color`、`axisTick.lineStyle.width`、`axisLabel.show`、`axisLabel.distance`、`axisLabel.rotate`、`axisLabel.color`、`axisLabel.fontSize`、`axisLabel.formatter`、`detail.show`、`detail.color`、`detail.fontSize`、`detail.offsetCenterX`、`detail.offsetCenterY`、`detail.formatter`、`pointer.show`、`pointer.length`、`pointer.width`、`pointer.itemStyle.color`、`pointer.itemStyle.color.auto`、`axisLine.show`、`axisLine.lineStyle.width` |
| `barDisplay` | `barBackground`、`barColor`、`textColor`、`axisTickWidth`、`axisTickColor`、`interval`、`startValue`、`endValue`、`value` |
| `trace` | `color`、`text`、`backgroundColor`、`option` |
| `xyChart` | `color`、`text`、`backgroundColor`、`option` |
| `table` | `backgroundColor`、`fontSize`、`fontColor`、`borderWidth`、`borderColor`、`rowData` |
| `node:container` | `backgroundColor`、`borderWidth`、`borderColor`、`borderRadius`、`isClipping` |
| `node:tabView` | `backgroundColor`、`currentItem`、`borderWidth`、`borderColor`、`children` |
| `node:tab` | `type`、`id`、`name`、`titleText`、`visible`、`children` |

## 7. 绑定结构

### BOOL 控件

以下组件使用 BOOL 绑定：

```text
light
open
dipSwitch
powerSwitch
button
checkbox
switch
```

绑定结构：

```json
{
  "value": {
    "valueType": [
      "BOOL"
    ],
    "variableType": "",
    "variableName": "",
    "value": false
  }
}
```

以下写入型 BOOL 组件必须包含：

```json
{
  "event": "toggler"
}
```

适用组件：

```text
open
dipSwitch
powerSwitch
button
checkbox
switch
```

### 数值控件

数值组件使用：

```json
{
  "value": {
    "valueType": [
      "BYTE",
      "WORD",
      "DWORD",
      "LWORD",
      "SINT",
      "USINT",
      "INT",
      "UINT",
      "DINT",
      "UDINT",
      "LINT"
    ],
    "variableType": "",
    "variableName": "",
    "value": 10
  }
}
```

规则：

- `numberInput` 可以额外支持 `REAL`、`LREAL`。
- `numberInput.value.value` 保持字符串时，按已验证示例生成。
- `textarea.value.valueType` 固定为 `STRING`。
- `input`、`output`、`select` 使用其已验证示例的 `valueType: []`，除非后续有明确兼容类型协议。
- 用户未确认工程变量时，`variableName` 和 `variableType` 必须为空字符串。

## 8. 路径规则：base:shape 与 base:polyline

路径字段固定为：

```text
backgroundColor
strokeColor
strokeWidth
isDashed
dashLength
dashGap
dashGapColor
isDashFlowing
dashFlowDirection
dashFlowDistance
isImageFlowing
flowDirection
flowImage
flowImageSize
flowImageCount
flowImageDistance
flowImageDuration
pointsSize
segments
points
```

必须满足：

```text
points.length === segments.length
size.width === pointsSize.width
size.height === pointsSize.height
segments[0] === 1
segments[1..] 全部为 2
```

`points` 元素必须为：

```json
{
  "x": 0,
  "y": 0
}
```

规则：

- `points` 为相对组件 `position` 的局部坐标。
- `points` 不是 `[x, y]` 数组对。
- 水平线或垂直线应使用 `height: 1` 或 `width: 1`，避免零尺寸。
- `base:polyline` 默认是开放路径。
- 需要闭合轮廓时使用 `base:shape`。
- 不得猜测未定义的闭合路径命令。

流向枚举仅允许：

```json
{
  "dashFlowDirection": "forward"
}
```

或：

```json
{
  "dashFlowDirection": "backward"
}
```

以及：

```json
{
  "flowDirection": "forward"
}
```

或：

```json
{
  "flowDirection": "backward"
}
```

禁止：

```text
right
left
lineDash
animation
speed
duration
animationBinding
style
```

### 流动虚线最小条件

要启用已验证的虚线流动效果，至少需要：

```json
{
  "isDashed": true,
  "isDashFlowing": true,
  "dashFlowDirection": "forward"
}
```

规则：

- 未设置 `isDashed: true` 时，流动效果不生效。
- `dashLength`、`dashGap`、`dashGapColor`、`dashFlowDistance` 为可选视觉字段。
- `isImageFlowing` 及相关 `flowImage` 字段为可选图像流动字段。
- 不得使用 `speed`、`duration` 等 Schema 未定义字段调节原生流动速度。

## 9. 资源与特殊约束

已确认灯资源：

```text
Green
Gray
```

已确认默认流动图片：

```text
./img/radioCkecked.png
```

交叉约束：

```text
textarea.textLength === textarea.value.maxLength
select.value.value 必须命中 options[].value
node:tabView.currentItem 必须在 tab 索引范围内
数值预览值必须位于 [startValue, endValue]
```

## 10. 最终检查清单

输出前逐项确认：

1. 根节点完全符合第 1 节。
2. 每个原生 type 都在第 4 节白名单中。
3. 每个原生节点字段均在第 6 节白名单中。
4. `htmlCode` 仅使用 `codeHeadValue`、`codeBodyValue`。
5. 不存在 `w/h`、根级 `x/y/width/height`、`style`、`binding`、`background`、`textColor`、`foregroundColor`。
6. `text` 使用 `content` 与 `color`；`button` 使用 `text` 与 `fontColor`。
7. `node:container` 不含 `children`。
8. 所有 `points`、`segments`、`pointsSize` 满足第 8 节。
9. 所有未确认 PLC 变量名和变量类型为空字符串。
10. HTML 未读取、订阅、写入、同步或伪造现场 PLC/原生组件变量。
11. 第三方 API、摄像头、外部系统未提供接口配置时，HTML 只使用占位、模拟数据或设计预览。
12. 原生组件层与 HTML 页面层分别在假设另一层不存在的前提下进行自身的边界、可读性、可操作性和内部重叠检查；不得跨层参考坐标或尺寸，不得为另一层避让、留白、缩小或预留区域，也不执行跨层包围盒碰撞、遮挡、点击或滚动冲突检查。
13. 所有 ID 唯一；原生组件在原生组件层内坐标/尺寸合法且不越出画布，HTML 内容在 HTML 页面层内适配可见范围。
14. 输出是可解析 JSON，且不夹杂解释性文字。
