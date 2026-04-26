---
name: Google API専用 画像生成スキル（Mac版）
description: Google APIのみを使用してアニメ系イラストを生成する。Nano Banana 2を優先し、Google API以外へのフォールバックは行わない。Mac環境専用。
---

# Google API専用 画像生成スキル（Mac版）

## スキル概要

Google AI の **Nano Banana 2** / **Nano Banana Pro** APIを使い、YouTube動画用の16:9アニメ系イラストを生成する。harumiスタイル（ジブリ風温かいアニメ調）を基本テイストとする。

> [!CAUTION]
> **Google API専用制約**: このスキルはGoogle APIのみを使用する。
> DALL-E、Stable Diffusion、Midjourney等の他サービスへのフォールバックは**一切行わない**。
> Google APIが失敗した場合はエラーを返すのみとする。

## 前提条件

- `GOOGLE_API_KEY` が以下のいずれかの `.env` に設定されていること:
  - `~/Documents/Obsidian Vault/demo/05_設定/.env`
  - `~/Documents/Obsidian Vault/X_Post_System/2_Config/.env`
  - カレントディレクトリの `.env`
- Python3 環境に以下がインストール済み:
  - `google-genai`（新SDK。旧 `google-generativeai` は使用しない）
  - `Pillow`
  - `python-dotenv`

> [!IMPORTANT]
> Mac では `python3` / `pip3` コマンドを使用すること。
> `python` / `pip` は Python 2系を指す場合がある。

## 重要な仕様

### モデル優先順位

| 優先度 | モデル名 | API ID | 用途 |
|--------|----------|--------|------|
| **1（優先）** | Nano Banana 2 | `gemini-3.1-flash-image-preview` | 高速・高効率、Pro品質をFlashの速度で生成 |
| **2（フォールバック）** | Nano Banana Pro | `gemini-3-pro-image-preview` | 高品質、複雑な編集・精密描画向け |

> [!IMPORTANT]
> **Nano Banana 2 を優先使用**する。コスト対品質のバランスが最も良い。
> Nano Banana 2 で失敗した場合のみ Nano Banana Pro にフォールバックする。

> [!CAUTION]
> - `ImageGenerationModel` は使わないこと。`generate_content` を使う。
> - `imagen-3.0-generate-001` や `imagen-4` は使用しない。
> - 旧SDK `google-generativeai` (google.generativeai) は使用しない。新SDK `google-genai` (google.genai) を使う。

### 共通クライアントの使い方

```python
from google_image_client import GoogleImageClient
from pathlib import Path

# クライアント初期化（APIキーは.envから自動読み込み）
client = GoogleImageClient()

# 画像生成（Nano Banana 2 → Nano Banana Pro の順で自動試行）
success = client.generate_image(
    prompt="画像のプロンプト",
    output_path=Path("output/image.png"),
    retry=3,           # 各モデルでのリトライ回数
    retry_delay=10.0,  # リトライ間の待機秒数
)

# 特定モデルを指定する場合
success = client.generate_image(
    prompt="画像のプロンプト",
    output_path=Path("output/image.png"),
    preferred_model="gemini-3-pro-image-preview",  # Nano Banana Pro を優先
)

# アスペクト比の検証
client.verify_aspect_ratio(Path("output/image.png"))
```

### API呼び出し方式（直接使用する場合）

```python
from google import genai
from google.genai import types

client = genai.Client(api_key=API_KEY)

response = client.models.generate_content(
    model="gemini-3.1-flash-image-preview",  # Nano Banana 2
    contents=[prompt],
    config=types.GenerateContentConfig(
        response_modalities=["IMAGE", "TEXT"]
    )
)
```

### 16:9アスペクト比の指定方法

このモデルには `aspect_ratio` パラメータがないため、**プロンプト内で強く指定**する:

```
IMPORTANT: Generate this image in LANDSCAPE 16:9 widescreen aspect ratio
(e.g. 1792x1024 or similar wide format). NOT square.
The width must be significantly larger than the height.
```

### 画像データの取得

```python
for part in response.parts:
    if part.inline_data is not None:
        image_data = part.inline_data.data
        mime_type = part.inline_data.mime_type
        # JPEG→PNG変換が必要な場合
        if mime_type == 'image/jpeg':
            img = Image.open(io.BytesIO(image_data))
            buf = io.BytesIO()
            img.save(buf, format='PNG')
            image_data = buf.getvalue()
```

## 実行手順

### Step 1: シーン定義の作成

台本からシーンを分割し、各シーンに対してプロンプトを定義する:

```python
HARUMI_STYLE = """
IMPORTANT: Generate this image in LANDSCAPE 16:9 widescreen aspect ratio.
Art style: Soft, warm Japanese anime illustration style inspired by Studio Ghibli.
Clean linework, soft coloring, pastel palette, warm golden lighting.
No text, no speech bubbles, no writing in the image.
"""

SCENES = [
    {
        "filename": "scene1_xxx.png",
        "title": "シーンの説明",
        "prompt": f"{HARUMI_STYLE}\n\nScene: ..."
    },
]
```

### Step 2: 画像生成の実行

```bash
cd ~/Documents/Obsidian\ Vault/demo/01_画像生成_Mac
python3 generate_manga.py
```

または:

```python
from google_image_client import GoogleImageClient

client = GoogleImageClient()
for scene in SCENES:
    client.generate_image(scene["prompt"], Path(scene["filename"]))
```

- Nano Banana 2 → Nano Banana Pro の順で自動試行
- リトライは最大3回（各モデル）
- Google API以外へのフォールバックなし

### Step 3: サイズ検証

生成された画像が16:9（比率≈1.78）になっているか確認:
```python
client.verify_aspect_ratio(Path("output/image.png"))
# 期待値: 1376x768 (比率: 1.79) 前後
```

## 出力先

- `~/Documents/Obsidian Vault/demo/03_Remotion/public/images/` — Remotion用
- 画像形式: PNG

## ファイル構成

| ファイル | 説明 |
|----------|------|
| `google_image_client.py` | **共通クライアント** — モデル選択・リトライ・変換処理を集約 |
| `generate_manga.py` | 漫画イラスト生成（scene_data.json対応） |
| `generate_pension_scenes.py` | 年金台本用4枚生成（harumiスタイル） |
| `regen_split_image.py` | 個別画像再生成（対比カット・プリセット付き） |
| `generate_manga.sh` | Mac用シェルスクリプト（ダブルクリック実行可） |

## プロンプトのコツ

1. **キャラクターの年齢を具体的に書く** — 「68歳」「白髪」「シワ」など詳細に
2. **感情・雰囲気を明示** — 「温かい」「暗い」「後悔」「幸せ」
3. **構図を指定** — 「左1/3にキャラクター」「スプリットスクリーン」等
4. **NG要素を明示** — 「No text, no speech bubbles」は必須
5. **英語で書く** — AIの理解精度が上がりやすい
