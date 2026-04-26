---
name: Remotion動画編集スキル
description: Remotionコンポーネント（Ken Burns効果・分割テロップ・音声同期）を使ったYouTube動画の編集
---

# Remotion動画編集スキル

## スキル概要

Remotionフレームワークを使い、画像 + 音声 + テロップを組み合わせたYouTube動画を編集する。異世界漫画プロジェクトのコンポーネント構成を参照し、Ken Burns効果・フルテロップ分割表示・音声Sequence同期を実装。

## 前提条件

- Node.js + npm がインストール済み
- Remotionプロジェクトが `c:\Obsidian Vault\demo\03_Remotion\` に存在
- 画像が `public/images/`、音声が `public/audio/` に配置済み

## アーキテクチャ

### ファイル構成

```
03_Remotion/
├── src/
│   ├── Root.tsx          # エントリーポイント（Composition登録）
│   ├── DemoVideo.tsx     # メインコンポーネント
│   └── data/
│       └── demo_seminar_layout.json  # レイアウト定義
├── public/
│   ├── images/           # 画像ファイル
│   └── audio/            # 音声ファイル
└── out/                  # レンダリング出力
```

### コンポーネント構成

```
DemoVideo（メイン）
├── Sequence（パネル表示）
│   └── DemoPanel
│       ├── AbsoluteFill（Ken Burns画像）
│       └── Sequence × N（テロップセグメント）
│           └── TelopSegmentView
└── Sequence（音声 — 分離管理）
    └── Audio
```

> [!IMPORTANT]
> 音声は**パネルのSequenceとは別のSequence**に分離する。
> これが異世界漫画プロジェクトのTestVideo.tsx方式であり、音声-テロップ同期の核心。

## レイアウトJSON仕様

```json
{
    "title": "動画タイトル",
    "fps": 30,
    "width": 1920,
    "height": 1080,
    "panels": [
        {
            "id": "P1",
            "title": "パネル名",
            "image": "画像ファイル名.png",
            "startFrame": 0,
            "durationFrames": 340,
            "kenBurns": {
                "scaleStart": 1.0,
                "scaleEnd": 1.05,
                "xStart": 0, "xEnd": 0,
                "yStart": 0, "yEnd": -2
            },
            "telopSegments": [
                {
                    "text": "テロップ前半",
                    "startFrame": 0,
                    "durationFrames": 103
                },
                {
                    "text": "テロップ後半",
                    "startFrame": 103,
                    "durationFrames": 237
                }
            ],
            "audio": "音声ファイル名.mp3",
            "audioDurationSec": 10.6
        }
    ]
}
```

### telopSegments のルール

1. `startFrame` / `durationFrames` は**パネル内の相対フレーム**（パネル開始が0F）
2. テキストが20文字以下なら分割不要（1セグメント）
3. 分割点は句読点（。？）のタイムスタンプから計算
4. フォントサイズは60px固定（分割により大きさを維持）
5. `whiteSpace: "pre-line"` で明示的改行（`\n`）に対応

## テロップの実装

### スタイル仕様（異世界漫画Telop.tsx準拠）

```tsx
// テロップ帯
background: "linear-gradient(to top, rgba(0,0,0,0.90) 0%, rgba(0,0,0,0.78) 55%, rgba(0,0,0,0) 100%)"
padding: "50px 80px 48px 80px"
minHeight: "180px"
zIndex: 100

// テキスト
fontSize: 60
fontWeight: 800
fontFamily: "'Noto Sans JP', 'Hiragino Kaku Gothic ProN', 'Yu Gothic', sans-serif"
textShadow: "0 2px 8px rgba(0,0,0,0.8), 0 0px 2px rgba(0,0,0,0.9)"
WebkitTextStroke: "1px rgba(0,0,0,0.3)"
```

### フェードイン/アウト

- フェードイン: 10フレーム（Easing.out cubic）
- フェードアウト: 最後6フレーム
- スライドイン: 下から15px

## Ken Burns効果

```tsx
const progress = interpolate(frame, [0, durationFrames], [0, 1], {
    extrapolateRight: "clamp",
});
const scale = interpolate(progress, [0, 1], [scaleStart, scaleEnd]);
const translateX = interpolate(progress, [0, 1], [xStart, xEnd]);
const translateY = interpolate(progress, [0, 1], [yStart, yEnd]);
```

推奨値:
- ゆっくりズームイン: `scaleStart: 1.0 → scaleEnd: 1.05`
- 横パン: `xStart: -5 → xEnd: 5`
- 感情的なシーン: `scaleEnd: 1.08`（大きめズーム）

## 参考プロジェクト

- [異世界漫画 Remotion](file:///c:/Obsidian%20Vault/異世界漫画/05_Remotion/) — 元となるアーキテクチャ
  - [Telop.tsx](file:///c:/Obsidian%20Vault/異世界漫画/05_Remotion/src/components/Telop.tsx)
  - [TestPanel.tsx](file:///c:/Obsidian%20Vault/異世界漫画/05_Remotion/src/components/TestPanel.tsx)
  - [TestVideo.tsx](file:///c:/Obsidian%20Vault/異世界漫画/05_Remotion/src/TestVideo.tsx)
- [AI動画編集自動化ツール](file:///c:/Obsidian%20Vault/🔧_ツール/AI動画編集自動化ツール/) — Root.tsx構成の参考
- [老後資金チャンネル制作パイプライン](file:///c:/Obsidian%20Vault/老後資金チャンネル_制作パイプライン/remotion-project/) — calculateMetadata方式
