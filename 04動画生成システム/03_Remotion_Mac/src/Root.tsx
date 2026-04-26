import { Composition, Folder } from "remotion";
import { DemoVideo } from "./DemoVideo";
import layout from "./data/demo_seminar_layout.json";

export const RemotionRoot: React.FC = () => {
  // 動画の総フレーム数（最後のパネルの終了フレーム）
  const durationInFrames = layout.panels.length > 0 
    ? layout.panels[layout.panels.length - 1].startFrame + layout.panels[layout.panels.length - 1].durationFrames 
    : 300;

  return (
    <>
      <Folder name="Isekai-Standard">
        <Composition
          id="DemoVideo"
          component={DemoVideo}
          durationInFrames={durationInFrames}
          fps={layout.fps}
          width={layout.width}
          height={layout.height}
          defaultProps={{
            layout: layout as any,
          }}
        />
      </Folder>
    </>
  );
};
