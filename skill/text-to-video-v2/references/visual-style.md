# 视觉风格设计指南

字幕、布局、动画的视觉设计规范。

## 整体风格

### 电视新闻风格（默认）

- 底部字幕条（黑色半透明背景）
- 顶部类别标签 + 日期
- 左下角来源标注
- Ken Burns 缩放效果
- 简洁专业

适用场景：新闻、资讯、正式内容

### 教程风格

- 居中大字幕
- 步骤编号
- 明亮背景
- 箭头指示动画

适用场景：教程、讲解、演示

### 故事风格

- 上下字幕（影院风格）
- 黑边遮幅
- 慢速切换
- 情感化色调

适用场景：故事、纪录片、叙事内容

## 字幕设计

### 位置和尺寸

```typescript
// 底部居中字幕（新闻风格）
{
  position: "absolute",
  bottom: 60,
  left: "50%",
  transform: "translateX(-50%)",
  width: "85%",
  backgroundColor: "rgba(0,0,0,0.75)",
  padding: "20px 40px",
  textAlign: "center"
}
```

### 字体样式

```typescript
{
  fontSize: 34,              // 主字幕
  fontWeight: "bold",
  color: "#ffffff",
  lineHeight: 1.4,
  fontFamily: "'Microsoft YaHei', 'PingFang SC', sans-serif"
}
```

### 字幕长度

- **单行字幕**：最多 25 个汉字
- **双行字幕**：每行 15-20 个汉字
- **三行及以上**：避免，太拥挤

## 布局元素

### 1. 顶部类别标签

```typescript
{
  position: "absolute",
  top: 30,
  left: 40,
  fontSize: 18,
  color: "#ffffff",
  backgroundColor: "rgba(232,184,75,0.2)",  // 金色半透明
  padding: "6px 16px",
  borderLeft: "3px solid #E8B84B"           // 左侧金色边框
}
```

示例：`国内新闻` `国际新闻` `科技` `教程`

### 2. 日期标注

```typescript
{
  position: "absolute",
  top: 30,
  right: 40,
  fontSize: 16,
  color: "#aaaaaa"
}
```

格式：`2026年7月1日`

### 3. 来源标注

```typescript
{
  position: "absolute",
  bottom: 20,
  left: 40,
  fontSize: 16,
  color: "#aaaaaa"
}
```

格式：`来源：新华社` `来源：路透社`

### 4. 底部渐变遮罩

```typescript
{
  position: "absolute",
  bottom: 0,
  left: 0,
  right: 0,
  height: "50%",
  background: "linear-gradient(to top, rgba(10,24,48,0.95) 0%, rgba(10,24,48,0) 100%)"
}
```

作用：让底部字幕更清晰可读

## 动画效果

### Ken Burns 效果（图片缓慢放大）

```typescript
const scale = interpolate(
  frame,
  [0, durationInFrames],
  [1, 1.08],
  {
    extrapolateRight: "clamp",
    easing: Easing.inOut(Easing.ease),
  }
);

// 应用到图片
<Img style={{ transform: `scale(${scale})` }} />
```

效果：图片从 100% 缓慢放大到 108%，制造动态感

### 淡入淡出

```typescript
// 进场动画（前 0.3 秒）
const enter = interpolate(
  frame,
  [0, 0.3 * fps],
  [0, 1],
  {
    extrapolateRight: "clamp",
    easing: Easing.out(Easing.ease),
  }
);

// 退场动画（最后 0.3 秒）
const holdUntil = durationInFrames - 0.3 * fps;
const exit = interpolate(
  frame,
  [holdUntil, durationInFrames],
  [1, 0],
  {
    extrapolateLeft: "clamp",
    easing: Easing.in(Easing.ease),
  }
);

const opacity = Math.min(enter, exit);
```

效果：字幕和标签平滑淡入淡出

### 切换效果

```typescript
// 默认：直接切换（无过渡）
// 可选：交叉溶解（两个镜头重叠 0.5 秒）
```

## 色彩方案

### 新闻风格配色

```typescript
const colors = {
  background: "#0a1830",           // 深蓝背景（预览用）
  subtitleBg: "rgba(0,0,0,0.75)",  // 字幕背景
  subtitleText: "#ffffff",         // 字幕文字
  categoryBg: "rgba(232,184,75,0.2)", // 类别标签背景
  categoryBorder: "#E8B84B",       // 类别标签边框（金色）
  metaText: "#aaaaaa",             // 日期和来源（灰色）
  gradientStart: "rgba(10,24,48,0.95)",
  gradientEnd: "rgba(10,24,48,0)"
};
```

### 教程风格配色

```typescript
const colors = {
  background: "#f5f5f5",           // 浅灰背景
  subtitleBg: "rgba(255,255,255,0.9)", // 白色字幕背景
  subtitleText: "#333333",         // 深灰文字
  accent: "#2196F3",               // 蓝色强调色
  stepNumber: "#FF9800"            // 橙色步骤编号
};
```

### 故事风格配色

```typescript
const colors = {
  background: "#000000",           // 纯黑背景
  subtitleBg: "transparent",       // 无背景
  subtitleText: "#ffffff",         // 白色文字
  letterbox: "#000000"             // 黑边遮幅
};
```

## 分辨率和帧率

### 标准配置

```typescript
{
  width: 1920,
  height: 1080,
  fps: 30
}
```

### 高清配置

```typescript
{
  width: 2560,
  height: 1440,
  fps: 60
}
```

### 竖屏配置（抖音、快手）

```typescript
{
  width: 1080,
  height: 1920,
  fps: 30
}
```

## 响应式调整

### 竖屏模式调整

```typescript
const isPortrait = height > width;

const subtitleStyle = {
  bottom: isPortrait ? 200 : 60,    // 竖屏字幕上移
  width: isPortrait ? "90%" : "85%",
  fontSize: isPortrait ? 28 : 34,   // 竖屏字体缩小
};
```

## 常见布局

### 布局1：新闻播报

```
┌──────────────────────────────────┐
│ [国内新闻]            2026年7月1日 │ ← 顶部标签
│                                  │
│        [背景图片 + Ken Burns]      │ ← 主视觉区
│                                  │
│  ┌────────────────────────────┐  │
│  │   字幕内容字幕内容字幕内容    │  │ ← 底部字幕条
│  └────────────────────────────┘  │
│ 来源：新华社                      │ ← 来源标注
└──────────────────────────────────┘
```

### 布局2：教程讲解

```
┌──────────────────────────────────┐
│                                  │
│        [背景图片]                 │
│                                  │
│  ┌────────────────────────────┐  │
│  │   ① 第一步：准备材料         │  │ ← 居中编号字幕
│  └────────────────────────────┘  │
│                                  │
└──────────────────────────────────┘
```

### 布局3：故事叙述

```
┌──────────────────────────────────┐
│ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ │ ← 黑边遮幅
│                                  │
│        [背景图片]                 │
│                                  │
│         字幕内容字幕内容          │ ← 底部简洁字幕
│ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ │ ← 黑边遮幅
└──────────────────────────────────┘
```

## 最佳实践

### ✅ 推荐做法

- 字幕背景半透明，确保可读性
- 使用 Ken Burns 效果增加动感
- 统一配色方案
- 淡入淡出平滑过渡
- 重要信息用对比色突出

### ❌ 避免做法

- 字幕太小看不清
- 字幕颜色与背景对比度低
- 过度动画（旋转、飞入等花哨效果）
- 同时出现太多文字元素
- 不同镜头风格不统一

## 可访问性

### 字幕可读性

- 最小字号：28px（1080p）
- 对比度：至少 4.5:1（WCAG AA 标准）
- 背景遮罩：确保字幕与背景分离
- 行距：1.4 倍以上

### 色盲友好

避免仅用颜色传达信息，使用：
- 文字标签 + 颜色
- 图标 + 颜色
- 位置 + 颜色

## 输出设置

### MP4 编码参数

```bash
npx remotion render src/index.tsx Video out/output.mp4 \
  --codec=h264 \
  --crf=18 \
  --pixel-format=yuv420p
```

- `h264`：通用兼容性最好
- `crf=18`：高质量（范围 0-51，越小质量越高）
- `yuv420p`：兼容大多数播放器

### 文件大小优化

```bash
# 中等质量（文件更小）
--crf=23

# 压缩比更高
--codec=h265
```
