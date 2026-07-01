# 常见问题解答 (FAQ)

## 基础问题

### Q1: 这个 skill 和生成新闻视频有什么区别？
A: 这个 skill 是通用的文字转视频工具，不限于新闻。可以生成：
- 新闻视频
- 教程视频
- 产品介绍视频
- 故事视频
- 任何需要"文字 + 图片 + 字幕"的视频

### Q2: 需要什么技术背景？
A: 需要基本的：
- 命令行操作（npm, cd, mkdir）
- JSON 格式编辑
- 文件管理

不需要：
- 编程经验（除非要自定义样式）
- 视频编辑软件使用经验
- 设计经验

### Q3: 生成一个视频需要多久？
A: 
- 内容准备：10-20分钟（拆分字幕、搜索图片）
- 配置文件：5分钟
- 预览调整：5-10分钟
- 渲染视频：2-5分钟
- **总计：25-40分钟**

熟练后可以缩短到 15-20 分钟。

### Q4: 可以免费使用吗？
A: 完全免费，包括：
- Remotion（开源，MIT license）
- 图片素材（Pexels/Pixabay/Unsplash 免费商用）
- FFmpeg（开源）

---

## 图片相关

### Q5: 必须下载图片到本地吗？能不能直接用 URL？
A: **必须下载到本地**。Remotion 渲染时需要本地文件，不支持远程 URL。

```typescript
// ❌ 不支持
<img src="https://example.com/image.jpg" />

// ✅ 正确
<Img src={staticFile("media/image.jpg")} />
```

### Q6: 图片要求什么尺寸？
A: 
- **最低**：1920 x 1080 (1080p)
- **推荐**：2560 x 1440 或更高
- **宽高比**：16:9（与视频比例一致）

### Q7: 可以用手机拍的照片吗？
A: 可以，只要：
- 分辨率足够（至少 1920x1080）
- 与内容相关
- 清晰不模糊

### Q8: 可以使用 AI 生成的图片吗？
A: 可以，但建议在视频中标注 "AI合成" 或 "AI Generated"。

### Q9: 找不到合适的图片怎么办？
A: 几种方案：
1. 使用相关场景图片（找不到"iPhone"，用"smartphone"）
2. 使用抽象概念图片（如"会议""握手"）
3. 使用 AI 生成图片（Midjourney、DALL-E）

---

## 内容制作

### Q10: 字幕可以多长？
A: 
- **单行**：最多 25 个汉字
- **双行**：每行 15-20 个汉字
- **原则**：观众 3-5 秒内能读完

### Q11: 每个镜头应该多长？
A: 
- **太短**（1-2秒）：观众来不及阅读
- **合适**（3-5秒）：阅读舒适
- **太长**（6秒以上）：画面单调

### Q12: 如何避免字幕重复？
A: 递进式叙述，每个镜头推进故事：

❌ 错误（重复）：
```
镜头1: "苹果发布新 iPhone"
镜头2: "苹果推出 iPhone 15"
```

✅ 正确（递进）：
```
镜头1: "苹果公司今天举行新品发布会"
镜头2: "推出搭载 A17 芯片的 iPhone 15"
镜头3: "起售价 999 美元，9月开售"
```

### Q13: 一个视频应该有多少个镜头？
A: 取决于时长：
- **10-20秒**：2-4个镜头
- **30-60秒**：6-12个镜头
- **1-3分钟**：15-30个镜头

---

## 技术问题

### Q14: 为什么渲染后是黑屏？
A: 最常见原因：
1. 图片路径不正确
2. 图片不在 `public/media/` 目录
3. 没有使用 `staticFile()` API

解决方案：
```bash
# 检查图片是否存在
ls public/media/

# 检查 videoData.json 中的路径
cat src/videoData.json | grep "image"
```

### Q15: JSON 文件报错怎么办？
A: 最常见原因：
1. 使用了中文引号 `""`（应该用英文 `""`）
2. 多余的逗号
3. 缺少引号或括号

验证 JSON：
```bash
node -e "require('./src/videoData.json')"
```

### Q16: 渲染很慢怎么办？
A: 几个优化方法：
```bash
# 1. 压缩图片
# 使用 TinyPNG 或 Squoosh 压缩到 < 5MB

# 2. 降低渲染质量
npx remotion render ... --crf=28

# 3. 使用并行渲染
npx remotion render ... --concurrency=4
```

### Q17: 可以在服务器上渲染吗？
A: 可以，但需要：
1. 安装 FFmpeg
2. 足够的内存（建议 4GB+）
3. 无头模式渲染（不需要浏览器）

---

## 自定义和扩展

### Q18: 如何修改字幕样式？
A: 编辑 `src/ShotCard.tsx`：

```typescript
// 修改字体大小
fontSize: 34,  // 改成你想要的大小

// 修改颜色
color: "#ffffff",  // 改成你想要的颜色

// 添加阴影
textShadow: "2px 2px 4px rgba(0,0,0,0.8)"
```

### Q19: 如何制作竖屏视频（抖音/快手）？
A: 渲染时指定尺寸：

```bash
npx remotion render src/index.tsx Video out/vertical.mp4 \
  --width=1080 \
  --height=1920
```

可能需要调整字幕位置：
```typescript
// 竖屏时字幕上移
bottom: isPortrait ? 200 : 60
```

### Q20: 可以添加背景音乐吗？
A: 可以，使用 Remotion 的 `<Audio>` 组件：

```typescript
import { Audio } from "remotion";

<Audio src={staticFile("music/bgm.mp3")} volume={0.3} />
```

### Q21: 可以添加 Logo 水印吗？
A: 可以，在 `ShotCard.tsx` 中添加：

```typescript
<img 
  src={staticFile("logo.png")} 
  style={{
    position: "absolute",
    top: 20,
    right: 20,
    width: 100,
    opacity: 0.8
  }}
/>
```

---

## 输出和发布

### Q22: 视频文件太大怎么办？
A: 几种方案：
```bash
# 提高压缩率（降低质量）
--crf=28  # 默认 18，越大文件越小

# 使用 H.265 编码（更高压缩率）
--codec=h265

# 降低分辨率
--width=1280 --height=720
```

### Q23: 可以直接上传到 YouTube/B站吗？
A: 可以，渲染的 MP4 文件可以直接上传到：
- YouTube
- B站
- 抖音
- 快手
- 微信视频号

### Q24: 需要标注图片来源吗？
A: 
- **法律上**：Pexels/Pixabay/Unsplash 的图片不需要标注
- **道德上**：建议在视频描述中标注 "图片来源：Pexels"

---

## 高级用法

### Q25: 可以批量生成视频吗？
A: 可以，写个脚本循环渲染：

```bash
#!/bin/bash
for data in data/*.json; do
  name=$(basename "$data" .json)
  npx remotion render src/index.tsx Video "out/${name}.mp4"
done
```

### Q26: 可以用命令行生成 videoData.json 吗？
A: 可以，用脚本处理：

```javascript
// generateData.js
const fs = require('fs');

const content = "你的文字内容...";
const shots = splitContent(content); // 自己实现拆分逻辑
const data = { segments: [{ id: "auto", shots }] };

fs.writeFileSync('src/videoData.json', JSON.stringify(data, null, 2));
```

### Q27: 可以和 AI 结合自动生成吗？
A: 可以，流程：
1. 用 AI（如 GPT）生成字幕和拆分镜头
2. 用 AI 生成图片搜索关键词
3. 自动下载图片
4. 生成 videoData.json
5. 自动渲染

这需要一些编程知识。

---

## 其他

### Q28: 有没有可视化编辑器？
A: Remotion Studio 是可视化预览工具，但数据文件还是需要手动编辑 JSON。

### Q29: 可以商用吗？
A: 可以，只要：
- 图片是免费商用的（Pexels/Pixabay/Unsplash）
- 或者你有图片版权
- Remotion 本身是 MIT license

### Q30: 遇到问题怎么办？
A: 按顺序：
1. 查看 [故障排查指南](./troubleshooting.md)
2. 查看 [Remotion 官方文档](https://www.remotion.dev/docs)
3. 搜索 GitHub Issues
4. 在 Remotion Discord 提问
