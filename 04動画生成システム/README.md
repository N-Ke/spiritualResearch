# 🎬 デモ環境 — 異世界漫画 制作ツール一式

このフォルダには、異世界漫画プロジェクトの制作ツールと素材がすべて格納されています。
画像生成→音声生成→Remotion動画生成の一連のフローをここから実行できます。

---

## 📁 フォルダ構成

```
demo/
├── 01_画像生成/        ← Nano Banana 2 で漫画イラスト生成
├── 02_音声生成/        ← ElevenLabs で音声生成
├── 03_Remotion/        ← Remotion で動画レンダリング
├── 04_素材/            ← 生成済みの画像・音声・SE・動画
└── 05_設定/            ← APIキー設定
```

---

## 🔧 セットアップ

### 1. APIキーの設定

`05_設定/.env.example` を `05_設定/.env` にリネームして、キーを設定：

```
GOOGLE_API_KEY=あなたのGoogleAPIキー
ELEVENLABS_API_KEY=あなたのElevenLabsAPIキー
```

> **Note**: `X_Post_System/2_Config/.env` に設定済みの場合、そちらが自動で読み込まれます。

### 2. Python依存パッケージ

```bash
pip install google-genai python-dotenv Pillow httpx
```

### 3. Remotion依存パッケージ

```bash
cd 03_Remotion
npm install
```

---

## 🚀 使い方

### Step 1: 画像生成

```bash
# 全パネルの画像を生成
cd 01_画像生成
python generate_manga.py

# 特定のシーンのみ
python generate_manga.py --scene A-1 A-2 A-3

# バッチファイルからも実行可能
generate_manga.bat
```

### Step 2: 音声生成

```bash
# 全セリフの音声を生成
cd 02_音声生成
python generate_voice.py

# 特定のパネルのみ
python generate_voice.py --panel A-3 B-1

# バッチファイルからも実行可能
generate_voice.bat
```

### Step 3: Remotion動画生成

```bash
cd 03_Remotion

# プレビュー
npm run start

# 動画レンダリング
npx remotion render TestOpening10s out/test_video.mp4
npx remotion render MangaVideo out/manga_video.mp4
```

---

## 📦 素材一覧（04_素材）

| フォルダ | 内容 | 数 |
|---------|------|-----|
| 画像/ | 漫画パネル画像（A1〜D2） | 24枚 |
| 音声/ | ElevenLabsナレーション・セリフ | 37本 |
| SE/ | 効果音（銃声・足音等） | 23本 |
| 動画/ | Luma Dream Machine生成動画 | 3本 |
| scene1_data.json | シーン1の全パネル定義 | - |

---

## 📊 使用モデル情報

| ツール | モデル | 用途 |
|--------|--------|------|
| **Nano Banana 2** | gemini-3.1-flash-image-preview | 漫画イラスト生成 |
| **ElevenLabs v3** | eleven_v3 | ナレーション・セリフ音声 |
| **Remotion** | 4.0.242 | 動画レンダリング |

---

**更新日**: 2026年3月18日
