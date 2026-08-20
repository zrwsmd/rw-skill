# HMI JSON Generator Skill v1.1

这是一个 ZIP 格式的 `.skill` 包。解压后导入 `SKILL.md`，并向 Agent 提供 `references/` 下的组件默认值与字段约束。

## v1.1 修正

本版删除了基于业务语义自动猜测 PLC 变量名的行为。用户没有提供真实变量或变量类型未验证时，统一生成空绑定：

```json
"variableName": ""
```

这使生成的画面 JSON 可以先导入、渲染，再由工程人员在 HMI 编辑器中完成真实变量绑定。
