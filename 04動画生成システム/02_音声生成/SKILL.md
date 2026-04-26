---
name: ElevenLabs音声生成スキル
description: ElevenLabs APIでナレーション・セリフ音声を生成し、文字単位タイムスタンプでテロップ同期データも取得する
---

# ElevenLabs音声生成スキル

## スキル概要

ElevenLabs API（`eleven_v3`モデル）を使い、キャラクター別の音声を生成する。`with-timestamps` エンドポイントにより文字単位のタイムスタンプを取得し、テロップとの100%同期を実現する。

## 前提条件

- `ELEVENLABS_API_KEY` が以下の `.env` に設定されていること:
  - `c:\Obsidian Vault\🔧_ツール\新AI動画編集_漫画動画生成ツール\.env`
- Python環境に以下がインストール済み:
  - `httpx`
  - `python-dotenv`

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
| `eleven_v3` | 最新モデル（推奨） |

### 登録済みボイスID

| キャラクター | voice_id | 説明 |
|-------------|----------|------|
| ナレーター杉山 | `XkfxZatpPaUTadDUJKRH` | narrator_b3、落ち着いた語り |
| 原田和夫（暫定） | `sxvhOzOyPqz0aOkYC9bl` | jin_b3、後悔の感情 |

### voice_settings パラメータ

```python
settings = {
    "stability": 0.55,         # 安定性（0.4-0.6が自然）
    "similarity_boost": 0.80,  # 類似性ブースト
    "style": 0.25,             # スタイル強度（感情的なセリフは0.3に上げる）
    "use_speaker_boost": True  # スピーカーブースト
}
```

| シーン種別 | stability | style | 説明 |
|-----------|-----------|-------|------|
| ナレーション | 0.55 | 0.25 | 安定した語り |
| 感情的セリフ | 0.45 | 0.30 | 声の揺れを許容 |
| 明るいセリフ | 0.60 | 0.15 | 安定した明るさ |

## 実行手順

### Step 1: 音声生成 + タイムスタンプ取得

```python
import httpx, base64, json

url = f"{BASE_URL}/text-to-speech/{voice_id}/with-timestamps"
headers = {
    "xi-api-key": ELEVENLABS_API_KEY,
    "Content-Type": "application/json",
}
payload = {
    "text": text,
    "model_id": "eleven_v3",
    "voice_settings": settings
}

with httpx.Client(timeout=60.0) as client:
    response = client.post(url, headers=headers, json=payload)

data = response.json()

# 音声データ取得
audio_data = base64.b64decode(data["audio_base64"])
with open("output.mp3", "wb") as f:
    f.write(audio_data)

# タイムスタンプ取得
alignment = data["alignment"]
characters = alignment["characters"]
start_times = alignment["character_start_times_seconds"]
end_times = alignment["character_end_times_seconds"]
```

### Step 2: テロップ分割点の計算

句読点（。？）の位置とそのタイムスタンプを使って、テロップの切り替えフレームを計算:

```python
FPS = 30
for i, char in enumerate(characters):
    if char in ["。", "？"]:
        split_frame = round(end_times[i] * FPS)
        # この位置でテロップを切り替え
```

### Step 3: レイアウトJSONの更新

```python
panel["telopSegments"] = [
    {
        "text": "前半テキスト",
        "startFrame": 0,
        "durationFrames": split_frame + 3  # 少し余裕
    },
    {
        "text": "後半テキスト", 
        "startFrame": split_frame,
        "durationFrames": panel_duration - split_frame
    }
]
```

## 出力先

- 音声: `c:\Obsidian Vault\demo\03_Remotion\public\audio\`
- 形式: MP3

## 参考スクリプト

- [generate_pension_voice.py](file:///c:/Obsidian%20Vault/demo/02_音声生成/generate_pension_voice.py) — 基本の音声生成
- [sync_telop_timestamps.py](file:///c:/Obsidian%20Vault/demo/02_音声生成/sync_telop_timestamps.py) — タイムスタンプ取得＋テロップ同期

## 注意事項

- `.env`ファイルが複数パスにある場合、`load_dotenv(override=False)` で全部読み込む（breakしない）
- API呼び出し間隔は1秒以上空ける
- 音声ファイルとタイムスタンプは**同じAPIコール**から取得すること（別々に呼ぶとズレる）
