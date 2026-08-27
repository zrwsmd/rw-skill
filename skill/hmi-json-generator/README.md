# hmi-json-generator

用于生成符合严格 HMI JSON 协议的 Skill 包，支持原生 HMI 组件、可选 HTML 页面，以及在同一个 `graph` JSON 中并列保存、分别独立渲染的原生组件层与 HTML 层。

## 文件说明

- `SKILL.md`：生成流程、需求解析、组件选型、变量使用、动态效果和输出校验规则。
- `references/schema.md`：唯一权威 HMI JSON Schema；定义根节点、字段白名单、组件类型、嵌套、绑定、路径、资源与 HTML 协议。
- `references/component-schema.json`：供程序读取的机器可读约束，包括根字段、组件字段、嵌套、绑定、资源和路径规则。
- `references/layout-style.md`：各渲染层自身的画布边界、组件对齐、合法工艺重叠和布局规则，以及禁止跨层空间协调的约束。
- `examples/valid-minimal.json`：可渲染的最小示例。

## 使用原则

1. 先阅读 `SKILL.md`，根据需求选择原生组件、HTML 或混合页面实现。
2. 所有输出 JSON 必须以 `references/schema.md` 为最终依据。
3. 字段白名单、组件类型、层级关系、变量绑定、路径约束和资源名必须符合 `references/component-schema.json`。
4. 原生组件层与 HTML 层必须分别在假设另一层不存在的前提下生成；各层内部的位置、边界、文字可读性和重叠必须符合 `references/layout-style.md`，不得进行跨层分区或避让。
5. 可参考 `examples/valid-minimal.json` 验证 JSON 的基本结构与渲染方式。

## HTML 与混合页面

根节点可选使用 `graph.htmlCode` 承载 HTML 内容。HTML 字段结构、字符串转义、支持能力、iframe 使用条件，以及 HTML 与 PLC/原生变量之间的数据边界，均以 `references/schema.md` 为准。

现场 PLC 控制、变量绑定、参数设定、报警确认、原生趋势图、仪表和工艺动画优先使用原生组件。复杂展示、复杂报表、第三方 API、摄像头、外部系统、iframe 和网页化交互可使用 HTML；两者需要同屏时可使用混合页面布局。

## 权威性顺序

当文件内容存在冲突时，按以下顺序处理：

1. 用户明确需求。
2. `references/schema.md` 的字段、类型、层级和数据结构约束。
3. `references/component-schema.json` 的机器可读约束。
4. `references/layout-style.md` 的布局规则。
5. `SKILL.md` 的生成流程与策略。
6. `examples/valid-minimal.json` 的参考实现。
