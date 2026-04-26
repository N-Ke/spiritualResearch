---
name: ElevenLabs音声生成スキル（Mac版）
description: ElevenLabs APIでナレーション・セリフ音声を生成し、文字単位タイムスタンプでテロップ同期データも取得する。Mac環境専用。
---

# ElevenLabs音声生成スキル（Mac版）

## スキル概要

ElevenLabs API（`eleven_v3`モデル）を使い、キャラクター別の音声を生成する。`with-timestamps` エンドポイントにより文字単位のタイムスタンプを取得し、テロップとの100%同期を実現する。

> [!CAUTION]
> **Mac版制約**: このスキルはMac環境向けに書かれている。
> Windows版は `02_音声生成/` を使用すること。両者は独立して動作する。

## 前提条件

- `ELEVENLABS_API_KEY` が以下のいずれかの `.env` に設定されていること:
  - `~/Documents/Obsidian Vault/demo/05_設定/.env`
  - `~/Documents/Obsidian Vault/X_Post_System/2_Config/.env`
  - カレントディレクトリの `.env`
- Python3 環境に以下がインストール済み:
  - `httpx`
  - `python-dotenv`

> [!IMPORTANT]
> Mac では `python3` / `pip3` コマンドを使用すること。
> `python` / `pip` は Python 2系を指す場合がある。

## 重要な仕様

### APIエンドポイント

```
POST https://api.elevenlabs.io/v1/text-to-speech/{voice_id}/with-timestamps
```

> [!IMPORTANT]
> 通常の `/text-to-speech/{voice_id}` ではなく、**`/with-timestamps`** を使用する。
> これにより文字単位のタイムスタンプが取得でき、テロップ同期が可能になる。

### モデル

| モデルID | 説明 |
|----------|------|
| `eleven_v3` | 最新モデル（推奨）。Audio Tags対応 |

### 共通クライアントの使い方

```python
from elevenlabs_client import ElevenLabsClient
from pathlib import Path

# クライアント初期化（APIキーは.envから自動読み込み）
client = ElevenLabsClient()

# 音声生成（プリセット使用）
result = client.generate_speech(
    text="こんにちは、皆さん。",
    voice_id="XkfxZatpPaUTadDUJKRH",
    output_path=Path("output/narration.mp3"),
    preset="narration",  # "narration" / "emotional" / "bright"
)

# カスタム設定で生成
result = client.generate_speech(
    text="[sad] もう…戻れないのか",
    voice_id="sxvhOzOyPqz0aOkYC9bl",
    output_path=Path("output/line01.mp3"),
    custom_settings={
        "stability": 0.45,
        "similarity_boost": 0.80,
        "style": 0.30,
        "use_speaker_boost": True,
    },
)

# テロップ分割
segments = client.get_telop_segments(result["alignment"], fps=30)
```

### voice_settings プリセット

| プリセット | stability | similarity | style | 用途 |
|-----------|-----------|------------|-------|------|
| narration | 0.55 | 0.80 | 0.25 | 安定した語り |
| emotional | 0.45 | 0.80 | 0.30 | 感情的なセリフ |
| bright | 0.60 | 0.80 | 0.15 | 安定した明るさ |

### Audio Tags（v3限定の感情制御）

v3 モデルではテキスト内に `[タグ]` を埋め込み、声の感情・演技指示ができる:

```
[sad] もう…戻れないのか
[laughs] なんだそりゃ
[quietly] [pauses] ──ナレーション、ここは黙っておきましょう。
[nervous] [stammers] 俺は…その…
```

詳細は `02_音声生成/音声設計_ElevenLabs.md` を参照。

## 実行手順

### Step 1: voice_data.json の準備

台本からセリフを分割し、JSON化する:

```json
{
  "lines": [
    {
      "id": "S1-NAR-01",
      "filename": "s1_nar_01_hook.mp3",
      "character": "ナレーター",
      "voice_id": "XkfxZatpPaUTadDUJKRH",
      "preset": "narration",
      "title": "冒頭フック",
      "text": "これ、面白い話があるんだけど。"
    }
  ]
}
```

### Step 2: 音声生成の実行

```bash
cd ~/Documents/Obsidian\ Vault/demo/02_音声生成_Mac
python3 generate_voice.py
```

オプション:
```bash
python3 generate_voice.py --list                       # 一覧表示
python3 generate_voice.py --scene S1-NAR-01 S1-NAR-02  # 特定セリフのみ
python3 generate_voice.py --output ~/Desktop/audio     # 出力先を指定
python3 generate_voice.py --timestamps                 # タイムスタンプJSON出力
python3 generate_voice.py --data custom_data.json      # カスタムデータファイル
```

### Step 3: タイムスタンプでテロップ同期

`--timestamps` オプションで `timestamps.json` が出力される。
句読点の位置とタイムスタンプからフレーム単位のテロップ切替が可能。

## 出力先

- デフォルト: `~/Documents/Obsidian Vault/demo/02_音声生成_Mac/output/`
- 音声形式: MP3

## ファイル構成

| ファイル | 説明 |
|----------|------|
| `elevenlabs_client.py` | **共通クライアント** — API呼出・リトライ・テロップ分割を集約 |
| `generate_voice.py` | 音声一括生成（voice_data.json対応） |
| `voice_data.json` | セリフ定義データ（ユーザー作成） |

## 注意事項

- `.env` に `ELEVENLABS_API_KEY` が必要（GOOGLE_API_KEY とは別）
- API呼び出し間隔は1.5秒以上空ける（自動制御済み）
- 音声ファイルとタイムスタンプは**同じAPIコール**から取得（別々に呼ぶとズレる）
- Audio Tags の詳細設計は `02_音声生成/音声設計_ElevenLabs.md` を参照
