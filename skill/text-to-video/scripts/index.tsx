import React from "react";
import { Composition, registerRoot, Sequence } from "remotion";
import { ShotCard } from "./ShotCard";
import videoData from "./videoData.json";

const Video: React.FC = () => {
  const fps = 30;
  let currentFrame = 0;

  return (
    <div style={{ width: "100%", height: "100%", backgroundColor: "#000" }}>
      {videoData.segments.map((segment) => {
        return segment.shots.map((shot, shotIndex) => {
          const durationInFrames = shot.durationSeconds * fps;
          const sequence = (
            <Sequence
              key={`${segment.id}-shot${shotIndex}`}
              from={currentFrame}
              durationInFrames={durationInFrames}
            >
              <ShotCard
                subtitle={shot.subtitle}
                category={segment.category}
                image={shot.image}
                source={segment.source}
              />
            </Sequence>
          );
          currentFrame += durationInFrames;
          return sequence;
        });
      })}
    </div>
  );
};

export const RemotionRoot: React.FC = () => {
  // 计算总时长
  const totalDuration = videoData.segments.reduce(
    (sum, segment) =>
      sum + segment.shots.reduce((shotSum, shot) => shotSum + shot.durationSeconds * 30, 0),
    0
  );

  return (
    <>
      <Composition
        id="Video"
        component={Video}
        durationInFrames={totalDuration}
        fps={30}
        width={1920}
        height={1080}
      />
    </>
  );
};

registerRoot(RemotionRoot);
