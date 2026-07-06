import React from "react";
import { useCurrentFrame, useVideoConfig, interpolate, Easing, staticFile, Img } from "remotion";

interface ShotProps {
  subtitle: string;
  category: string;
  image: string;
  source: string;
  date: string;
  /** 裁剪锚点。人物是画面主体、原图头部没有留白时设为 "top"，
   * 避免 object-fit: cover 按中心裁剪把头部切掉——但这只是补救手段，
   * 选图时优先找 headroom 充足的构图才是根本，见 references/strict-verification.md */
  focalPoint?: "top" | "center" | "bottom";
}

export const ShotCard: React.FC<ShotProps> = ({
  subtitle,
  category,
  image,
  source,
  date,
  focalPoint = "center",
}) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();

  // 进场和退场动画
  const enter = interpolate(frame, [0, 0.3 * fps], [0, 1], {
    extrapolateRight: "clamp",
    easing: Easing.out(Easing.ease),
  });
  const holdUntil = durationInFrames - 0.3 * fps;
  const exit = interpolate(frame, [holdUntil, durationInFrames], [1, 0], {
    extrapolateLeft: "clamp",
    easing: Easing.in(Easing.ease),
  });
  const opacity = Math.min(enter, exit);

  // Ken Burns 效果 - 慢速缩放
  const scale = interpolate(frame, [0, durationInFrames], [1, 1.08], {
    extrapolateRight: "clamp",
    easing: Easing.inOut(Easing.ease),
  });

  return (
    <div
      style={{
        width: "100%",
        height: "100%",
        backgroundColor: "#0a1830",
        position: "relative",
        overflow: "hidden",
        fontFamily: "'Microsoft YaHei', 'PingFang SC', sans-serif",
      }}
    >
      {/* 背景层 - 真实图片 */}
      <Img
        src={staticFile(image)}
        style={{
          position: "absolute",
          width: "100%",
          height: "100%",
          objectFit: "cover",
          objectPosition: focalPoint === "top" ? "center top" : focalPoint === "bottom" ? "center bottom" : "center center",
          transform: `scale(${scale})`,
        }}
      />

      {/* 底部渐变遮罩 */}
      <div
        style={{
          position: "absolute",
          bottom: 0,
          left: 0,
          right: 0,
          height: "50%",
          background: "linear-gradient(to top, rgba(10,24,48,0.95) 0%, rgba(10,24,48,0) 100%)",
        }}
      />

      {/* 顶部类别标签 */}
      <div
        style={{
          position: "absolute",
          top: 30,
          left: 40,
          fontSize: 18,
          color: "#ffffff",
          backgroundColor: "rgba(232,184,75,0.2)",
          padding: "6px 16px",
          borderLeft: "3px solid #E8B84B",
          opacity,
        }}
      >
        {category}
      </div>

      {/* 顶部日期 — 来自数据，而非渲染时的系统时间：
          Remotion 要求每帧渲染必须是确定性的，new Date() 在渲染期间
          取到的是"当前系统时间"，同一份视频重新渲染会得到不同结果 */}
      <div
        style={{
          position: "absolute",
          top: 30,
          right: 40,
          fontSize: 16,
          color: "#aaaaaa",
          opacity,
        }}
      >
        {date}
      </div>

      {/* 底部字幕条 */}
      <div
        style={{
          position: "absolute",
          bottom: 60,
          left: "50%",
          transform: `translateX(-50%)`,
          width: "85%",
          backgroundColor: "rgba(0,0,0,0.75)",
          padding: "20px 40px",
          textAlign: "center",
          opacity,
        }}
      >
        <div
          style={{
            fontSize: 34,
            fontWeight: "bold",
            color: "#ffffff",
            lineHeight: 1.4,
          }}
        >
          {subtitle}
        </div>
      </div>

      {/* 来源标注 */}
      <div
        style={{
          position: "absolute",
          bottom: 20,
          left: 40,
          fontSize: 16,
          color: "#aaaaaa",
          opacity,
        }}
      >
        来源：{source}
      </div>
    </div>
  );
};
