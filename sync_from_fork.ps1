# フォーク (remote: fork) の main を、手元の main に取り込む
# 使い方:
#   .\sync_from_fork.ps1
#   .\sync_from_fork.ps1 -PushOrigin   # 取り込み後に本家 origin へ push もする（権限があるときだけ）
param(
    [switch] $PushOrigin
)

$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

$fork = git remote | Select-String -Pattern "^fork$" -Quiet
if (-not $fork) {
    Write-Error "remote 'fork' がありません。例: git remote add fork https://github.com/<ユーザー>/spiritualResearch.git"
    exit 1
}

Write-Host ">> git fetch origin"
git fetch origin
Write-Host ">> git fetch fork"
git fetch fork

Write-Host ">> git checkout main"
git checkout main

Write-Host ">> git merge fork/main"
git merge fork/main --no-edit
if ($LASTEXITCODE -ne 0) {
    Write-Error "マージに失敗しました（コンフリクトの可能性）。解消後に git commit で完了してください。"
    exit $LASTEXITCODE
}

if ($PushOrigin) {
    Write-Host ">> git push origin main"
    git push origin main
}

Write-Host "完了。状態: git status -sb"
git status -sb
