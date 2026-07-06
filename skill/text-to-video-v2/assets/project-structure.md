# 项目结构示例

## 完整的文字转视频项目结构

```
my-video/
├── package.json                    # 依赖配置
├── remotion.config.ts              # Remotion 配置
├── src/
│   ├── index.tsx                   # 主入口（从 scripts/ 复制）
│   ├── ShotCard.tsx                # 镜头组件（从 scripts/ 复制）
│   └── videoData.json              # 视频数据（从 data-template.json 复制并编辑）
├── public/
│   └── media/                      # 图片素材目录
│       ├── image1.jpg
│       ├── image2.jpg
│       └── image3.jpg
└── out/
    └── output.mp4                  # 渲染输出
```

## videoData.json 示例

```json
{
  "segments": [
    {
      "id": "segment1",
      "category": "科技新闻",
      "source": "TechCrunch",
      "shots": [
        {
          "image": "media/apple-event.jpg",
          "subtitle": "苹果公司今天举行新品发布会",
          "durationSeconds": 4
        },
        {
          "image": "media/iphone-closeup.jpg",
          "subtitle": "推出搭载 A17 芯片的 iPhone 15 Pro",
          "durationSeconds": 4
        },
        {
          "image": "media/price-display.jpg",
          "subtitle": "起售价 999 美元，9月15日开售",
          "durationSeconds": 3
        }
      ]
    }
  ]
}
```

## package.json 依赖

```json
{
  "name": "my-video",
  "version": "1.0.0",
  "scripts": {
    "start": "remotion studio",
    "build": "remotion render src/index.tsx Video out/output.mp4"
  },
  "dependencies": {
    "react": "^18.2.0",
    "remotion": "^4.0.0"
  },
  "devDependencies": {
    "@types/react": "^18.2.0",
    "typescript": "^5.0.0"
  }
}
```

## remotion.config.ts 配置

```typescript
import { Config } from "@remotion/cli/config";

Config.setVideoImageFormat("jpeg");
Config.setOverwriteOutput(true);
```

## 文件大小参考

```
my-video/
├── src/                    ~10 KB
│   ├── index.tsx           ~2 KB
│   ├── ShotCard.tsx        ~4 KB
│   └── videoData.json      ~1 KB
├── public/media/           ~5-10 MB
│   ├── image1.jpg          ~2 MB
│   ├── image2.jpg          ~1.5 MB
│   └── image3.jpg          ~2 MB
└── out/
    └── output.mp4          ~5-15 MB (取决于时长)
```

## Git 忽略配置

创建 `.gitignore` 文件：

```
# 依赖
node_modules/

# 输出文件
out/
*.mp4

# 临时文件
.remotion/
.cache/

# 系统文件
.DS_Store
Thumbs.db
```

## 快速命令参考

```bash
# 1. 创建项目
npx create-video@latest my-video
cd my-video
npm install

# 2. 复制模板文件
cp /path/to/skill/scripts/ShotCard.tsx src/
cp /path/to/skill/scripts/index.tsx src/
cp /path/to/skill/scripts/data-template.json src/videoData.json

# 3. 创建图片目录
mkdir -p public/media

# 4. 预览视频
npm start
# 或
npx remotion studio

# 5. 渲染视频
npm run build
# 或
npx remotion render src/index.tsx Video out/output.mp4 --codec=h264

# 6. 渲染高质量版本
npx remotion render src/index.tsx Video out/output.mp4 \
  --codec=h264 \
  --crf=18 \
  --pixel-format=yuv420p

# 7. 渲染竖屏版本（抖音/快手）
npx remotion render src/index.tsx Video out/vertical.mp4 \
  --width=1080 \
  --height=1920 \
  --codec=h264
```

## 多场景项目结构

如果需要生成多个不同风格的视频：

```
my-videos/
├── src/
│   ├── components/
│   │   ├── NewsShot.tsx        # 新闻风格
│   │   ├── TutorialShot.tsx    # 教程风格
│   │   └── StoryShot.tsx       # 故事风格
│   ├── videos/
│   │   ├── news.tsx            # 新闻视频
│   │   ├── tutorial.tsx        # 教程视频
│   │   └── story.tsx           # 故事视频
│   └── data/
│       ├── newsData.json
│       ├── tutorialData.json
│       └── storyData.json
└── public/
    └── media/
        ├── news/
        ├── tutorial/
        └── story/
```
