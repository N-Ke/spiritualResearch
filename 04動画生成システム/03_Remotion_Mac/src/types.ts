// types.ts
export interface TelopSegment {
  text: string;
  startFrame: number;
  durationFrames: number;
}

export interface KenBurns {
  scaleStart: number;
  scaleEnd: number;
  xStart: number;
  xEnd: number;
  yStart: number;
  yEnd: number;
}

export interface Panel {
  id: string;
  title: string;
  image: string;
  startFrame: number;
  durationFrames: number;
  kenBurns: KenBurns;
  telopSegments: TelopSegment[];
  audio: string;
  audioDurationSec: number;
}

export interface VideoLayout {
  title: string;
  fps: number;
  width: number;
  height: number;
  panels: Panel[];
}
