# 代码模板说明

这个目录包含生成文字转视频项目所需的所有模板文件。

## 文件说明

### ShotCard.tsx
单个镜头组件模板，包含：
- Ken Burns 缩放效果
- 淡入淡出动画
- 电视新闻风格字幕布局
- 类别标签、日期、来源标注

### index.tsx
主视频组合文件模板，负责：
- 读取 videoData.json 数据
- 将所有镜头串联成完整视频
- 自动计算总时长
- 注册 Remotion 组合

### data-template.json
视频数据结构模板，定义：
- segments: 视频片段数组
- shots: 每个片段的镜头数组
- 图片路径、字幕、时长等配置

## 使用方法

### 1. 创建 Remotion 项目

```bash
npx create-video@latest my-video
cd my-video
npm install
```

### 2. 复制模板文件

将 `ShotCard.tsx` 和 `index.tsx` 复制到项目的 `src/` 目录：

```bash
cp ShotCard.tsx /path/to/my-video/src/
cp index.tsx /path/to/my-video/src/
```

### 3. 创建数据文件

将 `data-template.json` 复制为 `videoData.json`：

```bash
cp data-template.json /path/to/my-video/src/videoData.json
```

然后编辑 `videoData.json`，填入实际内容。

### 4. 准备图片素材

将图片放到 `public/media/` 目录：

```bash
mkdir -p /path/to/my-video/public/media
# 将图片复制到 public/media/ 目录
```

确保 `videoData.json` 中的图片路径与实际文件名一致。

### 5. 预览视频

```bash
npx remotion studio
```

### 6. 渲染视频

```bash
npx remotion render src/index.tsx Video out/output.mp4 --codec=h264
```

## 自定义样式

### 修改字幕样式

编辑 `ShotCard.tsx` 中的字幕样式：

```typescript
// 底部字幕条
<div style={{
  fontSize: 34,        // 字号
  fontWeight: "bold",  // 字重
  color: "#ffffff",    // 颜色
  // ...
}}>
```

### 修改布局位置

```typescript
// 字幕位置
bottom: 60,  // 距离底部距离
width: "85%", // 宽度

// 类别标签位置
top: 30,
left: 40,
```

### 修改动画效果

```typescript
// Ken Burns 缩放范围
const scale = interpolate(frame, [0, durationInFrames], [1, 1.08], {...});
//                                                          ↑    ↑
//                                                       起始  结束

// 淡入淡出时长
const enter = interpolate(frame, [0, 0.3 * fps], [0, 1], {...});
//                                      ↑
//                                   0.3 秒
```

## 注意事项

- 图片必须下载到本地 `public/media/` 目录
- 不要使用远程 URL 或相对路径
- JSON 文件中不要使用中文引号 `""`
- 确保所有图片路径与文件名匹配
- 字幕长度建议不超过 25 个汉字

## 故障排查

### 黑屏问题
检查：
- 图片是否存在于 `public/media/` 目录
- `videoData.json` 中的路径是否正确
- 使用 `staticFile("media/xxx.jpg")` 而不是直接路径

### JSON 解析错误
检查：
- 是否使用了中文引号 `""`
- JSON 格式是否正确
- 是否有多余的逗号

### 渲染卡住
检查：
- 图片文件是否太大（建议 < 5MB）
- 总时长是否过长
- 是否有语法错误
