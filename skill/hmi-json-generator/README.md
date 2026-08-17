# HMI JSON Generator Skill

这是一个 ZIP 格式封装的 `.skill` 文件内容。核心规则在 `SKILL.md`，已确认的组件字段模板在 `references/component-templates.json`，示例需求与输出在 `examples/`。

## 使用

1. 解压此 `.skill` 文件。
2. 将 `SKILL.md` 作为 AI Agent/Skill 的系统说明或技能定义导入。
3. 将 `references/component-templates.json` 作为结构化 Schema 参考一并提供。
4. 要求模型严格按 `SKILL.md`：读取用户中文 HMI 需求，输出单个合法 `graph` JSON，且不得输出解释性文本。

## 文件

- `SKILL.md`：完整规则、路由表、布局规则与校验清单
- `references/component-templates.json`：32 个根级组件加 `node:tab` 的字段模板
- `examples/motor-control.input.txt`：电机控制场景输入
- `examples/motor-control.output.json`：对应 JSON 输出范例

## v1 边界

- `base:shape` / `base:polyline` 仅生成已验证的直线段模式：首段为 `1`，其余为 `2`。
- 仅使用已确认图片资源名 `Gray`、`Green`，以及已给出的默认流动图片路径。
- 不为趋势图、XY 图或 PLC 变量捏造未提供的运行时绑定字段。
