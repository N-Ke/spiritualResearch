---
name: YouTube動画生成パイプラインスキル
description: 台本から画像生成→音声生成→テロップ同期→Remotionレンダリングまでの一気通貫パイプライン
---

# YouTube動画生成パイプラインスキル

## スキル概要

台本（.md）を入力として、画像生成 → 音声生成 → テロップ同期 → Remotionレンダリングまでを一気通貫で実行し、YouTube用MP4動画を生成する統合パイプライン。

## 前提条件

- 画像生成スキル（`demo/01_画像生成/SKILL.md`）の前提条件を満たすこと
- 音声生成スキル（`demo/02_音声生成/SKILL.md`）の前提条件を満たすこと
- 動画編集スキル（`demo/03_Remotion/SKILL.md`）の前提条件を満たすこと

## パイプライン全体像

```
台本（.md）
    │
    ▼
Phase 1: シーン分割・プロンプト設計
    │
    ▼
Phase 2: 画像生成（NanoBanana Pro API）
    │  → public/images/ に出力
    ▼
Phase 3: 音声生成 + タイムスタンプ取得（ElevenLabs API）
    │  → public/audio/ に出力
    │  → テロップ分割フレームを計算
    ▼
Phase 4: レイアウトJSON生成（フレーム精度テロップ同期）
    │  → src/data/ に出力
    ▼
Phase 5: Remotionレンダリング
    │  → out/ にMP4出力
    ▼
完成動画（1920x1080、30fps）
```

## 実行手順

### Phase 1: シーン分割・プロンプト設計

台本から冒頭30秒（または指定範囲）のシーンを分割:

1. 台本を読み込む
2. ナレーション・セリフの区切りでシーン（パネル）に分割
3. 各シーンに対して以下を定義:
   - 画像プロンプト（harumiスタイル + 具体的なシーン描写）
   - 音声テキスト（話者・感情指定）
   - キャラクター / voice_id の割り当て

### Phase 2: 画像生成

→ **画像生成スキル（`01_画像生成/SKILL.md`）を参照**

```bash
cd demo/01_画像生成
python generate_pension_scenes.py
```

### Phase 3: 音声生成 + タイムスタンプ同期

→ **音声生成スキル（`02_音声生成/SKILL.md`）を参照**

```bash
# Step 1: 音声生成 + タイムスタンプ取得 + レイアウト自動更新
cd demo/02_音声生成
python sync_telop_timestamps.py
```

> [!IMPORTANT]
> `sync_telop_timestamps.py` は音声生成とレイアウトJSON更新を同時に行う。
> 別々に実行すると音声とタイムスタンプがズレる。

### Phase 4: レイアウトJSON確認

自動生成されたレイアウトJSONを確認:
- 空テキストのtelopSegmentsがないか
- durationFramesがパネルの範囲内か
- startFrameの順序が正しいか

### Phase 5: Remotionレンダリング

→ **動画編集スキル（`03_Remotion/SKILL.md`）を参照**

```bash
cd demo/03_Remotion

# TypeScriptビルド確認
npx tsc --noEmit

# レンダリング実行
npx remotion render DemoVideo out/demo_pension_30s.mp4 --overwrite
```

## ディレクトリ構成

```
demo/
├── 01_画像生成/
│   ├── SKILL.md                    # 画像生成スキル
│   ├── generate_pension_scenes.py  # 画像生成スクリプト
│   └── regen_split_image.py        # 個別画像再生成
├── 02_音声生成/
│   ├── SKILL.md                    # 音声生成スキル
│   ├── generate_pension_voice.py   # 基本音声生成
│   └── sync_telop_timestamps.py   # タイムスタンプ同期
├── 03_Remotion/
│   ├── SKILL.md                    # 動画編集スキル
│   ├── src/
│   │   ├── Root.tsx               # Composition登録
│   │   ├── DemoVideo.tsx          # メインコンポーネント
│   │   └── data/
│   │       └── demo_seminar_layout.json
│   ├── public/
│   │   ├── images/                # 生成画像
│   │   └── audio/                 # 生成音声
│   └── out/
│       └── demo_pension_30s.mp4   # 出力動画
├── 05_設定/
│   └── .env.example               # API Key設定例
└── テスト台本_3回目_2026年年金新ルール.md
```

## トラブルシューティング

| 問題 | 原因 | 対処 |
|------|------|------|
| 画像が正方形 | プロンプトに16:9指定がない | `LANDSCAPE 16:9 widescreen` を必ず含める |
| `ImageGenerationModel` not found | 間違ったAPI方式 | `GenerativeModel` + `generate_content` を使う |
| テロップが表示されない | zIndexの問題 | テロップにzIndex:100、画像はzIndex指定なし |
| 音声とテロップがズレる | 別々にAPI呼び出し | `sync_telop_timestamps.py` で同一コールから取得 |
| `ELEVENLABS_API_KEY` 未設定 | .envの読み込み順 | 全.envをbreakせず読み込む（`override=False`） |
| TypeScriptエラー | 既存コンポーネントの型不一致 | DemoVideoのみのRoot.tsxにする |

## 品質チェックリスト

- [ ] 画像が全て16:9（比率≈1.78〜1.79）
- [ ] キャラクターの年齢が台本に合っている
- [ ] テロップが音声に完全同期している
- [ ] テロップのフォントサイズが十分大きい（60px固定）
- [ ] パネル間で音声が被らない（ギャップあり）
- [ ] Ken Burns効果が自然に動いている
- [ ] 動画の冒頭と末尾が黒画面で切れていない
