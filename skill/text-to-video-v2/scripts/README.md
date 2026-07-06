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
- date: 视频对应的日期（顶部日期标注用，作为 prop 传给每个镜头，不要在组件里用 `new Date()` 现取系统时间——那样每次重新渲染同一份视频，日期都会跟着变，破坏 Remotion 要求的渲染确定性）
- segments: 视频片段数组
- shots: 每个片段的镜头数组
  - image / subtitle / durationSeconds：基本配置
  - focalPoint（可选，"top" | "center" | "bottom"，默认 "center"）：图片裁剪锚点。人物是画面主体、原图头部没有 headroom 时设为 "top"，避免铺满画框时把头切掉——但这只是补救手段，选图时优先找构图安全的图，见 `references/strict-verification.md` 第5节

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

### 人物头部被裁掉
检查：
- 原图人物头部到图片上边缘是否有留白（headroom）——没有的话优先换图
- 是否需要给这个镜头的 shot 数据加 `"focalPoint": "top"`
- 渲染一帧静帧实际看一下裁剪结果，不要只凭原图判断（详见 `references/strict-verification.md` 第5节）
