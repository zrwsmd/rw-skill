# hmi-json-generator

完整 HMI JSON 生成 Skill 包。

## 文件

- `SKILL.md`：生成流程、原生组件、HTML 页面、变量、动态和输出校验规则。
- `references/schema.md`：唯一权威 HMI JSON Schema，包含 `graph.htmlCode`。
- `references/component-schema.json`：机器可读根字段、HTML 支持、嵌套、绑定、资源和路径约束。
- `references/layout-style.md`：原生组件、动态元素和 HTML 页面布局规则。
- `examples/valid-minimal.json`：最小可渲染示例。

## HTML 支持

根节点可选字段：

```json
"htmlCode": {
  "codeHeadValue": "...",
  "codeBodyValue": "..."
}
```

渲染器已验证支持常见 HTML 页面结构、常见标签与属性、完整 `<!DOCTYPE html>/<html>/<head>/<body>` 结构、CSS、内联 JavaScript、`<script src="...">` 外部脚本、DOM 交互、定时器和 iframe。

HTML 按正常网页开发方式生成：样式通常放在 `<head>` 中，页面内容和脚本通常放在 `<body>` 中。标准 HMI 控制、变量绑定、原生趋势图、仪表、按钮、输入和管线流动优先使用原生组件；复杂展示、动画和网页化交互可使用 HTML/CSS/JavaScript 或外部库。
