# スピリチュアル系（チャンネル設計）

YouTube スピ系の **ジャンルリサーチ・チャンネル調査** 用フォルダ。

バージョン管理: [github.com/N-Ke/spiritualResearch](https://github.com/N-Ke/spiritualResearch)（このフォルダをリポジトリルートとして `main` を追跡）

### フォークの変更をいつも取り込む

- **本家** … `origin`（`N-Ke/spiritualResearch`）
- **フォーク** … `fork`（例: `megumaguz04100410-cyber/spiritualResearch`）。未登録なら  
  `git remote add fork https://github.com/<ユーザー名>/spiritualResearch.git`

作業フォルダ（このリポジトリのルート）で:

```powershell
.\sync_from_fork.ps1
```

本家 GitHub も同じ内容にしたいとき（push 権限があるときだけ）:

```powershell
.\sync_from_fork.ps1 -PushOrigin
```

手動で同じことだけする場合: `git fetch origin` → `git fetch fork` → `git checkout main` → `git merge fork/main`

| 読者 | 最初に開くファイル |
|---|---|
| 人間 | [[00_はじめに]] |
| AI / エージェント | [[AGENTS]] |
| ジャンル階層の索引 | [[20_ジャンル/README]] |
