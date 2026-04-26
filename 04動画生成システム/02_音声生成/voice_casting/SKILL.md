---
name: 音声キャスティングスキル
description: 台本からキャラクターを抽出し、ElevenLabs Voice Design APIで各キャラの声を設計・選定する
---

# 音声キャスティングスキル

## スキル概要

台本（.md）を入力として、キャラクター自動抽出→声質ヒアリング→候補ボイス生成→試聴→選定までを一貫して行う。
SKILL.md がフローの司令塔として機能し、API呼び出しは `voice_casting.py` に委譲する。

## 前提条件

- `ELEVENLABS_API_KEY` が `.env` に設定されていること
- Python環境に `httpx`, `python-dotenv` がインストール済み
- 台本に `## キャラクター` セクションと `### セリフ` セクションが含まれていること

## 実行手順

### Phase 1: 台本解析 — キャラクター自動抽出

台本ファイルを読み込み、以下を抽出する:

1. **キャラクターセクションの解析**
   - `## キャラクター` または `### 語り手` `### 失敗側` `### 成功側` 等の見出しからキャラクター名・役割・属性を抽出
   - 名前、年齢、職業、性格、口癖、外見を構造化

2. **セリフセクションの解析**
   - `### セリフ` 内の `キャラ名「セリフ内容」（動作指示）` 形式からセリフを抽出
   - 各キャラの代表セリフ（最も感情が出るもの1〜2文）を自動選定

3. **ナレーションの解析**
   - `### ナレーション（話者名）` からナレーター名を抽出

4. **抽出結果をユーザーに提示**

```
【抽出結果】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. 杉山 誠（64歳）— ナレーター
   役割: 場面転換と感情の橋渡し
   代表セリフ: 「皆さん、1つ質問させてください。」
   
2. 原田 和夫（63歳）— メインキャラクター（失敗側）
   役割: 大手食品メーカー経理部37年勤務
   代表セリフ: 「…なんで。誰も教えてくれなかったんだ…」
   
（以下続く）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

このキャラクター構成でよろしいですか？
変更があればお知らせください。
```

**ユーザーの承認を待つ。**

---

### Phase 2: 声質ヒアリング

承認後、各キャラクターに対して順番にヒアリングを行う。

#### ヒアリングの進め方

1. キャラクターの属性データ（年齢・性格・役割）を提示
2. 以下を質問:

```
【杉山 誠（ナレーター）の声質設計】

属性: 64歳男性、場面転換と感情の橋渡し役
代表セリフ: 「皆さん、1つ質問させてください。」

どんな声をイメージしていますか？
例:
- 「落ち着いた低音で、温かみのある語り」
- 「若々しくてテンポのいい声」
- 「渋い声で、信頼感がある」

何パターンの候補を生成しますか？（推奨: 3）
```

3. ユーザーの回答から **英語の Voice Design プロンプト** を生成

#### 日本語→英語プロンプト変換ルール

| 日本語の表現 | 英語プロンプトへの変換 |
|---|---|
| 落ち着いた低音 | Deep low-pitched, calm measured delivery |
| 温かみのある | Warm, gentle resonance |
| 若い女の子 | Youthful female, bright soprano |
| 渋い | Rich, mature, gravelly undertone |
| 元気な | Energetic, lively, upbeat intonation |
| 怖い | Deep authoritative, commanding presence |
| かわいい | Sweet, light, playful |
| テンポがいい | Natural rhythmic pace, good timing |
| 信頼感がある | Trustworthy, professional broadcaster quality |
| アニメっぽい | Expressive anime-style, dynamic range |

**生成するプロンプトの構造:**
```
"{音域}, {声質特徴}, {話し方}, {年齢・性別}, {キャラクター性}, {言語指示}"
```

例:
```
"Deep baritone, warm rich resonance, calm measured delivery, 
mature middle-aged male, trustworthy narrator with subtle warmth, 
natural Japanese accent"
```

**全キャラのヒアリングが完了するまで繰り返す。**

---

### Phase 3: 候補ボイス生成

ヒアリング結果を元に `voice_casting.py` を実行。

#### 実行コマンド

```bash
cd "c:\Obsidian Vault\demo\02_音声生成\voice_casting"

# キャラクターごとに候補生成
python voice_casting.py design ^
  --character "杉山誠" ^
  --prompt "Deep baritone, warm rich resonance..." ^
  --test-text "皆さん、1つ質問させてください。" ^
  --count 3

# 全キャラ一括生成（casting_state.jsonを使用）
python voice_casting.py design --from-state
```

#### 出力

```
output/
├── 杉山誠_preview_1.mp3    ← 候補1のテスト音声
├── 杉山誠_preview_2.mp3    ← 候補2のテスト音声
├── 杉山誠_preview_3.mp3    ← 候補3のテスト音声
└── casting_state.json       ← 状態管理ファイル（更新）
```

---

### Phase 4: 試聴・選択

生成された音声ファイルをユーザーに提示:

```
【杉山 誠（ナレーター）— 候補ボイス】

▶ 候補1: output/杉山誠_preview_1.mp3
▶ 候補2: output/杉山誠_preview_2.mp3
▶ 候補3: output/杉山誠_preview_3.mp3

テストフレーズ: 「皆さん、1つ質問させてください。」

どの候補がお好みですか？
微調整のリクエストがあれば教えてください。
例: 「候補2がいいけど、もう少し低い声がいい」
```

#### フィードバック対応

ユーザーから微調整リクエストがあった場合:
1. フィードバックを反映した新しい英語プロンプトを生成
2. Phase 3 に戻って再生成
3. 再度試聴・選択

**全キャラの選択が完了するまで繰り返す。**

---

### Phase 5: 確定・保存

全キャラの声が選択されたら、ElevenLabsライブラリに永続保存:

```bash
# 選択されたボイスをライブラリに保存
python voice_casting.py save --character "杉山誠" --index 2

# 全キャラ一括保存
python voice_casting.py save --all

# voice_ids.json に自動追記される
```

#### 保存後の出力

`voice_ids.json` が更新される:
```json
{
  "杉山誠": "永続voice_id_here",
  "原田和夫": "永続voice_id_here",
  "原田典子": "永続voice_id_here",
  "長谷川正志": "永続voice_id_here",
  "長谷川美代子": "永続voice_id_here"
}
```

#### 最終確認

```
【キャスティング完了】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. 杉山 誠 → voice_id: xxx... ✅
2. 原田 和夫 → voice_id: xxx... ✅
3. 原田 典子 → voice_id: xxx... ✅
4. 長谷川 正志 → voice_id: xxx... ✅
5. 長谷川 美代子 → voice_id: xxx... ✅

voice_ids.json に保存しました。
本番音声の生成に進んでよろしいですか？
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 参考スクリプト

- [voice_casting.py](file:///c:/Obsidian%20Vault/demo/02_音声生成/voice_casting/voice_casting.py) — Voice Design API呼び出し・ファイル管理
- [elevenlabs_service.py](file:///c:/Obsidian%20Vault/demo/02_音声生成/elevenlabs_service.py) — 本番音声生成（TTS with timestamps）

## 注意事項

- Voice Design API の呼び出しにはクレジット消費が発生する
- プレビューボイスは一定期間後に期限切れになるため、確定後は必ず `save` コマンドで永続化すること
- 日本語テストフレーズを使用する場合、`model_id` は `eleven_ttv_v3` を使用すること
- API呼び出し間隔は1秒以上空けること
