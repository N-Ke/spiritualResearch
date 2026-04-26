import React from "react";
import { AbsoluteFill, Sequence, Audio, staticFile } from "remotion";
import { VideoLayout } from "./types";
import { DemoPanel } from "./components/DemoPanel";

export const DemoVideo: React.FC<{ layout: VideoLayout }> = ({ layout }) => {
  return (
    <AbsoluteFill style={{ backgroundColor: "#000" }}>
      {/* 1. パネル（画像とテロップ）のSequence */}
      {layout.panels.map((panel) => (
        <Sequence
          key={panel.id}
          from={panel.startFrame}
          durationInFrames={panel.durationFrames}
        >
          <DemoPanel panel={panel} />
        </Sequence>
      ))}

      {/* 2. 音声のSequence（画像/テロップとは完全に独立して再生） */}
      {layout.panels.map((panel) => {
        if (!panel.audio) return null;
        
        return (
          <Sequence
            key={`audio-${panel.id}`}
            from={panel.startFrame}
            // 音声はパネルのdurationに関わらず1つのトラックとして開始
          >
            <Audio src={staticFile(`audio/${panel.audio}`)} volume={1} />
          </Sequence>
        );
      })}
    </AbsoluteFill>
  );
};
