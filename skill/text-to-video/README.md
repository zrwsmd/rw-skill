# Text to Video - 文字转视频 Skill

这是一个通用的文字转视频 skill，可以将任何文字内容转换为带字幕和图片的视频。

## 目录结构

```
text-to-video/
├── SKILL.md                    # 主文档（开始阅读这个）
├── README.md                   # 本文件
├── assets/                     # 资源和指南
│   ├── quick-start.md          # 5分钟快速上手
│   ├── examples.md             # 完整示例
│   ├── workflow.md             # 工作流程图
│   ├── troubleshooting.md      # 故障排查
│   └── project-structure.md    # 项目结构说明
├── references/                 # 参考文档
│   ├── content-splitting.md    # 内容拆分方法
│   ├── image-sourcing.md       # 图片搜索指南
│   └── visual-style.md         # 视觉设计规范
└── scripts/                    # 代码模板
    ├── README.md               # 模板使用说明
    ├── ShotCard.tsx            # 镜头组件
    ├── index.tsx               # 主入口
    └── data-template.json      # 数据模板
```

## 快速导航

### 🚀 新手入门
1. 先阅读 [SKILL.md](./SKILL.md) 了解基本概念
2. 然后看 [快速开始指南](./assets/quick-start.md) 创建第一个视频
3. 遇到问题查看 [故障排查](./assets/troubleshooting.md)

### 📚 深入学习
- [内容拆分指南](./references/content-splitting.md) - 如何将文字拆分为多个镜头
- [图片搜索指南](./references/image-sourcing.md) - 如何找到合适的图片
- [视觉风格指南](./references/visual-style.md) - 如何自定义字幕和样式

### 💡 参考示例
- [完整示例](./assets/examples.md) - 4个完整的从文字到视频的案例
- [工作流程](./assets/workflow.md) - 完整的工作流程图

### 🔧 代码模板
- [scripts/](./scripts/) 目录包含所有代码模板
- [scripts/README.md](./scripts/README.md) 说明如何使用模板

## 核心特性

- ✅ **通用性**: 不限于新闻，支持教程、产品、故事等任何类型
- ✅ **多镜头**: 支持将内容拆分为多个镜头，每个镜头独立配图
- ✅ **递进叙述**: 字幕逐步推进故事，不重复信息
- ✅ **动画效果**: Ken Burns 缩放、淡入淡出
- ✅ **TV 新闻风格**: 底部字幕条、类别标签、来源标注
- ✅ **自定义样式**: 可以修改字体、颜色、布局

## 使用场景

- 📰 **新闻播报**: 每日新闻、快讯、报道
- 🎓 **教育教程**: 烹饪、编程、技能教学
- 📱 **产品介绍**: 功能演示、卖点展示
- 📖 **故事讲述**: 历史、传记、案例分析
- 🎬 **自媒体内容**: YouTube、B站、抖音视频

## 技术栈

- [Remotion](https://www.remotion.dev/) - React 视频渲染框架
- React + TypeScript
- FFmpeg（自动安装）

## 5分钟快速开始

```bash
# 1. 创建项目
npx create-video@latest my-video
cd my-video
npm install

# 2. 复制模板
cp /path/to/skill/scripts/*.tsx src/
cp /path/to/skill/scripts/data-template.json src/videoData.json

# 3. 创建图片目录
mkdir -p public/media

# 4. 编辑 src/videoData.json 填入内容

# 5. 下载图片到 public/media/

# 6. 预览
npx remotion studio

# 7. 渲染
npx remotion render src/index.tsx Video out/output.mp4
```

详细步骤请查看 [快速开始指南](./assets/quick-start.md)

## 工作流程

```
文字内容 → 拆分镜头 → 搜索图片 → 下载图片 → 配置数据 → 预览 → 渲染
```

详细流程请查看 [工作流程图](./assets/workflow.md)

## 最佳实践

1. **字幕长度**: 每个镜头不超过25个汉字
2. **镜头时长**: 3-5秒最佳
3. **递进叙述**: 每个镜头推进故事，不要重复
4. **图片质量**: 至少 1920x1080
5. **预览优先**: 渲染前一定要预览

## 示例项目

查看 [完整示例](./assets/examples.md) 了解：
- 科技新闻视频（14秒，4镜头）
- 教程视频（21秒，6镜头）
- 产品介绍视频（16秒，5镜头）
- 新闻快讯视频（18秒，4镜头）

## 故障排查

常见问题：
- 黑屏问题 → 检查图片路径和 `staticFile()` 使用
- JSON 错误 → 检查中文引号
- 渲染慢 → 压缩图片到 < 5MB
- 字幕看不清 → 增加背景遮罩透明度

详细解决方案请查看 [故障排查指南](./assets/troubleshooting.md)

## 常见问题

**Q: 可以生成多长的视频？**
A: 理论上无限制，建议单个视频 1-3 分钟最佳。

**Q: 图片必须下载到本地吗？**
A: 是的，Remotion 不支持远程 URL，必须使用 `staticFile()` 引用本地图片。

**Q: 可以用自己的图片吗？**
A: 可以，只要放到 `public/media/` 目录即可。

**Q: 可以修改样式吗？**
A: 可以，编辑 `ShotCard.tsx` 自定义字体、颜色、布局等。

**Q: 支持竖屏视频吗？**
A: 支持，渲染时指定 `--width=1080 --height=1920` 即可。

## 进阶功能

- 自定义动画效果
- 多种字幕风格（新闻/教程/故事）
- 添加背景音乐
- 添加转场效果
- 批量生成视频

详细说明请查看各个参考文档。

## 获取帮助

- 📖 查看 [SKILL.md](./SKILL.md) 主文档
- 💡 查看 [示例](./assets/examples.md) 获取灵感
- 🔧 查看 [故障排查](./assets/troubleshooting.md) 解决问题
- 🌐 访问 [Remotion 官方文档](https://www.remotion.dev/docs)

## License

MIT
