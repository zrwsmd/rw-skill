---
name: code-review-fixer
description: 自动读取代码审查报告HTML，根据问题严重程度（严重/中等/轻微/误报）逐个修改代码，每修改完一个问题等待用户确认后再继续下一个。适用于增量修复代码审查问题的场景。
allowed-tools: Bash, Read, Write, Glob, EditCode
---

## 使用场景
当用户说"修改代码审查报告里的严重问题"、"修复中等问题"、"处理轻微问题"等指令时触发本技能。

## 工作流程（必须严格遵守）

### 1. 解析报告阶段
- 用户指令示例："修改严重的问题" / "修复中等问题" / "处理轻微问题"
- 从指令中提取严重程度关键词：`严重` / `中等` / `轻微` / `误报`
- 使用 glob 查找项目根目录下的代码审查报告：`代码审查报告_*.html` 或 `Dai-Ma-Shen-Cha-Bao-Gao-*.html`
- 若有多个报告，选择最新修改时间的文件
- 运行解析脚本提取问题列表：
  ```bash
  python tools/parse_code_review_report.py --input "<报告路径>" --severity "<严重程度>" --output /tmp/issues.json
