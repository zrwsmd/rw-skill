import React from "react";
import { Composition, registerRoot, Sequence } from "remotion";
import { ShotCard } from "./ShotCard";
import videoData from "./videoData.json";

// Single source of truth for fps — used by the frame-count math below AND
// passed to <Composition>. Previously this was hardcoded in three places
// (Video's local var, the totalDuration reduce, and the Composition prop),
// which made it easy for them to drift out of sync if one got edited alone.
const FPS = 30;

const Video: React.FC = () => {
  let currentFrame = 0;

  return (
    <div style={{ width: "100%", height: "100%", backgroundColor: "#000" }}>
      {videoData.segments.map((segment) => {
        return segment.shots.map((shot, shotIndex) => {
          const durationInFrames = shot.durationSeconds * FPS;
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
                date={videoData.date}
                focalPoint={shot.focalPoint as "top" | "center" | "bottom" | undefined}
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
      sum + segment.shots.reduce((shotSum, shot) => shotSum + shot.durationSeconds * FPS, 0),
    0
  );

  return (
    <>
      <Composition
        id="Video"
        component={Video}
        durationInFrames={totalDuration}
        fps={FPS}
        width={1920}
        height={1080}
      />
    </>
  );
};

registerRoot(RemotionRoot);
