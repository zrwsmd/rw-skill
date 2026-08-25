---
name: hmi-json-generator
description: 将中文工控/HMI需求编译为现有渲染器可加载的严格 graph JSON；支持原生组件和完整 HTML/CSS/JavaScript 页面渲染。
language: zh-CN
output: json
---

# HMI JSON Generator

## 任务

将用户的自然语言 HMI 需求编译为可直接导入的单个合法 `graph` JSON 画面。

支持两条实现路径：

- 原生 HMI 组件：`graph.children`。
- HTML 页面：根节点 `graph.htmlCode`，按正常 HTML/CSS/JavaScript 网页方式生成。

用户可明确指定工艺对象、功能、组件、HTML、CSS、JavaScript、iframe、外部脚本、变量、画布、位置、尺寸、布局、颜色、字体、主题或动态效果。用户的明确要求优先，但不得违反 Schema。

最终输出必须是单个合法 JSON 对象，且只能输出 JSON。禁止输出 Markdown、解释、注释、伪代码或省略号。

## 必须读取的参考文件

每次生成前，必须按顺序读取：

1. `references/schema.md`
   - 唯一权威 HMI JSON 协议，定义根节点、组件、字段、层级、绑定、资源、`htmlCode` 和校验规则。
2. `references/component-schema.json`
   - 机器可读的根字段、HTML 字段、原生组件白名单、路径、绑定和交叉校验约束。
3. `references/layout-style.md`
   - 布局安全、边界、普通元素避让、合法工艺重叠、动态元素与 HTML 内容布局规则。
4. `examples/valid-minimal.json`
   - 已验证的最小合法示例。

## 规则优先级

规则优先级从高到低：

1. 用户明确且不违反 Schema 的要求。
2. `references/schema.md`。
3. `references/component-schema.json`。
4. `references/layout-style.md`。
5. `examples/valid-minimal.json`。

用户可以覆盖默认尺寸、位置、颜色、主题、字体、布局、动态效果和预览值；但不能覆盖 Schema 中的 JSON 字段名、原生组件 type、嵌套结构、枚举值、资源约束和数据一致性约束。

未在 Schema 中明确允许的原生组件 type、JSON 字段、资源、层级、枚举值或绑定结构，一律禁止生成。

## 生成流程

1. 解析需求。
   - 提取工艺对象、控制、状态、设定、读数、报警、趋势、表格、页面结构、HTML需求、变量、动态效果和用户明确的视觉要求。
2. 选择实现路径。
   - 按“原生组件与 HTML 选择规则”选择原生组件、HTML 或经验证的混合方案。
3. 选择原生组件。
   - 仅使用 `schema.md` 登记的组件 type。
   - 状态显示优先使用 `light`、`output`、`progress`、`arc`、仪表等。
   - BOOL 操作优先使用 `button`、`switch`、`checkbox`、`open`、`dipSwitch`、`powerSwitch`。
   - 数值设定优先使用 `input`、`numberInput`、`slider`、`arcSlider`、`potentiometer360`。
   - 开放工艺路径使用 `base:polyline`；封闭自由图形使用 `base:shape`。
4. 规划布局。
   - 优先执行用户明确给出的画布、坐标、尺寸、排列和页面结构。
   - 未完整指定时，根据 `layout-style.md`、已验证默认值、画布、功能关系和内容长度动态安排。
   - 先规划功能区，再放置原生组件或 HTML 内容。
   - 空间不足时重新排列、分区、减少非关键预览元素或使用 `node:tabView`；不得让普通元素重叠。
5. 处理变量绑定和动态效果。
   - 严格遵守本文件的变量绑定和动态效果规则。
6. 执行校验。
   - 先执行 Schema、字段白名单、路径、层级和 HTML 字段校验。
   - 再执行边界、文本可读性、普通元素不重叠、合法工艺重叠、动态元素与 HTML 布局校验。
   - 全部通过后才输出 JSON。

## 原生组件与 HTML 选择规则

- 用户明确要求 HTML、CSS、JavaScript、网页布局、iframe、网页嵌入、复杂自定义视觉、复杂图表、复杂动画或网页化交互时，优先使用 `graph.htmlCode`。
- 需要 PLC 变量绑定、原生事件、标准输入控制、报警、趋势、已支持管线流动或原生组件编辑能力时，优先使用 `graph.children`。
- 用户未指定实现方式时，优先选择稳定、可维护、符合变量绑定需求且能清晰完成需求的路径。
- 标准 HMI 的原生趋势图、仪表、按钮、输入控件和已支持的管线流动，优先使用原生组件；原生组件无法满足的复杂展示、动画和网页化交互，可使用 HTML/CSS/JavaScript 或外部库。
- `children` 与 `htmlCode` 的混合使用，只有在 Schema 或已验证示例明确支持共同渲染且层级关系可控时才使用；未经验证不得假设二者可安全叠加、自动避让或相互绑定。

## HTML 页面规则

- 已验证支持常见 HTML 页面结构、常见 HTML 标签及常见属性；HTML 内容按正常网页开发方式生成。
- 已验证支持完整文档结构与常规位置安排：`<!DOCTYPE html>`、`<html>`、`<head>`、`<body>`。
- 在 `<head>` 中可按正常 HTML 用法放置 `<meta>`、`<title>`、`<style>`、`<link>` 等头部内容。
- 在 `<body>` 中可按正常 HTML 用法放置页面布局、标题、文本、列表、表格、表单、按钮、图片、链接、iframe、SVG、canvas 等可见内容；可在 body 末尾放置脚本。
- 已验证支持内联 `<script>`、带 `src` 属性的外部 `<script src="..."></script>`、DOM 查询和修改、元素点击事件、`onclick`、`addEventListener(...)` 与定时器。
- 可使用 HTML/CSS/JavaScript 生成当前 HTML 页面内的展示、交互和设计预览动态；复杂展示、图表或动画确有必要时，可加载外部 JavaScript 库。
- 外部脚本优先使用用户提供或已确认可访问的 HTTPS 地址。用户未提供外部库地址时，优先原生 HTML、CSS 和内联 JavaScript，不得为简单展示或简单交互无必要引入外部依赖。
- `iframe` 可用于用户明确要求的内部或外部网页嵌入。渲染器支持 iframe 标签不代表每个第三方地址均允许嵌入；目标站点拒绝时不得保证内容显示。
- `htmlCode.codeHeadValue` 与 `htmlCode.codeBodyValue` 必须是正确 JSON 转义的字符串。按完整 HTML 文档生成时，用户或渲染器实际使用方式优先；未采用完整文档时，头部内容放入 `codeHeadValue`，可见内容和脚本放入 `codeBodyValue`。
- HTML 页面不得伪造 PLC 实时数据、变量绑定或现场设备状态。没有已确认接口时，HTML 数值、动画和交互仅表示设计预览。
- HTML 不得调用未确认的 HMI 宿主 API、PLC 接口、父窗口接口、浏览器扩展接口或未确认的全局对象。

## 变量绑定规则

- 用户未提供真实工程变量名时，所有原生组件的 `value.variableName` 和 `value.variableType` 必须为 `""`。
- 不得根据启动、停止、复位、液位、温度、压力、转速、运行状态等业务语义猜测 PLC 变量路径。
- 只有用户明确提供完整变量路径，且变量类型已确认与组件兼容时，才可填写 `value.variableName`。
- `valueType` 仅表示组件支持的数据类型，不代表变量存在、可写或可绑定。
- BOOL 写入型组件只有绑定到已确认可写 BOOL 变量时，才允许写入该变量。
- 变量路径无法解析、类型未知、不兼容或不可写时，必须保持空绑定。
- HTML 不得自行定义、猜测或模拟 PLC/HMI 宿主的变量读写接口；只有 Schema 或已验证示例明确提供接口时才可使用。

## 默认值规则

- 所有常规原生组件默认 `visible:true`。
- 用户未指定画布尺寸时，使用 `schema.md` 或已验证示例中的默认画布。
- 用户未指定原生组件的尺寸、颜色、字体、边框、资源、量程或预览值时，使用该组件在已验证 JSON 示例或 `component-schema.json` 中已有的字段和值；不得自行发明资源名、字段名、主题体系或样式方案。
- 用户未指定位置时，按 `layout-style.md` 动态布局；不得把固定像素边距、固定间距或固定主题当成强制规则。
- 用户未提供趋势数据时，可使用已验证示例中的设计预览数据；不得称为实时生产数据，也不得杜撰实时绑定字段。
- 使用 HTML 时，用户未指定样式可按内容和画布自适应生成；不得声称其为系统默认主题或现场真实状态。

## 布局与重叠规则

- 用户明确指定位置、尺寸、排列、主题或颜色时优先执行，前提是 Schema 合法且关键内容可读、可操作。
- 所有原生组件与 HTML 可见内容必须位于画布或合法父节点范围内，避免关键文字、图片、描边或交互区域被裁剪。
- 除 `layout-style.md` 定义的合法工艺重叠外，普通组件包围盒不得相交。
- 文本不得覆盖按钮、输入框、输出框、开关、仪表、图表或表格。
- 容器仅作为根级背景或边框区域；普通组件与容器并列放在 `graph.children` 中，禁止 `node:container.children`。
- 合法重叠只用于表达设备结构、液面、工艺路径、流动方向、状态标识或容器背景层。
- HTML 页面内部可按正常网页布局合理嵌套和局部视觉重叠，但不得遮挡关键操作、关键读数、报警文字或画布外内容。

## 动态效果规则

- 当 `schema.md` 或 `component-schema.json` 明确支持相应字段，且动态效果能表达工艺状态、流向、设备运行、液位、进度、数值变化或需关注事件时，应优先配置动态效果。
- 持续动画仅用于具有明确工艺语义的状态、流向、进度、数值变化或异常强调；不对应明确工艺语义时默认保持静态。
- 当 Schema 支持流动动画且工艺对象具有物料、液体、气体、产品或能量传递语义时，默认优先生成动态预览；用户明确要求静态、禁用动画或指定其他动态方式时除外。
- 用户未说明流动方向时，应结合设备类型、连接关系、页面空间布局、路径几何和常见业务流程，生成合理且可修改的初始流动方向与动态预览。
- 初始方向只是设计推断；用户后续指定方向、运行条件、循环方式、双向流或变量绑定时，必须覆盖。
- 有真实变量且变量类型、路径、读写属性和业务含义已确认时，可按 Schema 允许方式绑定动态效果。
- 未确认变量时，不得填写猜测的变量路径、变量类型、动画绑定字段或其他会被解释为现场实时数据源的配置。
- 未确认变量不妨碍设计预览：Schema 支持且工艺语义明确时，可使用非绑定动画字段、静态预览值和初始方向生成可修改演示效果；其不表示设备现场运行、介质真实流动或数值实时变化。
- 报警、故障和未确认事件可使用有限强调效果，但必须同时提供可读文字、图标或状态信息；不得只依赖颜色或动画。
- HTML 中可使用 CSS 动画、内联 JavaScript、定时器或外部库实现设计预览动态；除非存在已确认的实时接口，否则不得表述为 PLC 或现场实时状态。
- 同一视图中应限制同时持续运行的动态元素；动态不得遮挡关键文字、关键读数或关键控制。
- 不得新增 Schema 未登记的原生动画字段、资源名、事件字段或变量绑定结构。

## 输出前硬校验

输出前必须逐项确认：

1. 输出是单个可解析 JSON 对象，根节点为 `graph`。
2. 根节点、所有原生组件 type、JSON 字段、层级和枚举值严格符合 `schema.md`。
3. `htmlCode` 仅在 `schema.md` 明确允许时生成，且只含允许字段。
4. 不包含未确认字段，例如 `w`、`h`、根级 `x`、`y`、`width`、`height`、`style`、`binding`、`background`、`textColor`、`foregroundColor`。
5. 不使用未登记的原生 type，例如 `rect`、`circle`、`line`、`container`、`group`、`svg`、`path`。
6. 所有组件 ID 全局唯一，默认 `name === id`。
7. 所有未确认变量均为空绑定；HTML 未使用猜测的实时数据接口或未确认宿主 API。
8. 用户明确要求的合法尺寸、位置、主题、颜色、字体、布局、HTML 与动态效果已优先执行。
9. 所有原生组件和 HTML 可见内容在画布或合法父节点范围内；普通组件之间不存在包围盒重叠。
10. 所有文字可读，未被组件、HTML 内容或画布边界遮挡。
11. `base:shape` 与 `base:polyline` 满足 points、segments、pointsSize 和方向枚举约束。
12. `node:container` 不含 `children`；`node:tabView.children` 仅含 `node:tab`，且 `currentItem` 有效。
13. `textarea.textLength === textarea.value.maxLength`；`select.value.value` 属于 `options[].value`；数值预览值位于对应范围内。
14. 所有原生动态字段、资源名、方向值和绑定结构均在 `schema.md` 中明确允许。
15. 每个持续动画具有工艺或交互语义；动态元素在全部可见状态下均不越界、不遮挡关键文字、关键读数或关键控制。
16. `htmlCode.codeHeadValue` 与 `htmlCode.codeBodyValue` 均为正确转义的 JSON 字符串；HTML、CSS、JavaScript、外部脚本和 iframe 均符合用户要求和已确认渲染能力。

如无法同时满足业务需求、用户要求、布局安全和 Schema，优先输出更简单但完全合法、可渲染且不重叠的 JSON。绝不输出猜测字段、猜测 type、猜测变量接口或未经验证的嵌套结构。
