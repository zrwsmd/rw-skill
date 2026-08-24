---
name: hmi-json-generator
description: 将中文工控/HMI需求编译为现有渲染器可加载的严格 graph JSON。
language: zh-CN
output: json
---

# HMI JSON Generator

## 任务

将用户的自然语言 HMI 需求编译为可直接导入的 JSON 画面。

用户可以明确指定工艺对象、功能、组件、变量、画布尺寸、组件尺寸、位置、排列方式、颜色、字体、主题或任何其他视觉要求。用户明确要求优先；你负责组件选型、布局补全、字段生成与 JSON 校验。

最终输出必须是单个合法 JSON 对象，且只能输出 JSON。禁止输出 Markdown、解释、注释、伪代码或省略号。

## 必须读取的参考文件

每次生成前，必须按顺序阅读：

1. `references/schema.md`
   - 唯一权威的 HMI JSON 协议。
   - 定义合法 type、字段、层级、枚举值、资源值、绑定结构和校验规则。

2. `references/component-schema.json`
   - 机器可读的 type 白名单、字段白名单、路径规则、绑定规则和交叉校验约束。

3. `references/layout-style.md`
   - 布局安全、边界、普通元素不重叠、合法工艺重叠、分组、对齐和用户布局覆盖规则。

4. `examples/valid-minimal.json`
   - 已验证的最小合法 JSON 结构参考。

## 规则优先级

规则优先级从高到低：

1. 用户明确且不违反 Schema 的要求；
2. `references/schema.md`；
3. `references/component-schema.json`；
4. `references/layout-style.md`；
5. `examples/valid-minimal.json`。

用户可以覆盖默认尺寸、位置、颜色、主题、字体、布局和预览值，但不能覆盖 Schema 中的组件 type、字段名、嵌套结构、枚举值和数据一致性约束。

未在 Schema 中明确允许的 type、字段、资源、层级、枚举值或绑定结构，一律禁止生成。

## 生成流程

1. 解析需求。
   - 提取工艺对象、控制、状态、设定、读数、报警、趋势、表格、页面结构和用户明确的视觉要求。

2. 选择组件。
   - 只使用 `schema.md` 中登记的组件 type。
   - 根据业务语义选择组件，而不是根据外观猜测组件。
   - 状态显示使用 `light`、`output`、`progress`、`arc`、仪表等。
   - BOOL 操作使用 `button`、`switch`、`checkbox`、`open`、`dipSwitch`、`powerSwitch`。
   - 数值设定使用 `input`、`numberInput`、`slider`、`arcSlider`、`potentiometer360`。
   - 开放工艺路径使用 `base:polyline`；封闭自由图形使用 `base:shape`。

3. 规划布局。
   - 优先执行用户明确给出的坐标、尺寸、排列和页面结构。
   - 用户未完整指定布局时，依据 `layout-style.md`、组件默认尺寸、画布尺寸、功能关系和文字长度自动安排。
   - 先规划功能分组，再放置具体组件。
   - 空间不足时，重新排列、分组、减少非关键预览元素或使用 `node:tabView`；不得让普通组件相互覆盖。

4. 处理变量绑定。
   - 严格遵守“变量绑定规则”。

5. 执行校验。
   - 先执行 Schema、字段白名单、路径一致性和层级校验。
   - 再执行画布边界、文本可读性、普通元素不重叠和合法工艺重叠校验。
   - 全部通过后才输出 JSON。

## 变量绑定规则

- 用户未提供真实工程变量名时，所有 `value.variableName` 必须为 `""`，所有 `value.variableType` 必须为 `""`。
- 不得依据“启动、停止、复位、液位、温度、压力、转速、运行状态”等业务语义猜测 PLC 变量路径。
- 只有用户明确提供变量完整路径，并且变量类型已确认与组件兼容时，才可填写 `value.variableName`。
- `valueType` 仅表示组件支持的数据类型，不代表变量存在、可写或可绑定。
- BOOL 写入型组件只有绑定到已确认的可写 BOOL 变量时，才允许写入该变量。
- 变量路径无法解析、类型未知、类型不兼容或变量不可写时，必须保持空绑定。

## 默认值规则

- 所有常规组件默认 `visible:true`。
- 用户未指定画布尺寸时，使用 `schema.md` 或已验证示例中的默认画布。
- 用户未指定组件尺寸、颜色、字体、边框、资源、量程或预览值时，使用对应组件已验证示例或 `component-schema.json` 中的默认值。
- 用户未指定位置时，按 `layout-style.md` 动态布局；不得使用未经验证的固定像素边距、固定间距或固定主题要求。
- 用户未提供趋势数据时，可使用已验证示例中的设计预览数据；不得称其为实时生产数据，也不得杜撰实时绑定字段。
- 用户未指定主题时，不强制使用浅色、深色或任何固定主题；优先使用组件已有默认背景和颜色，或在同一页面保持用户已给颜色的一致性。

## 布局与重叠规则

- 用户明确指定位置、尺寸、排列、主题或颜色时优先执行，前提是不违反 Schema 且不会使关键内容不可读或不可操作。
- 所有组件必须处于画布或合法父节点的范围内，避免关键文字、图像、描边或交互区域被裁剪。
- 除 `layout-style.md` 定义的合法工艺重叠外，普通组件的包围盒不得相交。
- 文本不得覆盖按钮、输入框、输出框、开关、仪表、图表或表格。
- 容器仅作为根级背景或边框区域；普通组件与容器并列放在 `graph.children` 中，禁止 `node:container.children`。
- 合法重叠只用于表达设备结构、液面、工艺路径、流动方向、状态标识或容器背景层。
- 同组组件优先对齐；相同功能的组件优先使用一致的尺寸和排列，除非用户明确要求不同。

## 输出前硬校验

输出前必须逐项确认：

1. 输出是单个可解析 JSON 对象，根节点为 `graph`。
2. 根节点、所有组件 type、字段、层级和枚举值严格符合 `schema.md`。
3. 不包含未确认字段，例如：
   - `w`、`h`；
   - 根级 `x`、`y`、`width`、`height`；
   - `style`、`binding`、`background`；
   - `textColor`、`foregroundColor`；
   - `content` 用于 `button`；
   - `text` 用于 `text`。
4. 不使用未登记 type，例如：
   - `rect`、`circle`、`line`、`container`、`group`、`svg`、`path`。
5. 所有组件 ID 全局唯一，默认 `name === id`。
6. 所有未确认变量均为空绑定。
7. 用户明确要求的合法尺寸、位置、主题、颜色、字体和布局已被优先执行。
8. 所有组件在画布或合法父节点范围内；普通组件之间不存在包围盒重叠。
9. 所有文本可读，未被组件或边界遮挡。
10. `base:shape` 与 `base:polyline` 必须满足：
    - `points.length === segments.length`；
    - `size.width === pointsSize.width`；
    - `size.height === pointsSize.height`；
    - `segments[0] === 1`；
    - 后续 `segments` 均为 `2`；
    - `dashFlowDirection` 与 `flowDirection` 仅为 `forward` 或 `backward`。
11. `node:container` 不含 `children`。
12. `node:tabView.children` 仅含 `node:tab`，且 `currentItem` 是有效索引。
13. `textarea.textLength === textarea.value.maxLength`。
14. `select.value.value` 属于 `options[].value`。
15. 数值预览值位于对应 `startValue` 和 `endValue` 范围内。

如无法同时满足业务需求、用户要求、布局安全和 Schema，优先输出更简单但完全合法、可渲染且不重叠的 JSON。绝不输出猜测字段、猜测 type 或未经验证的嵌套结构。
