# HMI JSON 严格 Schema

本文件是 HMI JSON 的唯一权威协议。所有字段大小写敏感。任何没有列出的字段都视为**禁止字段**。

## 1. 根节点 graph

根节点固定为：

```json
{
  "type":"graph",
  "id":"graph",
  "name":"screen",
  "size":{"width":800,"height":600},
  "backgroundColor":"#ffffff",
  "children":[]
}
```

允许字段仅为：`type`、`id`、`name`、`size`、`backgroundColor`、`children`。

禁止：根级 `width`、`height`、`x`、`y`、`background`、`version`、`style`。

## 2. 通用节点规则

除 `node:tab` 外，每个可视组件必须含有：

```json
"id":"唯一字符串",
"name":"唯一字符串",
"visible":true,
"size":{"width":数字,"height":数字},
"position":{"x":数字,"y":数字}
```

- 只能使用 `size.width`、`size.height`；禁止 `w/h` 及根级 `width/height`。
- 只能使用 `position.x`、`position.y`；禁止根级 `x/y`。
- 默认 `name === id`，每个 id 必须全局唯一。
- 色彩为 `#RRGGBB`。
- 所有未确认变量均使用空绑定。

## 3. 允许的 type 与意图

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

禁止 type：`rect`、`circle`、`ellipse`、`line`、`container`、`group`、`svg`、`path` 以及其他未登记 type。

## 4. 层级规则

仅允许下列层级：

```text
graph.children → 常规组件、node:container、node:tabView
node:tabView.children → node:tab
node:tab.children → 常规组件
```

`node:container` 在已验证示例中仅作为根级背景/边框区域使用；**禁止生成 `node:container.children`**，普通组件应与容器并列放入 `graph.children`，使用绝对位置覆盖在容器区域上。

## 5. 类型字段白名单

下表列出每个 type 在通用字段之外允许的专有字段。不得增添其他字段。

| type | 专有允许字段 |
|---|---|
| `base:circle` | `backgroundColor`；`size` 可额外含 `r` |
| `base:rect` | `backgroundColor` |
| `base:ellipse` | `backgroundColor`；`size` 可额外含 `r` |
| `base:sector` | `backgroundColor`,`strokeColor`,`strokeWidth`,`startAngle`,`endAngle` |
| `base:shape` | 所有路径字段、`pointsSize`,`segments`,`points` |
| `base:polyline` | 所有路径字段、`pointsSize`,`segments`,`points` |
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
| `meter180`,`meter360` | `radius`,`value`,`startValue`,`endValue`,`splitNumber`,`startAngle`,`endAngle`,`axisLine.lineStyle.color`,`splitLine.show`,`splitLine.length`,`splitLine.lineStyle.color`,`splitLine.lineStyle.width`,`axisTick.show`,`axisTick.length`,`axisTick.splitNumber`,`axisTick.lineStyle.color`,`axisTick.lineStyle.width`,`axisLabel.show`,`axisLabel.distance`,`axisLabel.rotate`,`axisLabel.color`,`axisLabel.fontSize`,`axisLabel.formatter`,`detail.show`,`detail.color`,`detail.fontSize`,`detail.offsetCenterX`,`detail.offsetCenterY`,`detail.formatter`,`pointer.show`,`pointer.length`,`pointer.width`,`pointer.itemStyle.color`,`pointer.itemStyle.color.auto`,`axisLine.show`,`axisLine.lineStyle.width` |
| `barDisplay` | `barBackground`,`barColor`,`textColor`,`axisTickWidth`,`axisTickColor`,`interval`,`startValue`,`endValue`,`value` |
| `trace` | `color`,`text`,`backgroundColor`,`option` |
| `xyChart` | `color`,`text`,`backgroundColor`,`option` |
| `table` | `backgroundColor`,`fontSize`,`fontColor`,`borderWidth`,`borderColor`,`rowData` |
| `node:container` | `backgroundColor`,`borderWidth`,`borderColor`,`borderRadius`,`isClipping` |
| `node:tabView` | `backgroundColor`,`currentItem`,`borderWidth`,`borderColor`,`children` |
| `node:tab` | `type`,`id`,`name`,`titleText`,`visible`,`children` |

## 6. 绑定结构

### BOOL 控件

`light`、`open`、`dipSwitch`、`powerSwitch`、`button`、`checkbox`、`switch` 使用：

```json
"value":{"valueType":["BOOL"],"variableType":"","variableName":"","value":false}
```

其中 `open`、`dipSwitch`、`powerSwitch`、`button`、`checkbox`、`switch` 必须含有：

```json
"event":"toggler"
```

### 数值控件

数值组件使用：

```json
"value":{"valueType":["BYTE","WORD","DWORD","LWORD","SINT","USINT","INT","UINT","DINT","UDINT","LINT"],"variableType":"","variableName":"","value":10}
```

`numberInput` 可以额外支持 `REAL`、`LREAL`，其 `value.value` 保持字符串。`textarea.value.valueType` 固定为 `"STRING"`。

`input`、`output`、`select` 使用其已验证示例的 `valueType:[]`，除非后续有该组件的明确兼容类型协议。

## 7. 路径规则：base:shape 与 base:polyline

路径字段固定为：

```text
backgroundColor, strokeColor, strokeWidth,
isDashed, dashLength, dashGap, dashGapColor,
isDashFlowing, dashFlowDirection, dashFlowDistance,
isImageFlowing, flowDirection, flowImage, flowImageSize,
flowImageCount, flowImageDistance, flowImageDuration,
pointsSize, segments, points
```

必须满足：

```text
points.length === segments.length
size.width === pointsSize.width
size.height === pointsSize.height
segments[0] === 1
segments[1..] 全部为 2
```

流向枚举仅允许：

```json
"dashFlowDirection":"forward" | "backward"
"flowDirection":"forward" | "backward"
```

禁止：`right`、`left`、`lineDash`、`animation`、`style`。

`base:polyline` 默认是开放路径。需要闭合轮廓时使用 `base:shape`，不要猜测未定义的闭合路径命令。

## 8. 资源与特殊约束

- 已确认灯资源：`Green`、`Gray`。
- 已确认默认流动图片：`./img/radioCkecked.png`。
- `textarea.textLength === textarea.value.maxLength`。
- `select.value.value` 必须命中 `options[].value`。
- `node:tabView.currentItem` 必须在 tab 索引范围内。
- 数值预览值必须位于 `[startValue,endValue]`。

## 9. 最终检查清单

在输出前逐项确认：

1. 根节点完全符合第 1 节。
2. 每个 type 在第 3 节白名单中。
3. 每个节点字段均在第 5 节白名单中。
4. 不存在 `w/h`、根级 `x/y/width/height`、`style`、`binding`、`background`、`textColor`、`foregroundColor`。
5. `text` 使用 `content` 与 `color`；`button` 使用 `text` 与 `fontColor`。
6. `node:container` 不含 `children`。
7. 所有 `points`、`segments`、`pointsSize` 满足第 7 节。
8. 所有未确认的变量名为空字符串。
9. 所有 ID 唯一、组件可见、坐标/尺寸合法且不越出画布。
10. 输出是可解析 JSON，且不夹杂任何解释性文字。
