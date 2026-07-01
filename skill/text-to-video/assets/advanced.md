# 高级功能指南

## 添加背景音乐

### 基础用法

```typescript
import { Audio } from "remotion";

// 在 index.tsx 中添加
<Audio src={staticFile("music/bgm.mp3")} volume={0.3} />
```

### 音乐淡入淡出

```typescript
import { Audio, interpolate, useCurrentFrame } from "remotion";

const AudioTrack: React.FC = () => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();
  
  // 开头3秒淡入，结尾3秒淡出
  const volume = interpolate(
    frame,
    [0, 90, durationInFrames - 90, durationInFrames],
    [0, 0.3, 0.3, 0],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );
  
  return <Audio src={staticFile("music/bgm.mp3")} volume={volume} />;
};
```

### 多段音乐切换

```typescript
// 根据不同片段播放不同音乐
{newsData.segments.map((segment, i) => {
  const startFrame = calculateStartFrame(i);
  return (
    <Sequence from={startFrame} durationInFrames={segment.duration}>
      <Audio src={staticFile(`music/${segment.mood}.mp3`)} volume={0.3} />
    </Sequence>
  );
})}
```

---

## 添加转场效果

### 交叉溶解

```typescript
// 在 ShotCard.tsx 中
const CrossFade: React.FC<{ duration: number }> = ({ duration }) => {
  const frame = useCurrentFrame();
  
  // 最后 duration 帧淡出
  const opacity = interpolate(
    frame,
    [durationInFrames - duration, durationInFrames],
    [1, 0]
  );
  
  return <div style={{ opacity }}>...</div>;
};
```

### 滑动切换

```typescript
const SlideTransition: React.FC = () => {
  const frame = useCurrentFrame();
  
  const translateX = interpolate(
    frame,
    [0, 30],
    [1920, 0],
    { easing: Easing.out(Easing.ease) }
  );
  
  return (
    <div style={{ transform: `translateX(${translateX}px)` }}>
      {children}
    </div>
  );
};
```

---

## 添加 Logo 水印

### 静态水印

```typescript
// 在 ShotCard.tsx 中添加
<img
  src={staticFile("logo.png")}
  style={{
    position: "absolute",
    top: 20,
    right: 20,
    width: 100,
    height: 100,
    opacity: 0.7
  }}
/>
```

### 动态水印（淡入淡出）

```typescript
const Logo: React.FC = () => {
  const frame = useCurrentFrame();
  
  const opacity = interpolate(
    frame,
    [0, 30, 270, 300],
    [0, 0.7, 0.7, 0]
  );
  
  return (
    <img
      src={staticFile("logo.png")}
      style={{
        position: "absolute",
        top: 20,
        right: 20,
        width: 100,
        opacity
      }}
    />
  );
};
```

---

## 多种字幕风格

### 电影风格（上下黑边）

```typescript
const CinematicSubtitle: React.FC = ({ subtitle }) => {
  return (
    <>
      {/* 上边遮幅 */}
      <div style={{
        position: "absolute",
        top: 0,
        width: "100%",
        height: 100,
        backgroundColor: "#000000"
      }} />
      
      {/* 下边遮幅 + 字幕 */}
      <div style={{
        position: "absolute",
        bottom: 0,
        width: "100%",
        height: 150,
        backgroundColor: "#000000",
        display: "flex",
        alignItems: "center",
        justifyContent: "center"
      }}>
        <div style={{ color: "#ffffff", fontSize: 28 }}>
          {subtitle}
        </div>
      </div>
    </>
  );
};
```

### 弹幕风格

```typescript
const DanmakuSubtitle: React.FC = ({ subtitle }) => {
  const frame = useCurrentFrame();
  const { width } = useVideoConfig();
  
  const translateX = interpolate(
    frame,
    [0, 300],
    [width, -500],
    { extrapolateRight: "clamp" }
  );
  
  return (
    <div style={{
      position: "absolute",
      top: 100,
      transform: `translateX(${translateX}px)`,
      color: "#ffffff",
      fontSize: 32,
      textShadow: "2px 2px 4px rgba(0,0,0,0.8)"
    }}>
      {subtitle}
    </div>
  );
};
```

---

## 动态数据源

### 从 API 获取数据

```typescript
// generateVideo.js
const fetch = require('node-fetch');
const fs = require('fs');

async function generateFromAPI() {
  // 从 API 获取新闻
  const response = await fetch('https://api.example.com/news');
  const news = await response.json();
  
  // 转换为 videoData 格式
  const videoData = {
    segments: news.articles.map(article => ({
      id: article.id,
      category: article.category,
      source: article.source,
      shots: splitIntoShots(article.content)
    }))
  };
  
  // 保存到文件
  fs.writeFileSync('src/videoData.json', JSON.stringify(videoData, null, 2));
  
  // 下载图片
  await downloadImages(videoData);
}
```

### 从 RSS 订阅生成

```typescript
const Parser = require('rss-parser');
const parser = new Parser();

async function generateFromRSS(feedUrl) {
  const feed = await parser.parseURL(feedUrl);
  
  const videoData = {
    segments: feed.items.slice(0, 5).map(item => ({
      id: item.guid,
      category: "RSS新闻",
      source: feed.title,
      shots: [
        {
          image: "media/default.jpg",
          subtitle: item.title,
          durationSeconds: 4
        }
      ]
    }))
  };
  
  return videoData;
}
```

---

## 批量渲染

### 批量渲染多个视频

```bash
#!/bin/bash
# batch-render.sh

for json_file in data/*.json; do
  basename=$(basename "$json_file" .json)
  echo "渲染 $basename..."
  
  cp "$json_file" src/videoData.json
  
  npx remotion render src/index.tsx Video "out/${basename}.mp4" \
    --codec=h264 \
    --crf=23
    
  echo "$basename 完成"
done
```

### 并行渲染

```bash
#!/bin/bash
# parallel-render.sh

# 使用 GNU parallel 并行渲染
ls data/*.json | parallel -j 4 '
  basename=$(basename {} .json)
  cp {} src/videoData.json
  npx remotion render src/index.tsx Video out/${basename}.mp4
'
```

---

## 自定义动画

### 打字机效果

```typescript
const TypewriterText: React.FC<{ text: string }> = ({ text }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  
  // 每5帧显示一个字
  const charsToShow = Math.floor(frame / 5);
  const displayText = text.slice(0, charsToShow);
  
  return <div>{displayText}</div>;
};
```

### 逐字淡入

```typescript
const FadeInWords: React.FC<{ text: string }> = ({ text }) => {
  const frame = useCurrentFrame();
  const words = text.split(' ');
  
  return (
    <div style={{ display: "flex", gap: 8 }}>
      {words.map((word, i) => {
        const opacity = interpolate(
          frame,
          [i * 10, i * 10 + 10],
          [0, 1],
          { extrapolateRight: "clamp" }
        );
        
        return (
          <span key={i} style={{ opacity }}>
            {word}
          </span>
        );
      })}
    </div>
  );
};
```

---

## 响应式设计

### 自适应不同分辨率

```typescript
const ResponsiveShot: React.FC = () => {
  const { width, height } = useVideoConfig();
  const isPortrait = height > width;
  const isMobile = width < 1280;
  
  return (
    <div style={{
      fontSize: isMobile ? 24 : 34,
      padding: isPortrait ? "20px 15px" : "20px 40px",
      bottom: isPortrait ? 200 : 60
    }}>
      {subtitle}
    </div>
  );
};
```

### 多语言支持

```typescript
const MultiLanguageSubtitle: React.FC = ({ subtitles }) => {
  const { language } = useVideoConfig();
  
  return (
    <>
      <div style={{ fontSize: 34 }}>
        {subtitles[language] || subtitles.en}
      </div>
      {language !== 'zh' && (
        <div style={{ fontSize: 20, marginTop: 10, opacity: 0.7 }}>
          {subtitles.zh}
        </div>
      )}
    </>
  );
};
```

---

## 性能优化

### 图片预加载

```typescript
import { prefetch } from "remotion";

// 在组件外预加载图片
const images = [
  "media/image1.jpg",
  "media/image2.jpg",
  "media/image3.jpg"
];

images.forEach(image => {
  prefetch(staticFile(image));
});
```

### 懒加载组件

```typescript
import { lazy, Suspense } from "react";

const HeavyComponent = lazy(() => import("./HeavyComponent"));

<Suspense fallback={<div>Loading...</div>}>
  <HeavyComponent />
</Suspense>
```

---

## 集成 CI/CD

### GitHub Actions 自动渲染

```yaml
# .github/workflows/render-video.yml
name: Render Video

on:
  push:
    paths:
      - 'src/videoData.json'

jobs:
  render:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      
      - name: Install dependencies
        run: npm install
      
      - name: Render video
        run: |
          npx remotion render src/index.tsx Video out/output.mp4
      
      - name: Upload artifact
        uses: actions/upload-artifact@v3
        with:
          name: video
          path: out/output.mp4
```

### 定时自动生成（每日新闻）

```yaml
# .github/workflows/daily-news.yml
name: Daily News Video

on:
  schedule:
    - cron: '0 8 * * *'  # 每天早上8点

jobs:
  generate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Fetch news data
        run: node scripts/fetch-news.js
      
      - name: Download images
        run: node scripts/download-images.js
      
      - name: Render video
        run: npx remotion render src/index.tsx Video out/daily-$(date +%Y%m%d).mp4
      
      - name: Upload to YouTube
        run: node scripts/upload-youtube.js
```

---

## 高级示例项目

查看完整的高级示例项目：

```bash
# 克隆示例项目
git clone https://github.com/example/remotion-advanced-examples
cd remotion-advanced-examples

# 查看示例
cd examples/music-video        # 带背景音乐
cd examples/transitions         # 自定义转场
cd examples/batch-render        # 批量渲染
cd examples/api-integration     # API集成
```
