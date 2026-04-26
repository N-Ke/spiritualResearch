import React from "react";
import { AbsoluteFill, useCurrentFrame, useVideoConfig, Img, staticFile, interpolate, Sequence } from "remotion";
import { Panel } from "../types";
import { TelopSegmentView } from "./TelopSegmentView";

export const DemoPanel: React.FC<{ panel: Panel }> = ({ panel }) => {
  const frame = useCurrentFrame();
  const { durationFrames } = panel;

  // Ken Burns 効果
  const { scaleStart, scaleEnd, xStart, xEnd, yStart, yEnd } = panel.kenBurns;
  
  const progress = interpolate(frame, [0, durationFrames], [0, 1], {
    extrapolateRight: "clamp",
  });
  
  const scale = interpolate(progress, [0, 1], [scaleStart, scaleEnd]);
  const translateX = interpolate(progress, [0, 1], [xStart, xEnd]);
  const translateY = interpolate(progress, [0, 1], [yStart, yEnd]);

  return (
    <AbsoluteFill style={{ backgroundColor: "#000" }}>
      {/* 1. 背景画像（Ken Burns） */}
      <AbsoluteFill style={{ overflow: "hidden" }}>
        <Img
          src={staticFile(`images/${panel.image}`)}
          style={{
            width: "100%",
            height: "100%",
            objectFit: "cover",
            transform: `scale(${scale}) translate(${translateX}%, ${translateY}%)`,
            transformOrigin: "center center",
          }}
        />
      </AbsoluteFill>

      {/* 2. テロップセグメント（完全にパネル相対のSequenceで表示） */}
      {panel.telopSegments.map((segment, idx) => (
        <Sequence
          key={`telop-${idx}`}
          from={segment.startFrame}
          durationInFrames={segment.durationFrames}
        >
          <TelopSegmentView segment={segment} />
        </Sequence>
      ))}
    </AbsoluteFill>
  );
};
