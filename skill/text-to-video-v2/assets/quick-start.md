# 快速开始指南

5分钟快速上手文字转视频。

## 第一步：安装依赖

```bash
# 确保 Node.js >= 16
node --version

# 创建项目
npx create-video@latest my-first-video
cd my-first-video
npm install
```

## 第二步：复制模板

```bash
# 从 skill 目录复制模板文件
cp /path/to/skill/text-to-video/scripts/ShotCard.tsx src/
cp /path/to/skill/text-to-video/scripts/index.tsx src/
cp /path/to/skill/text-to-video/scripts/data-template.json src/videoData.json
```

## 第三步：准备内容

编辑 `src/videoData.json`，填入你的内容：

```json
{
  "segments": [
    {
      "id": "my-story",
      "category": "我的视频",
      "source": "原创",
      "shots": [
        {
          "image": "media/shot1.jpg",
          "subtitle": "这是第一个镜头的字幕",
          "durationSeconds": 4
        },
        {
          "image": "media/shot2.jpg",
          "subtitle": "这是第二个镜头的字幕",
          "durationSeconds": 3
        }
      ]
    }
  ]
}
```

## 第四步：下载图片

```bash
# 创建图片目录
mkdir -p public/media

# 访问 Pexels 下载图片
# https://www.pexels.com

# 将图片保存到 public/media/ 目录
# 重命名为 shot1.jpg, shot2.jpg
```

## 第五步：预览

```bash
npx remotion studio
```

浏览器会自动打开，你可以实时预览视频效果。

## 第六步：渲染

```bash
npx remotion render src/index.tsx Video out/output.mp4 --codec=h264
```

完成！视频保存在 `out/output.mp4`

---

## 完整示例：制作一个10秒科技新闻视频

### 1. 准备文字内容

```
"OpenAI 今天发布了 GPT-5 模型，性能比 GPT-4 提升3倍，支持更长的上下文窗口。"
```

### 2. 拆分镜头

```
镜头1: "OpenAI 今天发布 GPT-5 模型" (4秒)
镜头2: "性能提升3倍，支持更长上下文" (3秒)
```

### 3. 搜索图片

访问 https://www.pexels.com

- 搜索 "AI technology" 下载第一张
- 搜索 "data center" 下载第二张

保存为：
- `public/media/ai-tech.jpg`
- `public/media/data-center.jpg`

### 4. 编辑配置文件

编辑 `src/videoData.json`：

```json
{
  "segments": [
    {
      "id": "gpt5-news",
      "category": "科技新闻",
      "source": "OpenAI",
      "shots": [
        {
          "image": "media/ai-tech.jpg",
          "subtitle": "OpenAI 今天发布 GPT-5 模型",
          "durationSeconds": 4
        },
        {
          "image": "media/data-center.jpg",
          "subtitle": "性能提升3倍，支持更长上下文",
          "durationSeconds": 3
        }
      ]
    }
  ]
}
```

### 5. 预览和渲染

```bash
# 预览
npx remotion studio

# 满意后渲染
npx remotion render src/index.tsx Video out/gpt5-news.mp4 --codec=h264
```

完成！一个7秒的科技新闻视频就做好了。

---

## 常用命令

```bash
# 预览视频
npm start

# 渲染视频
npm run build

# 渲染高质量视频
npx remotion render src/index.tsx Video out/output.mp4 \
  --codec=h264 \
  --crf=18

# 渲染竖屏视频（抖音/快手）
npx remotion render src/index.tsx Video out/vertical.mp4 \
  --width=1080 \
  --height=1920

# 渲染指定片段（10-20秒）
npx remotion render src/index.tsx Video out/clip.mp4 \
  --frames=300-600
```

---

## 下一步

- 📖 阅读 [内容拆分指南](../references/content-splitting.md) 学习如何拆分字幕
- 🖼️ 阅读 [图片搜索指南](../references/image-sourcing.md) 学习如何找图片
- 🎨 阅读 [视觉风格指南](../references/visual-style.md) 学习如何自定义样式
- 💡 查看 [完整示例](./examples.md) 获取更多灵感
- 🔧 遇到问题？查看 [故障排查指南](./troubleshooting.md)

---

## 小贴士

1. **字幕长度**: 每个镜头字幕不超过25个汉字
2. **镜头时长**: 3-5秒最佳，太短读不完，太长单调
3. **图片尺寸**: 至少 1920x1080，避免模糊
4. **递进叙述**: 每个镜头推进故事，不要重复
5. **预览优先**: 渲染前一定要在 studio 中预览

---

## 一行命令创建项目

```bash
npx create-video@latest my-video && \
cd my-video && \
npm install && \
mkdir -p public/media && \
echo '{"segments":[{"id":"demo","category":"示例","source":"原创","shots":[{"image":"media/demo.jpg","subtitle":"这是一个示例镜头","durationSeconds":4}]}]}' > src/videoData.json && \
echo "项目创建完成！现在下载图片到 public/media/ 然后运行 npm start 预览"
```
