# 性能优化指南

提升渲染速度和视频质量的最佳实践。

## 图片优化

### 压缩图片

**问题**: 大图片（>5MB）会显著降低渲染速度

**解决方案**:

#### 方法1: 使用 TinyPNG
访问 https://tinypng.com/ 上传图片压缩

#### 方法2: 使用 Squoosh
访问 https://squoosh.app/ 在线压缩，可以精确控制质量

#### 方法3: 使用命令行工具

```bash
# 使用 ImageMagick
mogrify -resize 1920x1080 -quality 85 public/media/*.jpg

# 使用 jpegoptim
jpegoptim --size=2048k public/media/*.jpg

# 使用 pngquant (PNG)
pngquant --quality=65-80 public/media/*.png
```

#### 方法4: 批量处理脚本

```javascript
// compress-images.js
const sharp = require('sharp');
const fs = require('fs');
const path = require('path');

const inputDir = 'public/media';
const files = fs.readdirSync(inputDir);

files.forEach(async file => {
  if (file.endsWith('.jpg') || file.endsWith('.png')) {
    const inputPath = path.join(inputDir, file);
    const outputPath = path.join(inputDir, `optimized-${file}`);
    
    await sharp(inputPath)
      .resize(1920, 1080, { fit: 'cover' })
      .jpeg({ quality: 85 })
      .toFile(outputPath);
    
    console.log(`压缩完成: ${file}`);
  }
});
```

**最佳实践**:
- JPG 质量: 80-85%
- 目标文件大小: 500KB - 2MB
- 分辨率: 1920x1080 或 2560x1440

---

## 渲染优化

### 并行渲染

```bash
# 使用多个 CPU 核心
npx remotion render src/index.tsx Video out/output.mp4 \
  --concurrency=4

# 自动检测 CPU 核心数
npx remotion render src/index.tsx Video out/output.mp4 \
  --concurrency=$(nproc)
```

### 渲染指定片段

```bash
# 只渲染前10秒（0-300帧）
npx remotion render src/index.tsx Video out/preview.mp4 \
  --frames=0-300

# 只渲染10-20秒
npx remotion render src/index.tsx Video out/clip.mp4 \
  --frames=300-600
```

### 使用草稿模式预览

```bash
# 降低质量快速预览
npx remotion render src/index.tsx Video out/draft.mp4 \
  --crf=35 \
  --scale=0.5
```

---

## 代码优化

### 避免重复计算

❌ **不好的做法**:
```typescript
{videoData.segments.map((segment, i) => {
  // 每次渲染都计算
  const startFrame = videoData.segments
    .slice(0, i)
    .reduce((sum, s) => sum + s.duration * 30, 0);
  
  return <Sequence from={startFrame}>...</Sequence>;
})}
```

✅ **好的做法**:
```typescript
// 提前计算一次
const segmentFrames = useMemo(() => {
  let currentFrame = 0;
  return videoData.segments.map(segment => {
    const start = currentFrame;
    currentFrame += segment.duration * 30;
    return { start, duration: segment.duration * 30 };
  });
}, [videoData]);

{videoData.segments.map((segment, i) => (
  <Sequence from={segmentFrames[i].start}>...</Sequence>
))}
```

### 使用 React.memo

```typescript
// 避免不必要的重新渲染
export const ShotCard = React.memo<ShotProps>(({ subtitle, image, ... }) => {
  // 组件代码
});
```

### 懒加载图片

```typescript
const LazyImage: React.FC<{ src: string }> = ({ src }) => {
  const [loaded, setLoaded] = useState(false);
  
  return (
    <>
      {!loaded && <div style={{ background: "#333" }} />}
      <Img
        src={staticFile(src)}
        onLoad={() => setLoaded(true)}
        style={{ display: loaded ? "block" : "none" }}
      />
    </>
  );
};
```

---

## 编码优化

### 选择合适的编码器

```bash
# H.264 - 兼容性最好，速度快
npx remotion render ... --codec=h264

# H.265 (HEVC) - 文件更小，但编码慢
npx remotion render ... --codec=h265

# ProRes - 质量最高，但文件巨大
npx remotion render ... --codec=prores
```

### 调整 CRF 值

```bash
# CRF 范围: 0-51，越小质量越高，文件越大

# 高质量（推荐用于最终输出）
--crf=18

# 中等质量（适合快速预览）
--crf=23

# 低质量（草稿模式）
--crf=28
```

### 优化像素格式

```bash
# 兼容性最好
--pixel-format=yuv420p

# 更高色彩深度（文件更大）
--pixel-format=yuv444p
```

---

## 内存优化

### 限制内存使用

```bash
# 设置 Node.js 内存限制
NODE_OPTIONS="--max-old-space-size=4096" npx remotion render ...
```

### 清理缓存

```bash
# 清理 Remotion 缓存
rm -rf .remotion

# 清理 npm 缓存
npm cache clean --force

# 清理 node_modules 重新安装
rm -rf node_modules
npm install
```

---

## 文件大小优化

### 对比不同设置

| 设置 | 1分钟视频大小 | 渲染时间 | 质量 |
|-----|-------------|---------|------|
| CRF 18 + H.264 | ~50MB | 3分钟 | 最高 |
| CRF 23 + H.264 | ~25MB | 2分钟 | 高 |
| CRF 28 + H.264 | ~15MB | 1.5分钟 | 中 |
| CRF 23 + H.265 | ~15MB | 4分钟 | 高 |

### 最佳实践

**用于发布**:
```bash
npx remotion render src/index.tsx Video out/final.mp4 \
  --codec=h264 \
  --crf=20 \
  --pixel-format=yuv420p
```

**用于预览**:
```bash
npx remotion render src/index.tsx Video out/draft.mp4 \
  --codec=h264 \
  --crf=28 \
  --scale=0.75
```

---

## 批量处理优化

### 使用队列系统

```javascript
// render-queue.js
const Queue = require('bull');
const { exec } = require('child_process');

const renderQueue = new Queue('video-render');

renderQueue.process(4, async (job) => {
  const { dataFile, outputFile } = job.data;
  
  return new Promise((resolve, reject) => {
    exec(`npx remotion render ... ${outputFile}`, (error, stdout) => {
      if (error) reject(error);
      else resolve(stdout);
    });
  });
});

// 添加任务
renderQueue.add({ dataFile: 'data1.json', outputFile: 'out1.mp4' });
renderQueue.add({ dataFile: 'data2.json', outputFile: 'out2.mp4' });
```

---

## 监控和调试

### 启用性能日志

```bash
# 显示详细渲染信息
npx remotion render ... --log=verbose

# 显示进度条
npx remotion render ... --progress
```

### 测量渲染时间

```bash
#!/bin/bash
start=$(date +%s)

npx remotion render src/index.tsx Video out/output.mp4

end=$(date +%s)
duration=$((end - start))
echo "渲染耗时: ${duration}秒"
```

### 检查资源使用

```bash
# 在渲染时监控资源
htop

# 或使用 time 命令
time npx remotion render ...
```

---

## 缓存策略

### 缓存图片

```typescript
// 预加载图片到缓存
import { prefetch } from "remotion";

const images = videoData.segments.flatMap(s => 
  s.shots.map(shot => shot.image)
);

images.forEach(img => {
  prefetch(staticFile(img));
});
```

### 使用 Web Worker

```typescript
// 复杂计算放到 Worker
const worker = new Worker('./compute.worker.js');

worker.postMessage({ data: complexData });
worker.onmessage = (e) => {
  const result = e.data;
  // 使用计算结果
};
```

---

## 服务器渲染优化

### Docker 容器配置

```dockerfile
# Dockerfile
FROM node:18

# 安装 FFmpeg
RUN apt-get update && \
    apt-get install -y ffmpeg

# 复制项目
COPY . /app
WORKDIR /app

# 安装依赖
RUN npm install

# 渲染命令
CMD ["npx", "remotion", "render", "src/index.tsx", "Video", "out/output.mp4"]
```

### 使用 Lambda/云函数

```javascript
// aws-lambda-render.js
const { exec } = require('child_process');
const AWS = require('aws-sdk');
const s3 = new AWS.S3();

exports.handler = async (event) => {
  const { dataUrl } = event;
  
  // 下载数据文件
  const data = await fetch(dataUrl);
  
  // 渲染视频
  await execPromise('npx remotion render ...');
  
  // 上传到 S3
  const video = fs.readFileSync('out/output.mp4');
  await s3.upload({
    Bucket: 'my-videos',
    Key: 'output.mp4',
    Body: video
  }).promise();
  
  return { statusCode: 200, body: 'Rendered' };
};
```

---

## 性能检查清单

渲染前检查：
- [ ] 所有图片已压缩（< 2MB）
- [ ] 图片分辨率合适（1920x1080）
- [ ] JSON 数据文件格式正确
- [ ] 没有不必要的重复计算
- [ ] 使用了 React.memo 优化组件

渲染时设置：
- [ ] 使用合适的 concurrency 值
- [ ] 选择合适的 CRF 值
- [ ] 使用正确的编码器
- [ ] 启用进度显示

---

## 性能对比

### 渲染时间对比（1分钟视频，4核 CPU）

| 优化项 | 渲染时间 | 改进 |
|-------|---------|------|
| 未优化 | 8分钟 | - |
| 压缩图片 | 5分钟 | -37% |
| + 并行渲染 | 3分钟 | -40% |
| + 代码优化 | 2.5分钟 | -17% |
| + CRF 23 | 2分钟 | -20% |

### 文件大小对比（1分钟视频）

| 设置 | 文件大小 | 质量损失 |
|-----|---------|---------|
| 原始 | 80MB | 0% |
| 压缩图片 | 50MB | 0% |
| CRF 23 | 25MB | <5% |
| H.265 | 15MB | <5% |

---

## 推荐配置

### 开发环境（快速预览）
```bash
npx remotion render src/index.tsx Video out/preview.mp4 \
  --codec=h264 \
  --crf=28 \
  --scale=0.75 \
  --concurrency=2
```

### 生产环境（最终输出）
```bash
npx remotion render src/index.tsx Video out/final.mp4 \
  --codec=h264 \
  --crf=20 \
  --pixel-format=yuv420p \
  --concurrency=4
```

### 服务器环境（批量渲染）
```bash
npx remotion render src/index.tsx Video out/output.mp4 \
  --codec=h264 \
  --crf=23 \
  --concurrency=8 \
  --log=verbose
```
