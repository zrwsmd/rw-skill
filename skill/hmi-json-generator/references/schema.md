# HMI JSON 严格 Schema

本文件是 HMI JSON 的唯一权威协议。字段大小写敏感；任何未列出的 JSON 字段均为禁止字段。

## 1. 根节点 graph

根节点固定为：

```json
{
  "type": "graph",
  "id": "graph",
  "name": "screen",
  "size": {"width": 800, "height": 600},
  "backgroundColor": "#ffffff",
  "children": [],
  "htmlCode": {
    "codeHeadValue": "",
    "codeBodyValue": ""
  }
}
```

允许字段仅为：`type`、`id`、`name`、`size`、`backgroundColor`、`children`、`htmlCode`。

`htmlCode` 为可选根字段；出现时只能含有字符串字段 `codeHeadValue` 与 `codeBodyValue`。两者均可为空字符串。`htmlCode` 不属于 `children`，不含 `type`、`id`、`name`、`size` 或 `position`。

禁止根级 `width`、`height`、`x`、`y`、`background`、`version`、`style`。

## 2. HTML 页面规则

- 已验证渲染器支持常见 HTML 页面结构、常见 HTML 标签与常见属性，可按正常 HTML/CSS/JavaScript 网页方式生成。
- 已验证支持 `<!DOCTYPE html>`、`<html>`、`<head>`、`<body>` 的完整文档结构。
- `<head>` 可按常规 HTML 用法放置 `<meta>`、`<title>`、`<style>`、`<link>` 等内容。
- `<body>` 可按常规 HTML 用法放置页面结构、文本、表格、表单、按钮、图片、链接、iframe、SVG、canvas 等内容；脚本通常放在 body 末尾。
- 已验证支持内联 `<script>`、带 `src` 属性的外部 `<script src="..."></script>`、DOM 查询与修改、点击事件、`onclick`、`addEventListener(...)` 与定时器。
- `htmlCode.codeHeadValue` 与 `htmlCode.codeBodyValue` 都是 JSON 字符串；其中的换行、双引号、反斜杠必须正确转义。
- 使用完整 HTML 文档结构时，按用户或渲染器实际接收方式放置内容；未采用完整结构时，头部内容放入 `codeHeadValue`，可见内容与脚本放入 `codeBodyValue`。
- HTML 能力不等同于 HMI/PLC 数据接口。不得凭 HTML 猜测或虚构 PLC 变量、HMI 宿主 API 或现场实时状态。
- iframe 标签已验证支持，但第三方页面是否允许嵌入由目标站点策略决定。

## 3. 通用原生节点规则

除 `node:tab` 外，每个原生可视组件必须含有：

```json
"id": "唯一字符串",
"name": "唯一字符串",
"visible": true,
"size": {"width": 数字, "height": 数字},
"position": {"x": 数字, "y": 数字}
```

- 只能使用 `size.width`、`size.height`；禁止 `w/h` 及根级 `width/height`。
- 只能使用 `position.x`、`position.y`；禁止根级 `x/y`。
- 默认 `name === id`，每个 ID 必须全局唯一。
- 色彩为 `#RRGGBB`。
- 所有未确认变量使用空绑定。

## 4. 允许的 type 与意图

| 意图 | type |
|---|---|
| 圆、矩形、椭圆、扇形 | `base:circle` / `base:rect` / `base:ellipse` / `base:sector` |
| 自由封闭图形、开放路径 | `base:shape` / `base:polyline` |
| 状态指示灯 | `light` |
| 开关 | `open` / `dipSwitch` / `powerSwitch` / `checkbox` / `switch` |
| 常规按钮 | `button` |
| 输入 | `input` / `numberInput` / `textarea` / `select` |
| 仪表与进度 | `potentiometer360` / `meter180` / `meter360` / `barDisplay` / `slider` / `progress` / `arc` / `arcSlider` |
| 标签和只读值 | `text` / `output` |
| 图表与表格 | `trace` / `xyChart` / `table` |
| 容器与页签 | `node:container` / `node:tabView` / `node:tab` |

禁止 type：`rect`、`circle`、`ellipse`、`line`、`container`、`group`、`svg`、`path` 以及其他未登记 type。

## 5. 层级规则

```text
graph.children → 常规组件、node:container、node:tabView
graph.htmlCode → codeHeadValue、codeBodyValue
node:tabView.children → node:tab
node:tab.children → 常规组件
```

`node:container` 只作为根级背景或边框区域，禁止 `node:container.children`。普通组件应与容器并列放入 `graph.children`。

## 6. 类型字段白名单

| type | 专有允许字段 |
|---|---|
| `base:circle` | `backgroundColor`；`size` 可额外含 `r` |
| `base:rect` | `backgroundColor` |
| `base:ellipse` | `backgroundColor`；`size` 可额外含 `r` |
| `base:sector` | `backgroundColor`,`strokeColor`,`strokeWidth`,`startAngle`,`endAngle` |
| `base:shape`,`base:polyline` | `backgroundColor`,`strokeColor`,`strokeWidth`,`isDashed`,`dashLength`,`dashGap`,`dashGapColor`,`isDashFlowing`,`dashFlowDirection`,`dashFlowDistance`,`isImageFlowing`,`flowDirection`,`flowImage`,`flowImageSize`,`flowImageCount`,`flowImageDistance`,`flowImageDuration`,`pointsSize`,`segments`,`points` |
| `light` | `value`,`startColor`,`backgroundImage` |
| `open` | `value`,`rotate`,`backgroundImage`,`event` |
| `dipSwitch`,`powerSwitch` | `event`,`value`,`backgroundImage` |
| `button` | `event`,`value`,`text`,`backgroundColor`,`fontColor`,`fontSize`,`selectedBackgroundColor`,`selectedFontColor`,`selectedFontSize`,`borderWidth`,`borderColor`,`borderRadius` |
| `checkbox` | `event`,`text`,`value`,`borderWidth`,`borderColor`,`borderRadius`,`fontSize`,`fontColor` |
| `switch` | `event`,`value`,`borderWidth`,`color`,`backgroundColor`,`selectedBackgroundColor`,`controllerColor`,`selectedControllerColor`,`borderColor`,`borderRadius` |
| `input` | `backgroundColor`,`fontColor`,`borderColor`,`borderWidth`,`borderRadius`,`fontSize`,`value` |
| `output` | `backgroundColor`,`fontColor`,`borderColor`,`borderWidth`,`borderRadius`,`fontSize`,`textAlign`,`value` |
| `text` | `color`,`content`,`fontSize`,`borderWidth`,`borderColor`,`borderRadius`,`backgroundColor`,`mode`,`textAlign` |
| `textarea` | `backgroundColor`,`value`,`borderWidth`,`borderColor`,`borderRadius`,`fontSize`,`fontColor`,`textLength` |
| `numberInput` | `value`,`intLength`,`decimalLength`,`color`,`fontSize`,`fontColor`,`backgroundColor`,`selectedBackgroundColor`,`selectedFontColor`,`selectedFontSize` |
| `select` | `value`,`backgroundColor`,`color`,`fontSize`,`fontColor`,`borderColor`,`options` |
| `slider` | `backgroundColor`,`controllerColor`,`selectedBackgroundColor`,`value`,`startValue`,`endValue`,`fontSize`,`fontColor`,`isShowText` |
| `progress` | `backgroundColor`,`selectedBackgroundColor`,`value`,`startValue`,`endValue`,`fontSize`,`fontColor`,`isShowText` |
| `arc` | `value`,`startValue`,`endValue`,`backgroundColor`,`selectedBackgroundColor`,`color`,`fontSize`,`fontColor`,`rotateAngle`,`startAngle`,`endAngle`,`strokeWidth`,`isShowText` |
| `arcSlider` | `value`,`startValue`,`endValue`,`backgroundColor`,`selectedBackgroundColor`,`fontSize`,`fontColor`,`rotateAngle`,`startAngle`,`endAngle`,`strokeWidth`,`isShowText`,`sliderColor`,`sliderSize` |
| `potentiometer360` | `value`,`backgroundImage`,`splitNumber`,`startValue`,`endValue`,`pointerIcon` |
| `meter180`,`meter360` | `radius`,`value`,`startValue`,`endValue`,`splitNumber`,`startAngle`,`endAngle`,`axisLine`,`splitLine`,`axisTick`,`axisLabel`,`detail`,`pointer` |
| `barDisplay` | `barBackground`,`barColor`,`textColor`,`axisTickWidth`,`axisTickColor`,`interval`,`startValue`,`endValue`,`value` |
| `trace`,`xyChart` | `color`,`text`,`backgroundColor`,`option` |
| `table` | `backgroundColor`,`fontSize`,`fontColor`,`borderWidth`,`borderColor`,`rowData` |
| `node:container` | `backgroundColor`,`borderWidth`,`borderColor`,`borderRadius`,`isClipping` |
| `node:tabView` | `backgroundColor`,`currentItem`,`borderWidth`,`borderColor`,`children` |
| `node:tab` | `type`,`id`,`name`,`titleText`,`visible`,`children` |

## 7. 绑定结构

BOOL 控件使用：

```json
"value":{"valueType":["BOOL"],"variableType":"","variableName":"","value":false}
```

`open`、`dipSwitch`、`powerSwitch`、`button`、`checkbox`、`switch` 必须使用：

```json
"event":"toggler"
```

数值控件使用：

```json
"value":{"valueType":["BYTE","WORD","DWORD","LWORD","SINT","USINT","INT","UINT","DINT","UDINT","LINT"],"variableType":"","variableName":"","value":10}
```

`numberInput` 可额外支持 `REAL`、`LREAL`；`textarea.value.valueType` 固定为 `STRING`。

## 8. 路径与动态约束

`base:shape` 与 `base:polyline` 必须满足：

```text
points.length === segments.length
size.width === pointsSize.width
size.height === pointsSize.height
segments[0] === 1
segments[1..] 全部为 2
```

`points` 元素为对象 `{"x": 数字, "y": 数字}`（相对组件 position 的局部坐标），**不是** `[x, y]` 数组对；水平/垂直线取 `"height": 1`（或 `"width": 1`）避免零尺寸。（实测：数组对写法渲染器不识别。）

流动动画最小字段集（实测可动）：`isDashed: true` + `isDashFlowing: true` + `dashFlowDirection`；**省略 `isDashed` 时流动不生效**。`dashLength/dashGap/dashGapColor/dashFlowDistance` 及 `isImageFlowing` 全家桶均为可选装饰字段，不写也能动；实测 `dashFlowDistance` 不同取值无速度差异（渲染器疑似未实现调速）。

方向枚举仅允许：

```json
"dashFlowDirection":"forward" | "backward"
"flowDirection":"forward" | "backward"
```

禁止 `right`、`left`、`animation`、`speed`、`duration`、`animationBinding` 等未定义原生 JSON 字段。

## 9. 资源与交叉约束

- 已确认灯资源：`Green`、`Gray`。
- 已确认默认流动图片：`./img/radioCkecked.png`。
- `textarea.textLength === textarea.value.maxLength`。
- `select.value.value` 必须命中 `options[].value`。
- `node:tabView.currentItem` 必须位于 tab 索引范围。
- 数值预览值必须位于 `[startValue,endValue]`。

## 10. 最终检查

1. 根节点符合第 1 节。
2. 每个原生 type、字段、层级都在白名单内。
3. `htmlCode` 仅使用第 2 节允许字段，且字符串正确转义。
4. 不存在 `w/h`、根级 `x/y/width/height`、`style`、`binding`、`background`、`textColor`、`foregroundColor` 等禁止 JSON 字段。
5. `text` 使用 `content` 和 `color`；`button` 使用 `text` 和 `fontColor`。
6. 容器不含 `children`；路径、绑定、范围和资源均符合约束。
7. 未确认变量名和变量类型为空字符串。
8. 所有 ID 唯一；原生组件与 HTML 内容不越出画布。
9. 输出是可解析 JSON，且不夹杂解释性文字。
