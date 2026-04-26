---
name: Remotion動画編集スキル（Mac版）
description: Remotionコンポーネント（Ken Burns効果・テロップ・音声同期・トランジション）を使ったYouTube動画編集。Mac環境専用。
---

# Remotion動画編集スキル（Mac版）

## スキル概要

Remotionフレームワークを使い、画像 + 音声 + テロップを組み合わせたYouTube動画を編集する。manga-video-remotionプロジェクトのコンポーネント構成をベースに、Ken Burns効果・テロップ自動分割・音声同期・シーントランジションを実装。

> [!CAUTION]
> **Mac版制約**: このスキルはMac環境向け。Windows版は `03_Remotion/` を使用すること。

## 前提条件

- Node.js + npm がインストール済み（`node -v` で確認）
- `npm install` 実行済み

## アーキテクチャ

```
03_Remotion_Mac/
├── src/
│   ├── index.ts          # エントリーポイント
│   ├── Root.tsx           # Composition登録
│   ├── MangaVideo.tsx     # メインコンポーネント（TransitionSeries + Audio）
│   ├── types.ts           # 型定義
│   ├── components/
│   │   ├── MangaScene.tsx     # Ken Burns + 画像 + Caption
│   │   ├── Caption.tsx        # テロップ（日本語自動改行）
│   │   ├── BlackPause.tsx     # 黒画面
│   │   ├── SfxText.tsx        # 擬音テキスト
│   │   ├── Inset.tsx          # インセット
│   │   ├── ConcentrationLines.tsx
│   │   └── Vignette.tsx
│   └── scenes/
│       └── adsense_scene1.ts  # シーンデータ定義
├── public/
│   ├── images/            # 画像ファイル
│   └── audio/             # 音声ファイル
└── out/                   # レンダリング出力
```

## 実行手順

### Step 1: プレビュー（Remotion Studio）

```bash
cd ~/Documents/Obsidian\ Vault/demo/03_Remotion_Mac
npm run studio
```
→ ブラウザで http://localhost:3000 が開きプレビュー可能

### Step 2: MP4レンダリング

```bash
npm run render
```
→ `out/adsense_scene1.mp4` が生成される

### シーンの追加方法

1. `src/scenes/` に新しい `.ts` ファイルを作成
2. `MangaVideoData` 型に沿ってシーンデータを定義
3. `src/Root.tsx` に新しい `<Composition>` を追加

## 注意事項

- Folder名はASCIIのみ（日本語不可）
- 画像は `public/images/`、音声は `public/audio/` に配置
- Ken Burns の `intensity` は 1.03〜1.08 が推奨
- テロップは28文字で自動改行（句読点・助詞位置優先）
