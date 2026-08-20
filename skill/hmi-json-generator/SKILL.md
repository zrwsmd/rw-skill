---
name: hmi-json-generator
description: 将中文工控/HMI需求编译为现有渲染器可加载的严格 graph JSON。
language: zh-CN
output: json
---

# HMI JSON Generator

## 任务

把用户的自然语言 HMI 需求编译为一个可直接导入的 JSON 画面。用户只需描述工艺对象、功能、信息、视觉偏好以及可选的真实变量；你负责组件选择、布局与 JSON 生成。

输出必须是**一个 JSON 对象且仅包含 JSON**，不能输出 Markdown、解释、注释、伪代码或省略号。

## 强制读取顺序

生成前必须阅读：

1. `references/schema.md`：唯一权威的字段、类型、层级、禁止项和校验规则。
2. `references/component-schema.json`：机器可读的 type/字段白名单与默认值。
3. `examples/valid-minimal.json`：已验证的最小合法结构示例。

出现冲突时，以 `schema.md` 为最高优先级。未在 Schema 明确允许的 type、字段、资源值、层级或枚举值，一律禁止生成。

## 工作方式

1. 从自然语言抽取业务对象、操作、状态、设定、读数、报警、趋势和风格。
2. 使用 `schema.md` 的意图映射选择现有组件，不能创造新组件。
3. 用户未指定布局时自动布局：标题顶部；控制区域左侧/下方；状态靠近控制；工艺图或主要仪表置于中心或右侧；组件最小间距 16 px。
4. 用户未指定画布时用 800×600。所有根级组件必须留在画布内，且避免重叠。
5. 先建立组件对象，再执行 Schema 白名单和交叉字段校验；校验通过后才输出。

## 变量绑定规则

- 用户没有给出真实工程变量名时，所有 `value.variableName` 必须为 `""`，`variableType` 必须为 `""`。
- 不得根据“启动、停止、液位、温度、压力、运行”等语义猜测或生成 PLC 路径。
- 只有用户明确给出变量路径且其类型已确认兼容时，才能填写 `variableName`。
- `valueType` 只是组件的支持类型声明，不代表变量存在、可写或可绑定。
- BOOL 操作控件只有绑定到已确认的可写 BOOL 时才可写入变量。

## 安全默认值

- `visible:true`。
- 默认画布：800×600，`backgroundColor:"#ffffff"`。
- 默认文字/描边：`#000000`；默认 UI 主色：`#409eff`。
- 数值范围未指定时：`startValue:0`、`endValue:100`、预览值 `10`。
- 未提供趋势数据时允许使用 Schema 示例中的设计预览数据，但不得宣称为实时生产数据。

## 输出前硬校验

必须逐项满足 `schema.md` 的“最终检查清单”。特别禁止：

- `w`、`h`、根级 `x/y/width/height`、`style`、`binding`、`background`、`textColor`、`foregroundColor`、`content`（用于 button）、`text`（用于 text）。
- `rect`、`circle`、`line`、`container` 等未登记 type。
- `node:container.children`。
- 未登记的图片资源、方向值或字段。
- `points.length !== segments.length`。

如无法遵守 Schema，选择更简单的已验证组件组合；不要输出猜测结构。
