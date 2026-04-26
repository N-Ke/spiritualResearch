#!/bin/bash
# ============================================================
#  漫画イラスト一括生成シェルスクリプト (Mac版)
#
#  このファイルをダブルクリックまたはターミナルから実行すると
#  generate_manga.py が起動し、画像が自動生成されます。
#
#  初回のみ実行権限の付与が必要です:
#    chmod +x generate_manga.sh
#
# ============================================================

# スクリプトのあるディレクトリに移動
cd "$(dirname "$0")"

echo ""
echo "============================================================"
echo "  🎨 漫画イラスト一括生成ツール (Mac版)"
echo "============================================================"
echo ""

# Python3 の存在確認
if ! command -v python3 &> /dev/null; then
    echo "[NG] python3 が見つかりません。"
    echo ""
    echo "以下のいずれかの方法でインストールしてください："
    echo "  1. Python公式サイト: https://www.python.org/downloads/"
    echo "  2. Homebrew: brew install python@3.12"
    echo ""
    echo "Press any key to exit..."
    read -n 1
    exit 1
fi

echo "[OK] Python3: $(python3 --version)"
echo ""

# 必要なパッケージの確認
python3 -c "import google.genai; import dotenv; import PIL" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "[INFO] 必要なパッケージをインストール中..."
    echo ""
    pip3 install google-genai python-dotenv Pillow
    echo ""
    if [ $? -ne 0 ]; then
        echo "[NG] パッケージのインストールに失敗しました。"
        echo "  手動で以下を実行してください:"
        echo "  pip3 install google-genai python-dotenv Pillow"
        echo ""
        echo "Press any key to exit..."
        read -n 1
        exit 1
    fi
fi

# 画像生成を実行
python3 generate_manga.py "$@"
EXIT_CODE=$?

echo ""
if [ $EXIT_CODE -eq 0 ]; then
    echo "[OK] 生成完了！"
else
    echo "[NG] 一部のシーン生成に失敗しました。"
fi

echo ""
echo "Press any key to exit..."
read -n 1
