# 故障排查指南

## 常见问题和解决方案

### 1. 渲染问题

#### 黑屏问题

**症状**: 视频渲染后全是黑屏，没有图片显示

**原因**:
- 图片路径不正确
- 图片不在 `public/media/` 目录
- 没有使用 `staticFile()` API

**解决方案**:
```typescript
// ❌ 错误写法
<img src="media/image.jpg" />
<img src="./media/image.jpg" />
<img src="/media/image.jpg" />

// ✅ 正确写法
<Img src={staticFile("media/image.jpg")} />
```

**检查步骤**:
1. 确认图片存在: `ls public/media/`
2. 确认路径匹配: 检查 `videoData.json` 中的路径
3. 确认使用了 `staticFile()` API

---

#### JSON 解析错误

**症状**: 运行时报错 `Unexpected token` 或 `JSON parse error`

**原因**:
- 使用了中文引号 `""`
- JSON 格式不正确（多余逗号、缺少引号）

**解决方案**:
```json
// ❌ 错误：中文引号
{
  "subtitle": "习近平向"七一勋章"获得者颁授勋章"
}

// ✅ 正确：英文引号
{
  "subtitle": "习近平向七一勋章获得者颁授勋章"
}

// ❌ 错误：多余逗号
{
  "durationSeconds": 4,
}

// ✅ 正确：去掉最后的逗号
{
  "durationSeconds": 4
}
```

**检查步骤**:
1. 用 VSCode 打开 JSON 文件，检查是否有红色波浪线
2. 运行: `node -e "require('./src/videoData.json')"`
3. 在线验证: https://jsonlint.com/

---

#### 渲染速度慢

**症状**: 渲染一个1分钟视频需要10分钟以上

**原因**:
- 图片文件太大（> 5MB）
- 图片分辨率过高（> 4K）
- 电脑性能不足

**解决方案**:

1. **压缩图片**:
```bash
# 使用 ImageMagick 批量压缩
mogrify -resize 1920x1080 -quality 85 public/media/*.jpg

# 或使用在线工具
# https://tinypng.com/
# https://squoosh.app/
```

2. **降低渲染质量**:
```bash
# 使用较低的 CRF 值（文件更小）
npx remotion render src/index.tsx Video out/output.mp4 --crf=28
```

3. **使用并行渲染**:
```bash
npx remotion render src/index.tsx Video out/output.mp4 --concurrency=4
```

---

### 2. 显示问题

#### 字幕看不清

**症状**: 字幕文字模糊或被背景淹没

**解决方案**:
```typescript
// 增加背景遮罩透明度
backgroundColor: "rgba(0,0,0,0.85)"  // 从 0.75 增加到 0.85

// 增加字体粗细
fontWeight: "bold"  // 或 "900"

// 添加文字阴影
textShadow: "2px 2px 4px rgba(0,0,0,0.8)"
```

---

#### 图片显示不完整

**症状**: 图片被裁剪或变形

**解决方案**:
```typescript
// 使用 objectFit: "cover" 保持宽高比
<Img
  src={staticFile(image)}
  style={{
    objectFit: "cover",  // 保持比例，填满区域
    // objectFit: "contain",  // 保持比例，完整显示
  }}
/>
```

---

#### 日期显示错误

**症状**: 日期显示为 `Invalid Date` 或格式不正确

**解决方案**:
```typescript
// ✅ 正确写法
{new Date().toLocaleDateString('zh-CN', { 
  year: 'numeric', 
  month: 'long', 
  day: 'numeric' 
})}
// 输出: "2026年7月1日"

// 或手动指定
{"2026年7月1日"}
```

---

### 3. 安装问题

#### FFmpeg 找不到

**症状**: 渲染时报错 `FFmpeg not found`

**解决方案**:

**Windows**:
```bash
# 使用 Chocolatey 安装
choco install ffmpeg

# 或下载安装包
# https://ffmpeg.org/download.html
```

**macOS**:
```bash
brew install ffmpeg
```

**Linux**:
```bash
sudo apt-get install ffmpeg
```

---

#### npm install 失败

**症状**: `npm install` 报错或卡住

**解决方案**:
```bash
# 清理缓存
npm cache clean --force

# 删除 node_modules 重新安装
rm -rf node_modules package-lock.json
npm install

# 使用淘宝镜像（中国用户）
npm install --registry=https://registry.npmmirror.com
```

---

### 4. 代码问题

#### TypeScript 类型错误

**症状**: 编译时报 TypeScript 类型错误

**解决方案**:
```typescript
// 确保导入了正确的类型
import { Img } from "remotion";  // 不是 React 的 <img>

// 为 props 添加类型定义
interface ShotProps {
  subtitle: string;
  category: string;
  image: string;
  source: string;
}
```

---

#### 动画不流畅

**症状**: Ken Burns 效果卡顿或跳跃

**解决方案**:
```typescript
// 使用 Easing 函数
import { Easing } from "remotion";

const scale = interpolate(
  frame,
  [0, durationInFrames],
  [1, 1.08],
  {
    easing: Easing.inOut(Easing.ease),  // 添加缓动
  }
);
```

---

### 5. 输出问题

#### 视频无法播放

**症状**: 渲染成功但视频无法在某些设备播放

**解决方案**:
```bash
# 使用兼容性最好的编码参数
npx remotion render src/index.tsx Video out/output.mp4 \
  --codec=h264 \
  --pixel-format=yuv420p
```

---

#### 文件太大

**症状**: 生成的视频文件过大（> 50MB for 1min）

**解决方案**:
```bash
# 提高压缩率
npx remotion render src/index.tsx Video out/output.mp4 \
  --codec=h264 \
  --crf=28  # 默认是 18，数值越大文件越小

# 使用 H.265 编码（更高压缩率）
npx remotion render src/index.tsx Video out/output.mp4 \
  --codec=h265
```

---

## 调试技巧

### 1. 使用 Remotion Studio 预览

```bash
npx remotion studio
```
在浏览器中实时预览，可以看到每一帧的效果。

### 2. 检查单个镜头

在 `index.tsx` 中临时只保留一个镜头：
```typescript
// 临时注释掉其他镜头
{videoData.segments[0].shots.slice(0, 1).map(...)}
```

### 3. 输出调试信息

```typescript
console.log("当前帧:", frame);
console.log("总帧数:", durationInFrames);
console.log("缩放比例:", scale);
```

### 4. 检查文件路径

```bash
# 列出所有图片
ls -la public/media/

# 检查 JSON 中的路径
cat src/videoData.json | grep "image"
```

---

## 获取帮助

如果以上方法都无法解决问题：

1. **查看 Remotion 官方文档**: https://www.remotion.dev/docs
2. **搜索问题**: 在 GitHub Issues 搜索类似问题
3. **提问社区**: 
   - Remotion Discord: https://remotion.dev/discord
   - Stack Overflow: 标签 `remotion`
4. **检查日志**: 仔细阅读错误信息，通常会指出问题所在

---

## 快速诊断命令

```bash
# 检查 Node 版本（需要 >= 16）
node --version

# 检查 FFmpeg 是否安装
ffmpeg -version

# 检查项目依赖
npm list remotion

# 检查图片文件
ls -lh public/media/

# 验证 JSON 格式
node -e "console.log(require('./src/videoData.json'))"

# 清理并重新安装
rm -rf node_modules package-lock.json .remotion
npm install
```
