# 📖 AI画像生成ツール — 初心者マニュアル（Mac版）

> このマニュアルでは、AIを使った画像生成の手順を **ゼロから** 丁寧に説明します。
> Macをお使いの方向けに、すべての操作手順をMac環境に合わせて記載しています。
> パソコンに詳しくない方でも、順番通りに進めれば画像が生成できるようになります。

---

## 📋 目次

1. [このツールでできること](#1-このツールでできること)
2. [必要なもの](#2-必要なもの)
3. [APIキーの取得方法](#3-apiキーの取得方法)
4. [セットアップ手順](#4-セットアップ手順)
5. [画像を生成してみよう](#5-画像を生成してみよう)
6. [生成された画像の確認](#6-生成された画像の確認)
7. [カスタマイズ方法](#7-カスタマイズ方法)
8. [トラブルシューティング](#8-トラブルシューティング)

---

## 1. このツールでできること

このツールを使うと、**文章で指示するだけ** でアニメ風のイラストを自動生成できます。
難しいプログラミングの知識は不要で、簡単な操作だけで高品質なイラストが手に入ります。

### 活用例

| 用途 | 説明 |
|------|------|
| YouTube動画のイラスト | 16:9の横長イラストを自動生成 |
| SNS投稿用の画像 | 各シーンに合わせたイラストを量産 |
| 漫画風コンテンツ | ストーリーに沿った連続イラストを生成 |
| サムネイル素材 | 目を引くアニメ調のサムネイルを作成 |

### 使用するAI

Google の最新画像生成AI「**Nano Banana 2**」を使用します。
これは Google Gemini の画像生成機能で、高品質なイラストを高速に生成できます。

さらに、Nano Banana 2 で生成がうまくいかなかった場合は、自動的に上位モデル「**Nano Banana Pro**」に切り替わります。この切り替えはツールが自動で行うため、ユーザーが操作する必要はありません。

| モデル名 | 特徴 | 使われ方 |
|----------|------|----------|
| **Nano Banana 2** | 高速・高コスパ | 最優先で使用される |
| **Nano Banana Pro** | 超高品質・精密描画 | Nano Banana 2 が失敗した場合に自動切替え |

> ⚠️ このツールは **Google AI のみ** を使用します。DALL-E、Stable Diffusion、Midjourney等の他のAIサービスには一切切り替わりません。

---

## 2. 必要なもの

始める前に以下を用意してください：

| 必要なもの | 説明 | 入手方法 |
|------------|------|----------|
| **Mac（macOS）** | macOS 12 Monterey 以降を推奨 | — |
| **Python** | バージョン 3.10 以上 | [python.org](https://www.python.org/downloads/) または Homebrew |
| **Google API キー** | Google AIを使うための認証キー | 次のセクションで詳しく説明 |
| **インターネット接続** | AIサーバーへのアクセスに必要 | — |
| **テキストエディタ** | `.env` ファイルの編集に使用 | テキストエディット（Mac標準）でOK |

> 💡 **ヒント**: Pythonは最近のmacOSにはプリインストールされていないことがあります。次のセクションでインストール方法を詳しく説明します。

---

## 3. APIキーの取得方法

APIキーとは、Google AIを使うための「通行証」のようなものです。
以下の手順で無料で取得できます。

### ステップ 3-1: Google AI Studio にアクセス

1. ブラウザ（Safari や Chrome など）で以下のURLを開きます：
   **https://aistudio.google.com/**

2. お持ちのGoogleアカウント（Gmail等）でログインしてください

> 💡 **ヒント**: Googleアカウントをお持ちでない場合は、[Googleアカウント作成ページ](https://accounts.google.com/signup) から無料で作成できます。

### ステップ 3-2: APIキーを作成

1. 画面左メニューの「**Get API Key**」をクリック
2. 「**Create API Key**」ボタンをクリック
3. プロジェクトを選択する画面が出たら、そのまま「**Create API Key in new project**」をクリック（既存プロジェクトがある場合はそれを選んでもOK）
4. 表示されたAPIキーを **コピー** してください

> ⚠️ **重要**: APIキーは他人に見せないでください。このキーがあれば誰でもあなたのアカウントでAIを使えてしまいます。SNSやブログ、GitHubなどに公開しないよう十分ご注意ください。

### ステップ 3-3: APIキーを保存

1. **Finder** を開き、`demo` フォルダ内の `05_設定` フォルダに移動します
2. `.env.example` というファイルがあれば、それを `.env` にリネーム（名前変更）します

**リネームの方法：**
   - ファイルを選択した状態で `Return`（Enter）キーを押す
   - ファイル名を `.env` に変更する
   - 「.（ドット）で始まる名前にしますか？」と確認が出たら「OK」を押す

3. `.env.example` がない場合は、新しくファイルを作成します：

**新規作成の方法：**
   - `05_設定` フォルダ内で右クリック → 何もないところでは作成できないため、**ターミナル** を使います
   - ターミナルを開き（後述の方法を参照）、以下を入力してEnterキーを押します：
   ```bash
   touch ~/Documents/Obsidian\ Vault/demo/05_設定/.env
   ```

4. `.env` ファイルをテキストエディタで開き、以下のように記入します：

```
GOOGLE_API_KEY=ここにコピーしたAPIキーを貼り付け
```

例：
```
GOOGLE_API_KEY=AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

> ⚠️ **注意**: `=` の前後にスペースを入れないでください。また、APIキーの前後にも余分なスペースや引用符（`"` や `'`）を入れないでください。

5. ファイルを保存して閉じます

> 💡 **ヒント**: Macでは `.`（ドット）で始まるファイルはFinderで非表示になります。表示するには、Finderで `Command + Shift + .`（ピリオド）を押してください。もう一度押すと非表示に戻ります。

---

## 4. セットアップ手順

### ステップ 4-1: ターミナルを開く

Macでは、Windowsの「コマンドプロンプト」に相当するアプリが **ターミナル** です。
以下のいずれかの方法で開いてください：

**方法A: Spotlight検索で開く（おすすめ）**
1. `Command + Space` を押してSpotlight検索を開きます
2. 「ターミナル」または「Terminal」と入力します
3. 表示された「ターミナル.app」をクリックします

**方法B: LaunchpadまたはFinderから開く**
1. Finderを開きます
2. メニューバーの「移動」→「ユーティリティ」をクリックします
3. 「ターミナル.app」をダブルクリックします

> 💡 **ヒント**: ターミナルは黒い背景に白い文字が表示されるウィンドウです。ここにコマンド（命令文）を入力して操作します。最初は少し抵抗があるかもしれませんが、コピー＆ペーストで進められるのでご安心ください。

### ステップ 4-2: Pythonがインストールされているか確認

1. ターミナルに以下を入力して `Return`（Enter）キーを押します：

```bash
python3 --version
```

2. 「Python 3.10.x」のような表示が出ればOKです

> ⚠️ **注意**: Macでは `python` ではなく **`python3`** と入力してください。`python` コマンドはmacOSのバージョンによっては動作しない場合があります。

#### Pythonがインストールされていない場合

「command not found」や「No such file」と表示された場合は、Pythonをインストールする必要があります。以下のいずれかの方法でインストールしてください：

**方法A: Python公式サイトからインストール（初心者向け）**

1. ブラウザで [Python公式サイト](https://www.python.org/downloads/) を開きます
2. 「Download Python 3.xx.x」ボタンをクリック
3. ダウンロードした `.pkg` ファイルをダブルクリック
4. インストーラーの指示に従って進みます（基本的に「続ける」→「インストール」でOK）
5. インストール完了後、ターミナルを **閉じて再度開き**、`python3 --version` で確認

**方法B: Homebrewを使ってインストール（慣れた方向け）**

Homebrewがインストール済みの場合は、ターミナルで以下を実行するだけです：

```bash
brew install python@3.12
```

> 💡 **Homebrewとは**: Mac用のパッケージマネージャー（ソフト管理ツール）です。まだ入っていない場合は方法Aをおすすめします。

### ステップ 4-3: 必要なパッケージをインストール

ターミナルで以下を入力して `Return` キーを押します：

```bash
pip3 install google-genai python-dotenv Pillow
```

いくつかのメッセージが画面に流れますが、最終的に「Successfully installed」と出れば成功です。

> ⚠️ **注意**: Macでは `pip` ではなく **`pip3`** を使用してください。`pip` コマンドは古いPython 2系のものを指す場合があります。

#### 「WARNING: pip is configured with locations that require TLS/SSL」が出た場合

Python公式サイトからインストールした場合、SSL証明書のインストールが必要なことがあります。以下を実行してください：

```bash
open /Applications/Python\ 3.12/Install\ Certificates.command
```

（バージョン番号は実際にインストールしたものに置き換えてください）

---

## 5. 画像を生成してみよう

### 方法A: シェルスクリプトで実行（かんたん）

1. Finderで `01_画像生成` フォルダを開きます
2. `generate_manga.sh` を見つけます
3. 初回のみ、ターミナルで実行権限を付与する必要があります：

```bash
chmod +x ~/Documents/Obsidian\ Vault/demo/01_画像生成/generate_manga.sh
```

4. 方法は2通りあります：

**ターミナルから実行する場合：**
```bash
~/Documents/Obsidian\ Vault/demo/01_画像生成/generate_manga.sh
```

**Finderからダブルクリックで実行する場合：**
- `generate_manga.sh` を右クリック →「このアプリケーションで開く」→「ターミナル.app」を選択
- 初回以降は、ダブルクリックでターミナルから自動実行されます

> 💡 **ヒント**: シェルスクリプト（`.sh`ファイル）はWindowsの `.bat` ファイルに相当するもので、コマンドをまとめて実行するためのファイルです。

### 方法B: コマンドラインで実行

1. ターミナルを開きます
2. 以下を入力します：

```bash
cd ~/Documents/Obsidian\ Vault/demo/01_画像生成
python3 generate_manga.py
```

> 💡 **パスの入力のコツ**: 
> - `~` はホームフォルダ（`/Users/あなたのユーザー名`）を意味します
> - フォルダ名にスペースがある場合は、スペースの前に `\`（バックスラッシュ）を付けます
> - Finder からフォルダをターミナルにドラッグ＆ドロップすると、パスが自動入力されます（おすすめ！）

### 画面に表示されるメッセージの見方

```
[OK] .env読み込み: /Users/あなたの名前/Documents/Obsidian Vault/demo/05_設定/.env     ← 設定ファイル読み込み成功
[OK] Google API Key: AIzaSyXXXX...                          ← APIキー認識成功
[OK] モデル優先順位: Nano Banana 2 → Nano Banana Pro         ← 使用するAIモデル

============================================================
  [1/4] ナレーター導入（質問）                               ← 生成中のシーン
============================================================
  モデル: Nano Banana 2 (gemini-3.1-flash-image-preview)     ← 使用モデル
    [OK] 保存完了: scene1_narrator_intro.png                  ← 生成成功！
    [OK] サイズ: 1376x768 (比率: 1.79)                       ← 画像サイズ（16:9）
```

- `[OK]` → 成功
- `[NG]` → 失敗（自動でリトライします。最大3回まで各モデルで再試行）

> 💡 **生成にかかる時間**: 1枚あたり約10〜30秒程度です。全シーンの生成が完了するまでターミナルを閉じないでください。

---

## 6. 生成された画像の確認

生成された画像は以下のフォルダに保存されます：

```
demo/03_Remotion/public/images/
```

または、`--output` オプションで指定したフォルダに保存されます。

### Finderでの確認方法

1. Finderを開きます
2. `demo` → `03_Remotion` → `public` → `images` の順にフォルダを開きます
3. 生成された画像ファイル（`.png`）が一覧で表示されます
4. ファイルを選択して `Space` キーを押すと、クイックルック（プレビュー）で確認できます

### ターミナルからの確認方法

ターミナルで以下を実行すると、Finderで画像フォルダが開きます：

```bash
open ~/Documents/Obsidian\ Vault/demo/03_Remotion/public/images/
```

特定の画像をプレビューアプリで開くには：

```bash
open ~/Documents/Obsidian\ Vault/demo/03_Remotion/public/images/scene1_narrator_intro.png
```

ファイルはすべて **PNG形式** で保存されます。Macのプレビュー.appで開いて確認・編集が可能です。

---

## 7. カスタマイズ方法

### 独自のプロンプトで画像を生成する

Pythonの基本がわかる方は、以下のようにスクリプトを書いて独自の画像を生成できます：

```python
from google_image_client import GoogleImageClient
from pathlib import Path

# クライアントを準備
client = GoogleImageClient()

# プロンプト（どんな画像を生成するかの指示）
prompt = """
IMPORTANT: Generate this image in LANDSCAPE 16:9 widescreen aspect ratio.
Art style: Soft, warm Japanese anime illustration.
No text, no speech bubbles.

Scene: A beautiful sunset over a Japanese countryside.
A young woman in a summer dress standing in a rice field,
looking at the orange sky. Warm, nostalgic atmosphere.
"""

# 画像を生成して保存
client.generate_image(prompt, Path("my_image.png"))
```

このスクリプトを `my_script.py` として保存し、ターミナルで以下を実行します：

```bash
cd ~/Documents/Obsidian\ Vault/demo/01_画像生成
python3 my_script.py
```

### コマンドラインオプション

`generate_manga.py` は以下のオプションに対応しています：

```bash
# 特定のシーンだけを生成する
python3 generate_manga.py --scene A-1 A-2 B-1

# 出力先を指定する
python3 generate_manga.py --output ~/Desktop/images

# ヘルプを表示する
python3 generate_manga.py --help
```

### プロンプトのコツ

| コツ | 例 | 解説 |
|------|-----|------|
| **年齢を具体的に** | 「68歳の男性」「白髪」「シワ」 | 具体的な特徴を書くほど意図した画像に近づきます |
| **感情を明示** | 「温かい」「暗い」「後悔」「幸せ」 | シーンの雰囲気がガラリと変わります |
| **構図を指定** | 「左1/3にキャラクター」「スプリットスクリーン」 | 構図を指定すると安定した画面になります |
| **NG要素を明示** | 「No text, no speech bubbles」は必須 | AIが余計な文字を入れるのを防ぎます |
| **16:9を指定** | 「LANDSCAPE 16:9 widescreen」を冒頭に | 冒頭で強調することで16:9比率になりやすくなります |
| **画風を指定** | 「Studio Ghibli style」「soft anime」 | ジブリ風にしたい場合は明示すると効果的です |

> 💡 **上級者向けヒント**: プロンプトは英語で書くと、AIの理解精度が上がりやすい傾向があります。日本語のシーン説明を英語に翻訳してから入力すると、より意図通りの画像が生成されることがあります。

---

## 8. トラブルシューティング

### 🔴 「GOOGLE_API_KEYが設定されていません」

**原因:** `.env` ファイルが見つからないか、中身が正しくありません。

**対処法:**
1. `demo/05_設定/` フォルダに `.env` ファイルがあるか確認
   - Finderで `Command + Shift + .` を押して隠しファイルを表示
2. ファイルの中身が `GOOGLE_API_KEY=あなたのキー` の形式か確認
3. キーの前後に余分なスペースや引用符がないか確認
4. ターミナルで以下を実行して中身を確認することもできます：
   ```bash
   cat ~/Documents/Obsidian\ Vault/demo/05_設定/.env
   ```

---

### 🔴 「ModuleNotFoundError: No module named 'google'」

**原因:** 必要なパッケージがインストールされていません。

**対処法:**
```bash
pip3 install google-genai python-dotenv Pillow
```

もし `pip3` が見つからないと表示された場合は、以下を試してください：

```bash
python3 -m pip install google-genai python-dotenv Pillow
```

---

### 🔴 「Permission denied」エラー

**原因:** Mac特有の問題で、ファイルやフォルダへのアクセス権限がありません。

**対処法:**

シェルスクリプトの実行権限がない場合：
```bash
chmod +x ~/Documents/Obsidian\ Vault/demo/01_画像生成/generate_manga.sh
```

ファイルの書き込み権限がない場合：
```bash
chmod 755 ~/Documents/Obsidian\ Vault/demo/03_Remotion/public/images/
```

> 💡 **解説**: `chmod` はファイルの権限を変更するコマンドです。`+x` は「実行可能にする」、`755` は「所有者に全権限、それ以外に読み取り・実行権限を付与する」という意味です。

---

### 🔴 「画像データなし」と表示される

**原因:** AIが画像を生成できなかった（プロンプトの内容による場合が多い）。

**対処法:**
- 自動でリトライされます（各モデルにつき最大3回）
- Nano Banana 2 で失敗した場合は自動的に Nano Banana Pro に切り替わります
- それでもダメなら、プロンプトの内容を変えてみてください
- 暴力的・性的な内容はAIが拒否する場合があります
- プロンプトが長すぎる場合も失敗しやすくなります（目安：500文字以内）

---

### 🔴 画像が正方形になる

**原因:** プロンプトに16:9の指定がありません。

**対処法:** プロンプトの **冒頭** に以下を追加してください：
```
IMPORTANT: Generate this image in LANDSCAPE 16:9 widescreen aspect ratio.
NOT square. The width must be significantly larger than the height.
```

> 💡 **ヒント**: 共通クライアント（`GoogleImageClient`）を使って生成すると、16:9の指定が自動的に含まれるため、この問題は起きにくくなります。

---

### 🔴 「API quota exceeded」エラー

**原因:** APIの利用上限に達しました。

**対処法:**
- しばらく時間を置いてから再試行してください（通常1分程度で回復）
- 大量の画像を生成する場合は間隔を空けてください
- 1日の無料枠を超えた場合は、翌日まで待つ必要があることがあります

---

### 🔴 「SSL: CERTIFICATE_VERIFY_FAILED」エラー

**原因:** Mac特有の問題で、Python用のSSL証明書がインストールされていません。

**対処法:**

Python公式サイトからインストールした場合：
```bash
open /Applications/Python\ 3.12/Install\ Certificates.command
```
（バージョン番号は実際にインストールしたものに置き換えてください）

Homebrewでインストールした場合は、通常この問題は発生しません。

---

### 🔴 「zsh: command not found: python3」

**原因:** Python3がインストールされていない、またはパスが通っていません。

**対処法:**
1. まず、Pythonが本当にインストールされているか確認します：
   ```bash
   which python3
   ls /usr/local/bin/python3
   ls /opt/homebrew/bin/python3
   ```
2. いずれも見つからない場合は、[ステップ 4-2](#ステップ-4-2-pythonがインストールされているか確認) に戻ってPythonをインストールしてください

---

### 🟡 生成は成功するが品質が低い

**対処法:**
- プロンプトをより具体的にしてください
- 「High quality」「professional」「detailed」などの品質指定を追加
- キャラクターの特徴をより詳細に記述（年齢、髪型、服装、表情など）
- 背景の描写も具体的に（「教室」ではなく「午後の日差しが差し込む、木製の机が並ぶ教室」）
- アートスタイルを明示する（「Studio Ghibli inspired」「soft anime watercolor style」など）

---

## 📌 注意事項

1. **APIキーの管理** — APIキーは他人に共有しないでください。GitHubなど公開リポジトリに含めないよう特にご注意ください
2. **利用料金** — Google AIには無料枠がありますが、大量利用時は料金が発生する場合があります。利用状況は [Google AI Studio](https://aistudio.google.com/) のダッシュボードで確認できます
3. **生成内容** — AIが生成する画像には、意図しない要素が含まれることがあります。公開前に必ず目視で確認してください
4. **Google API専用** — このツールはGoogle AIのみを使用します。他のAIサービスには自動的に切り替わりません
5. **Macのセキュリティ設定** — macOS Ventura以降では、ダウンロードしたスクリプトの実行時にセキュリティ警告が出ることがあります。「システム設定」→「プライバシーとセキュリティ」から許可してください

---

## 🔧 Mac特有の便利テクニック

### ターミナルを素早く開くコツ

1. **Spotlight検索**: `Command + Space` → 「Terminal」と入力 → `Return`
2. **Dockに追加**: ターミナルをDockにドラッグして追加しておくと、ワンクリックで開けます

### パスの入力を楽にする

- **ドラッグ＆ドロップ**: Finderからフォルダやファイルをターミナルにドラッグすると、パスが自動入力されます
- **Tab補完**: ファイル名の最初の数文字を入力して `Tab` キーを押すと、自動補完されます
- **履歴の利用**: `↑`（上矢印）キーで過去に入力したコマンドを呼び出せます

### 隠しファイルの表示

`.env` のようなドットファイルをFinderで見るには：
- `Command + Shift + .`（ピリオド）を押すと表示/非表示が切り替わります

---

> 📞 **困ったときは** — このマニュアルで解決しない場合は、配布元にお問い合わせください。

**更新日**: 2026年3月25日  
**対応OS**: macOS 12 Monterey 以降
