---
description: Block Ledger の 8 カテゴリを更新する。引数で対象 Block 名と --light/--full モードを指定。空欄は <TBD: 理由> または N/A: 理由 を要求。
---

# /handoff-update {block-name} [--light | --full]

Block Ledger（`memory/blocks/works/{block-name}.md` または `memory/blocks/assets/{block-name}.md`）の 8 カテゴリを更新する。

## 引数

- 第 1 引数：Block 名（例: `OWN-VID-01`、`OWN-NOTE-01`、`LINE-FUNNEL`）
- 第 2 引数（任意）：モード切替
  - `--light`（デフォルト）：状態・KPI のみの軽い更新。Master Ledger 全体読込はしない
  - `--full`：シリーズ連続使用ルール照合などを伴う重い更新。Master Ledger §4 を再読する

`$ARGUMENTS` は `{block} [{mode}]` の形式で受け取る。

## 手順

### 1. 対象ファイルを特定

- `memory/blocks/works/{block}.md`（作品単位）または `memory/blocks/assets/{block}.md`（横断資料）の存在確認
- 存在しない場合：`memory/block_ledger_template.md` をコピーして新規作成し、ヘッダー（種別／状態／親 Block）を埋める
- 横断資料か作品単位かを判定：**ハイフン後ろが数字なら works/**（`OWN-VID-01` `OWN-NOTE-01` 等）、**ハイフン後ろが英字なら assets/**（`LINE-FUNNEL` `BROLL-CATALOG` 等）

### 2. モード別の Master Ledger 読込

- `--light` の場合：master_ledger は **読まない**。Block 内の §4 Emotion State と §5 Carry-over Lines に書かれている連続使用ルール参照はそのまま信頼する
- `--full` の場合：`memory/master_ledger.md` §4「不変ルール」「撤回された前提」を必ず読む

### 3. 8 カテゴリの更新を促す

- 1〜8 の各カテゴリについて、現在の値をユーザーに見せ、更新の必要があるか確認
- 空欄を見つけたら、次のいずれかを必ず入れる：
  - **`<TBD: 理由>`**（着手前・これから決める）
  - **`N/A: 理由`**（構造的に該当しない）
- **本ルールのスコープは Block Ledger 内のみ**。AGENTS.md・decision_log.md 等で運用語として使われている「未確定」はそのまま維持してよい
- **Block Ledger 内では理由なしの空欄、`未確定`、`未定` 等の他表現は禁止**
- `--light` モードは §1 Facts と §2 Symbols のスキップを許可（変更がなければ）

### 4. 特に厳格に扱うカテゴリ

- **§3 Pending Threads**：未回収の伏線。ない場合は `N/A: 単発完結のため伏線なし` のように **明示的な完結宣言** が必要
- **§4 Emotion State**：シリーズで連続使用回避ルールがあれば `--full` モードで照合
- **§6 KPI / 実測**：公開前は予測欄のみ、公開後 3 日以降は実測。実測値が予測と大きく乖離した場合、`feedback_*.md` に学びを追記すべきか提案

### 5. 更新の保存

- 全カテゴリが埋まった（または `<TBD: 理由>` / `N/A: 理由` 付きの）状態で保存
- 「最終更新」日付を更新
- 状態フィールドを最新に更新（v1 → v2 確定 / 公開済 等）

### 6. Master Ledger §5 索引の逆方向更新（必須）

- `memory/master_ledger.md` §5「Block Ledger 索引」を開く
- 対象 Block の行を確認：
  - 「リンク」列が `（未作成）` のままなら、`[blocks/works/{name}.md](blocks/works/{name}.md)` または `[blocks/assets/{name}.md](blocks/assets/{name}.md)` に更新
  - 「状態」列を最新に更新
- これを **怠ると索引が陳腐化する**。Block の Definition of Done に含まれる

### 7. 連動 Block への伝播チェック

- §5 Carry-over Lines に「次の Block へ渡すフレーズ」がある場合、対応する Block Ledger に伝達済みか確認
- 未伝達なら、対応 Block も更新するようユーザーに提案

### 8. Master Ledger 昇格の提案

- 本 Block の更新で「3 セッション以上参照されそうな新ルール」が生まれたら、Master Ledger §4 への昇格をユーザーに提案する

## 失敗パターン回避

- **形式主義化を避ける**：空欄をすべて `N/A` で埋めて済ませることは禁止。`N/A` には必ず**理由**を要求する
- **「未確定」「未定」「TBD」（理由なし）の混入禁止**：着手前は `<TBD: 理由>` 一択
- **片方向の更新で終わらせない**：シリーズ連動 Block がある場合、必ず両方向の整合を確認する
- **§6 索引更新を忘れない**：Block を更新したら master_ledger §5 のリンク列もペアで更新

## 完了報告

更新完了後、以下を 1 行ずつ報告：

- 更新した Block：
- モード：`--light` / `--full`
- 8 カテゴリのうち実値で埋めたもの：（番号列挙）
- `<TBD: 理由>` で残したもの：（番号列挙）
- `N/A: 理由` で埋めたもの：（番号列挙＋理由要約）
- master_ledger §5 索引更新：済 / 未更新箇所あり
- 連動 Block で更新が必要なもの：
- Master Ledger 昇格を提案した新ルール：（あれば）
