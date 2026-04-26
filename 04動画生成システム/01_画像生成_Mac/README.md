# 🎨 AI画像生成ツール（Mac版）

## これは何？

**Google AI** を使って、YouTube動画やSNS投稿用の **アニメ風イラスト** を自動生成するツールです。

プロンプト（「こんな絵を描いて」という指示文）を入力するだけで、プロ品質のイラストが数秒で生成されます。

Mac環境に最適化されたバージョンです。

---

## ✨ 特徴

- 🖼️ **高品質なアニメ風イラスト** — ジブリ風の温かいタッチからダイナミックな漫画調まで
- 📐 **16:9 横長フォーマット** — YouTube動画にそのまま使える
- 🔄 **自動リトライ** — 失敗しても自動で再試行（最大3回 × 2モデル）
- 🤖 **Gemini AI 搭載** — Google最新の画像生成AI使用
- 🍎 **Mac最適化** — macOS向けのパス・コマンド・シェルスクリプト対応

---

## 🚀 かんたんスタート（3ステップ）

### ステップ① APIキーを設定する

`05_設定` フォルダに `.env` ファイルを作成し、以下を記入：

```
GOOGLE_API_KEY=あなたのGoogleAPIキー
```

> 💡 APIキーの取得方法は [マニュアル](マニュアル_画像生成.md) を参照してください

> 💡 Finderで `.env` ファイルが見えない場合は `Command + Shift + .` で隠しファイルを表示

### ステップ② Python環境を準備する

ターミナルで実行（`Command + Space` → 「Terminal」で開けます）：

```bash
pip3 install google-genai python-dotenv Pillow
```

### ステップ③ 画像を生成する

```bash
cd ~/Documents/Obsidian\ Vault/demo/01_画像生成_Mac
python3 generate_manga.py
```

または、`generate_manga.sh` をターミナルから実行：

```bash
./generate_manga.sh
```

> 💡 初回のみ `chmod +x generate_manga.sh` で実行権限を付与してください

---

## 📁 ファイル構成

```
01_画像生成_Mac/
├── 🔧 google_image_client.py       ← 共通クライアント（中核モジュール）
├── 🎨 generate_manga.py            ← 漫画イラスト一括生成スクリプト
├── 🏛️ generate_pension_scenes.py   ← 年金台本用シーン生成
├── 🔄 regen_split_image.py         ← 個別画像の再生成（プリセット付き）
├── 📄 generate_manga.sh            ← シェルスクリプト実行用
├── 📖 SKILL.md                     ← AI向けスキル定義
├── 📖 README.md                    ← このファイル
└── 📖 マニュアル_画像生成.md        ← 初心者向けマニュアル
```

---

## 🤖 使用AIモデル

| モデル名 | 特徴 | 使われ方 |
|----------|------|----------|
| **Nano Banana 2** | 高速・高コスパ | 最優先で使用 |
| **Nano Banana Pro** | 超高品質 | Nano Banana 2が失敗時に自動切替え |

> ⚠️ このツールは **Google AIのみ** を使用します。他のAIサービスには切り替わりません。

---

## 🎯 使い方の例

### 漫画イラストを一括生成

```bash
python3 generate_manga.py
```

### 特定のシーンだけ生成

```bash
python3 generate_manga.py --scene A-1 A-2 B-1
```

### シーン一覧を確認

```bash
python3 generate_manga.py --list
```

### 出力先を指定

```bash
python3 generate_manga.py --output ~/Desktop/images
```

### 年金シーンを生成

```bash
python3 generate_pension_scenes.py
```

### プリセットで個別再生成

```bash
python3 regen_split_image.py --preset split_comparison --output comparison.png
python3 regen_split_image.py --preset character_closeup --output closeup.png
```

### カスタムプロンプトで1枚生成

```bash
python3 regen_split_image.py --prompt "A beautiful sunset over Mount Fuji..." --output fuji.png
```

---

## ❓ よくある質問

### Q: エラーが出ました
**A:** まず以下を確認してください：
1. `demo/05_設定/.env` に `GOOGLE_API_KEY` が正しく設定されているか
2. `pip3 install google-genai python-dotenv Pillow` を実行済みか
3. インターネットに接続されているか
4. `python3` コマンドが使えるか（`python3 --version` で確認）

### Q: 画像が正方形になってしまいます
**A:** プロンプトに「16:9 widescreen landscape」の指定が含まれているか確認してください。共通クライアント経由で生成すると、自動的に16:9が指定されます。

### Q: APIキーはどこで取得できますか？
**A:** [マニュアル](マニュアル_画像生成.md) の「APIキーの取得方法」セクションを参照してください。

### Q: Permission denied が出ます
**A:** シェルスクリプトに実行権限がない場合は `chmod +x generate_manga.sh` を実行してください。

### Q: `python` コマンドが見つからない
**A:** Macでは `python3` を使用してください。`python` は macOS によっては利用できません。

---

**更新日**: 2026年3月25日  
**対応OS**: macOS 12 Monterey 以降
