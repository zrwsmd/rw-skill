---
name: text-to-video
description: Convert any text content (news, tutorials, product intros, stories) into a subtitled video with real photos, rendered frame-by-frame with Remotion. Use whenever the user asks to turn text/a script into a video, generate a video from an article, or make a subtitled photo-slideshow-style video — including phrases like "把这段文字做成视频" / "生成一个视频" / "文字转视频" / "帮我做个新闻视频/教程视频/产品介绍视频". Covers the full pipeline: splitting content into shots, sourcing and verifying real images, and rendering.
---

# Text to Video Generator

将文字内容转换为带字幕和图片的视频，使用 Remotion 框架逐帧渲染。

## 功能

- 将任何文字内容转换为视频（新闻、教程、故事、产品介绍等）
- 支持多镜头叙事结构
- 自动配图和字幕
- Ken Burns 动画效果
- 输出高质量 MP4 视频

## 使用场景

- 📰 新闻播报视频
- 🎓 教育教程视频
- 📱 产品介绍视频
- 📖 故事讲述视频
- 🎬 自媒体内容视频

## 工作流程

1. **理解用户需求**：确定视频主题、风格、时长
   - **如果用户只给了主题、没有直接提供文字内容，且内容涉及真实世界的事实（新闻/时事/产品信息/数据）**：先联网检索获取真实、最新信息，不要凭训练数据编造，详见 `references/fact-accuracy.md`
2. **内容拆分**：将文字内容拆分为多个镜头，每个镜头 3-5 秒
3. **配图搜索**：为每个镜头找到匹配的图片（Pexels、Pixabay、Unsplash）
4. **项目配置**：创建 Remotion 项目结构
5. **数据准备**：生成 JSON 配置文件
6. **图片下载**：将图片保存到 public/media/ 目录
7. **⚠️ 关键步骤：验证图片内容**（详见 `references/strict-verification.md`）
   - 逐一检查每张下载的图片
   - 严格验证人名、地名、事件、时效性、人像取景、清晰度
   - 确认图片内容与对应字幕高度匹配
   - 如果不匹配，立即重新搜索和下载
8. **渲染视频**：运行 Remotion 渲染命令
9. **最终验证**：预览渲染后的视频，确认图文匹配度、人物头部是否完整

## 核心概念

### 多镜头叙事

将内容拆分为多个"镜头"（shots），每个镜头包含：
- 一张图片
- 一段字幕（不重复，递进叙述）
- 时长（3-5 秒）

示例：
```
原文："苹果公司今天发布了新款 iPhone，配备 A17 芯片，售价 999 美元。"

拆分为 3 个镜头：
1. 图片：苹果发布会现场 | 字幕："苹果公司今天举行新品发布会" | 4秒
2. 图片：iPhone 特写 | 字幕："推出搭载 A17 芯片的新款 iPhone" | 4秒
3. 图片：价格展示 | 字幕："起售价 999 美元" | 3秒
```

### JSON 数据结构

```json
{
  "date": "2026年7月1日",
  "segments": [
    {
      "id": "segment1",
      "category": "分类标签",
      "source": "来源",
      "shots": [
        {
          "image": "media/image1.jpg",
          "subtitle": "字幕内容",
          "durationSeconds": 4,
          "focalPoint": "top"
        }
      ]
    }
  ]
}
```

`focalPoint` 是可选字段（`"top" | "center" | "bottom"`，默认 `"center"`），人物是画面主体且原图头部没有留白时设为 `"top"`，避免裁剪切头，详见 `references/strict-verification.md` 第5节。

### 技术栈

- Remotion：React 框架的视频渲染引擎
- React + TypeScript
- staticFile()：引用本地图片
- Ken Burns 效果：慢速缩放动画

## 快速开始

用户提供文字内容后：

1. 询问视频风格（新闻、教程、故事等）
2. 将内容拆分为镜头（参考 `references/content-splitting.md`）
3. 搜索匹配图片（参考 `references/image-sourcing.md`）
4. 创建项目结构：
   ```bash
   npx create-video@latest my-video
   cd my-video
   npm install
   ```
5. 复制 `scripts/` 中的模板代码
6. 下载图片到 `public/media/`
7. 生成数据文件 `src/videoData.json`
8. 渲染：
   ```bash
   npx remotion render src/index.tsx Video out/output.mp4
   ```

## 注意事项

- 字幕要递进叙述，不要重复信息
- 每个镜头 3-5 秒，总时长根据内容调整
- 图片必须下载到本地，不能用 URL
- 使用免费商用图片（Pexels、Pixabay、Unsplash）
- 图片尺寸建议 1920x1080 或更高，**且必须目视确认真的清晰**
- **⚠️ 关键：下载图片后必须验证内容，不能直接渲染**
- **⚠️ 严格验证人名、地名、事件是否与图片匹配（详见 `references/strict-verification.md`）**
- **⚠️ 人物是画面主体时，头部必须完整、有 headroom，不能被裁剪切掉**
- **⚠️ 涉及真实世界事实的内容，必须联网核实、不许编造（详见 `references/fact-accuracy.md`）**
- **⚠️ 优先使用项目中已验证过的图片库**
- **⚠️ 渲染前先预览 1-2 个镜头，确认图文匹配**

## 镜头数量与视频时长怎么定

不要用一个固定数字套所有输入，按下面的优先级判断：

1. **用户当次提示词里明确说的数字/时长 — 硬约束，直接采用**（比如"控制在1分钟以内""我只要3个镜头""做成30秒的短视频"）。这个优先级最高，覆盖下面所有默认逻辑。
2. **没有明确说时，让内容本身决定** — 按 `references/content-splitting.md` 的拆分逻辑，原文信息点多就多拆，信息点少就少拆，不要为了凑一个心里默认的数字去拆分或合并镜头，那样会制造重复或者信息过密。
3. **宁可多覆盖，不要为了控制数量牺牲信息完整度** — 拆分时如果原文本身信息量大，优先保留完整叙事（多拆几个镜头），而不是为了"看起来精简"砍掉本该讲的信息点。
4. **兜底范围（仅用于兜底判断，不是目标值）**：单个视频建议落在 2-8 个镜头之间。自然拆分结果明显超出这个区间（比如内容极短只能拆1个镜头，或内容极长要拆12+个镜头）时，跟用户确认一下——"内容拆出来只够1个镜头，要不要我再补充点细节"或"这段内容信息量比较大，建议拆成12个镜头/2分钟，还是你想要更精简的版本？"——而不是不声不响地硬凑或硬砍。

## 参考文档

- `references/fact-accuracy.md` - **信息准确性/时效性规则（必读，涉及真实事实的内容优先看）** - 联网核实、不许编造
- `references/content-splitting.md` - 内容拆分指南
- `references/image-sourcing.md` - 图片搜索指南
- `references/strict-verification.md` - **严格验证流程（必读）** - 人名/地名/事件/时效性/人像取景/清晰度验证
- `references/visual-style.md` - 视觉风格指南
- `scripts/ShotCard.tsx` - 镜头组件模板
- `scripts/index.tsx` - 主组合模板
- `scripts/data-template.json` - 数据结构模板
