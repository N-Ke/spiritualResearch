import { z } from "zod";

// シーンのテンポ設定
export type TempoType = "slow" | "normal" | "fast" | "dramatic";

// 小窓（インセット）の形状
export type InsetShape = "rectangle" | "jagged" | "star" | "explosion" | "circle";

// 描き文字（擬音）- モダンな演出
export interface SfxText {
  text: string;
  position: { x: number; y: number }; // 0-1の相対位置
  size: number;
  color: string;
  rotation: number;
  // モダンな演出タイプ
  animation: "impact" | "tension" | "subtle" | "fade_in" | "glitch";
  startSec: number;
  durationSec: number;
  // オプション：スタイル調整
  style?: "bold" | "thin" | "distorted";
  opacity?: number; // 0-1 (薄く表示する場合)
}

// インセット（小窓）
export interface Inset {
  imagePath: string;
  shape: InsetShape;
  position: "top-left" | "top-right" | "bottom-left" | "bottom-right" | "center";
  scale: number; // 0.2-0.5
  startSec: number;
  durationSec: number;
  animation: "pop" | "slide" | "fade";
}

// シーン
export interface MangaScene {
  id: string;
  imagePath: string;
  durationSec: number;
  tempo: TempoType;
  kenBurns?: {
    type: "zoom_in" | "zoom_out" | "pan_left" | "pan_right" | "pan_up" | "pan_down";
    intensity: number; // 1.0-1.3
  };
  sfxTexts?: SfxText[];
  insets?: Inset[];
  caption?: {
    text: string;
    startSec: number;
  };
  transition?: "fade" | "slide" | "wipe" | "none";
  transitionDurationSec?: number;
  // 集中線
  concentrationLines?: boolean;
  // ビネット（周辺減光）
  vignette?: number; // 0-1
  // 黒画面挿入（間）
  pauseBefore?: number; // 秒
}

// オーディオレイヤー（SE/BGM）
export interface AudioLayer {
  id: string;
  type: "bgm" | "ambience" | "se";
  path: string;
  startSec: number;
  durationSec?: number; // 省略時はファイル全体
  volume: number; // 0-1
  fadeIn?: number; // 秒
  fadeOut?: number; // 秒
  loop?: boolean;
}

// 動画全体
export interface MangaVideoData {
  title: string;
  scenes: MangaScene[];
  audioPath?: string; // ナレーション
  audioLayers?: AudioLayer[]; // BGM/SE
  globalCaption?: {
    font: string;
    fontSize: number;
    color: string;
    backgroundColor: string;
  };
}

// Zod schema for Remotion props validation
export const mangaVideoSchema = z.object({
  title: z.string(),
  scenes: z.array(z.object({
    id: z.string(),
    imagePath: z.string(),
    durationSec: z.number(),
    tempo: z.enum(["slow", "normal", "fast", "dramatic"]),
    kenBurns: z.object({
      type: z.enum(["zoom_in", "zoom_out", "pan_left", "pan_right", "pan_up", "pan_down"]),
      intensity: z.number(),
    }).optional(),
    sfxTexts: z.array(z.object({
      text: z.string(),
      position: z.object({ x: z.number(), y: z.number() }),
      size: z.number(),
      color: z.string(),
      rotation: z.number(),
      animation: z.enum(["impact", "tension", "subtle", "fade_in", "glitch"]),
      startSec: z.number(),
      durationSec: z.number(),
      style: z.enum(["bold", "thin", "distorted"]).optional(),
      opacity: z.number().optional(),
    })).optional(),
    insets: z.array(z.object({
      imagePath: z.string(),
      shape: z.enum(["rectangle", "jagged", "star", "explosion", "circle"]),
      position: z.enum(["top-left", "top-right", "bottom-left", "bottom-right", "center"]),
      scale: z.number(),
      startSec: z.number(),
      durationSec: z.number(),
      animation: z.enum(["pop", "slide", "fade"]),
    })).optional(),
    caption: z.object({
      text: z.string(),
      startSec: z.number(),
    }).optional(),
    transition: z.enum(["fade", "slide", "wipe", "none"]).optional(),
    transitionDurationSec: z.number().optional(),
    concentrationLines: z.boolean().optional(),
    vignette: z.number().optional(),
    pauseBefore: z.number().optional(),
  })),
  audioPath: z.string().optional(),
  audioLayers: z.array(z.object({
    id: z.string(),
    type: z.enum(["bgm", "ambience", "se"]),
    path: z.string(),
    startSec: z.number(),
    durationSec: z.number().optional(),
    volume: z.number(),
    fadeIn: z.number().optional(),
    fadeOut: z.number().optional(),
    loop: z.boolean().optional(),
  })).optional(),
  globalCaption: z.object({
    font: z.string(),
    fontSize: z.number(),
    color: z.string(),
    backgroundColor: z.string(),
  }).optional(),
});

// デフォルトデータ（実際のタイミングとテキスト - captions.assから取得）
export const defaultMangaData: MangaVideoData = {
  title: "債権回収_産廃業者の罠",
  audioPath: "audio/narration.wav",
  scenes: [
    {
      id: "scene_01",
      imagePath: "images/scene_01.png",
      durationSec: 8.67,  // 0:00:00.00 - 0:00:08.67
      tempo: "normal",
      kenBurns: { type: "pan_up", intensity: 1.08 },
      caption: { 
        text: "東京、新橋。雑居ビルの三階、看板には「桐生ファイナンス」の文字が剥げかけている。", 
        startSec: 0 
      },
      transition: "fade",
      transitionDurationSec: 0.3,
    },
    {
      id: "scene_02",
      imagePath: "images/scene_02.png",
      durationSec: 12.67,  // 0:00:08.67 - 0:00:21.34
      tempo: "slow",
      kenBurns: { type: "zoom_in", intensity: 1.1 },
      caption: { 
        text: "午後三時。扉を開けて入ってきたのは、作業着姿の男、相沢誠。四十代半ば、日焼けした顔には深い皺が刻まれている。", 
        startSec: 0 
      },
      pauseBefore: 0.3,
      transition: "fade",
      transitionDurationSec: 0.3,
    },
    {
      id: "scene_03",
      imagePath: "images/scene_03.png",
      durationSec: 10.03,  // 0:00:21.34 - 0:00:31.37
      tempo: "dramatic",
      kenBurns: { type: "zoom_in", intensity: 1.18 },
      // モダンな演出：控えめで緊張感のある描き文字
      sfxTexts: [
        {
          text: "...",
          position: { x: 0.08, y: 0.25 },
          size: 50,
          color: "rgba(255,255,255,0.6)",
          rotation: 0,
          animation: "tension",
          startSec: 1.0,
          durationSec: 4,
          opacity: 0.5,
          style: "thin",
        },
      ],
      concentrationLines: true,
      vignette: 0.5,
      caption: { 
        text: "奥のデスクから立ち上がったのは、桐生蓮。黒いスーツに身を包み、鋭い眼光で相沢を見据える。", 
        startSec: 0 
      },
      // インセットは削除（古臭い印象を避ける）
      transition: "fade",
      transitionDurationSec: 0.3,
    },
    {
      id: "scene_04",
      imagePath: "images/scene_04.png",
      durationSec: 10.84,  // 0:00:31.37 - 0:00:42.21
      tempo: "fast",
      kenBurns: { type: "zoom_in", intensity: 1.06 },
      // 「ドクン」→ より控えめな「...」に変更（直接的な心音表現を避ける）
      // 緊張感は音（SE）とビネットで表現すべき
      vignette: 0.3,
      caption: { 
        text: "相沢は震える手で封筒を差し出した。中には一枚の請求書。金額は、八百五十万円。", 
        startSec: 0 
      },
      transition: "fade",
      transitionDurationSec: 0.3,
    },
    {
      id: "scene_05",
      imagePath: "images/scene_05.png",
      durationSec: 8.98,  // 0:00:42.21 - 0:00:51.19
      tempo: "normal",
      kenBurns: { type: "pan_left", intensity: 1.08 },
      caption: { 
        text: "「これ、見ていただけますか。産廃処理業者の神山産業から、突然送られてきたんです」", 
        startSec: 0 
      },
    },
  ],
  globalCaption: {
    font: "Hiragino Sans",
    fontSize: 56,
    color: "#FFFFFF",
    backgroundColor: "rgba(40, 40, 40, 0.7)",
  },
  // オーディオレイヤー（SE/BGM）
  audioLayers: [
    // 環境音：オフィスの静寂（全体に薄く）
    {
      id: "ambience_office",
      type: "ambience",
      path: "se/office_ambience.mp3",
      startSec: 0,
      volume: 0.15,
      fadeIn: 2,
      loop: true,
    },
    // シーン3: 緊張ドローン（桐生登場）
    {
      id: "tension_scene3",
      type: "se",
      path: "se/tension_drone.mp3",
      startSec: 21.5,  // シーン3開始
      volume: 0.25,
      fadeIn: 1,
      fadeOut: 1,
    },
    // シーン3: Riser（緊張の高まり）
    {
      id: "riser_scene3",
      type: "se",
      path: "se/riser.mp3",
      startSec: 28,  // シーン3終盤
      volume: 0.3,
    },
    // シーン4開始: インパクト
    {
      id: "impact_scene4",
      type: "se",
      path: "se/impact.mp3",
      startSec: 31.5,  // シーン4開始
      volume: 0.35,
    },
  ],
};
