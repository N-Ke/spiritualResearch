#!/usr/bin/env python3
"""
オンラインテキスト商品化 → Notionアップローダー
==================================================
- YouTubeタイトル記事（Step3_YouTubeタイトル_出力.md + 図解5枚）
- 四柱推命記事（四柱推命_仕事人間関係_Lite.md + 図解3枚）
をNotionにアップロードする

使い方:
cd "/Users/taisuke/Documents/Obsidian Vault/オンラインテキスト商品化/実行結果"
python3 upload_to_notion.py
"""

import json
import re
import base64
import requests
from pathlib import Path

# 設定
CONFIG_PATH = Path("/Users/taisuke/Documents/Obsidian Vault/📺_YouTube/セミナー関係/notion_config.json")
IMAGES_DIR = Path(__file__).parent / "images"

# アップロード対象の記事
ARTICLES = [
    {
        "file": Path(__file__).parent / "Step3_YouTubeタイトル_出力.md",
        "title": "YouTubeタイトルの考え方｜センスじゃなく構造で作る【図解付き】",
        "images": [
            "図解1_3つの構造.png",
            "図解2_欲求パターン.png",
            "図解3_粒度スケール.png",
            "図解4_クリック引力.png",
            "図解5_失敗パターン.png",
        ],
    },
    {
        "file": Path(__file__).parent / "四柱推命_仕事人間関係_Lite.md",
        "title": "「なぜあの人とだけ、うまくいかないのか」四柱推命で読み解く職場の人間関係【図解付き】",
        "images": [
            "3つの関係タイプ.png",
            "五行相関図.png",
            "3ステップ活用法.png",
        ],
    },
]


def load_config():
    """設定ファイルを読み込み"""
    if not CONFIG_PATH.exists():
        print(f"❌ 設定ファイルが見つかりません: {CONFIG_PATH}")
        return None
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def upload_to_imgbb(image_path: Path, api_key: str) -> str:
    """imgBBに画像をアップロードしてURLを返す"""
    print(f"   📤 imgBBアップロード中: {image_path.name}")
    with open(image_path, "rb") as f:
        image_data = f.read()
    if len(image_data) == 0:
        print(f"   ❌ ファイルが空です")
        return None

    image_base64 = base64.b64encode(image_data).decode("utf-8")
    try:
        response = requests.post(
            "https://api.imgbb.com/1/upload",
            data={"key": api_key, "image": image_base64, "name": image_path.stem},
            timeout=60,
        )
        result = response.json()
        if result.get("success"):
            url = result["data"]["url"]
            print(f"   ✅ 完了: {url[:60]}...")
            return url
        else:
            print(f"   ❌ 失敗: {result.get('error', {}).get('message', '不明')}")
            return None
    except Exception as e:
        print(f"   ⚠️ エラー: {e}")
        return None


# ── Notion ブロック生成 ─────────────────────────


def create_rich_text(text: str, bold=False, code=False, color="default"):
    return {
        "type": "text",
        "text": {"content": text},
        "annotations": {
            "bold": bold,
            "italic": False,
            "strikethrough": False,
            "underline": False,
            "code": code,
            "color": color,
        },
    }


def parse_inline_formatting(text: str) -> list:
    """**太字** と `コード` を解析"""
    rich_text = []
    pattern = r"\*\*(.+?)\*\*|`([^`]+)`"
    last_end = 0
    for match in re.finditer(pattern, text):
        if match.start() > last_end:
            before = text[last_end : match.start()]
            if before:
                rich_text.append(create_rich_text(before))
        if match.group(1):
            rich_text.append(create_rich_text(match.group(1), bold=True))
        elif match.group(2):
            rich_text.append(create_rich_text(match.group(2), code=True))
        last_end = match.end()
    if last_end < len(text):
        remaining = text[last_end:]
        if remaining:
            rich_text.append(create_rich_text(remaining))
    if not rich_text:
        rich_text.append(create_rich_text(text))
    return rich_text


def create_paragraph_block(text: str):
    return {"type": "paragraph", "paragraph": {"rich_text": parse_inline_formatting(text)}}


def create_heading1_block(text: str):
    return {
        "type": "heading_1",
        "heading_1": {"rich_text": [create_rich_text(text, bold=True)], "is_toggleable": False},
    }


def create_heading2_block(text: str):
    return {
        "type": "heading_2",
        "heading_2": {"rich_text": [create_rich_text(text, bold=True)], "is_toggleable": False},
    }


def create_heading3_block(text: str):
    return {"type": "heading_3", "heading_3": {"rich_text": [create_rich_text(text, bold=True)]}}


def create_bullet_block(text: str):
    return {"type": "bulleted_list_item", "bulleted_list_item": {"rich_text": parse_inline_formatting(text)}}


def create_numbered_block(text: str):
    return {"type": "numbered_list_item", "numbered_list_item": {"rich_text": parse_inline_formatting(text)}}


def create_image_block(url: str, caption: str = ""):
    block = {"type": "image", "image": {"type": "external", "external": {"url": url}}}
    if caption:
        block["image"]["caption"] = [create_rich_text(caption)]
    return block


def create_code_block(code: str, language: str = "plain text"):
    return {"type": "code", "code": {"rich_text": [create_rich_text(code)], "language": language}}


def create_callout_block(text: str, emoji: str = "💡"):
    return {
        "type": "callout",
        "callout": {
            "rich_text": parse_inline_formatting(text),
            "icon": {"type": "emoji", "emoji": emoji},
        },
    }


def create_quote_block(text: str):
    return {"type": "quote", "quote": {"rich_text": parse_inline_formatting(text)}}


def create_table_block(headers: list, rows: list):
    """テーブルブロックを作成"""
    table_width = len(headers)
    children = []

    # ヘッダー行
    header_cells = [[create_rich_text(h, bold=True)] for h in headers]
    children.append({"type": "table_row", "table_row": {"cells": header_cells}})

    # データ行
    for row in rows:
        data_cells = [parse_inline_formatting(cell) for cell in row]
        children.append({"type": "table_row", "table_row": {"cells": data_cells}})

    return {
        "type": "table",
        "table": {
            "table_width": table_width,
            "has_column_header": True,
            "has_row_header": False,
            "children": children,
        },
    }


# ── Markdown → Notion ブロック変換 ──────────────


def parse_markdown_to_blocks(content: str, image_url_map: dict) -> list:
    """MarkdownをNotionブロックに変換"""
    blocks = []
    lines = content.split("\n")
    i = 0
    current_paragraph = []

    def flush_paragraph():
        nonlocal current_paragraph
        if current_paragraph:
            text = "\n".join(current_paragraph)
            if text.strip():
                blocks.append(create_paragraph_block(text))
            current_paragraph = []

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # 空行
        if not stripped:
            flush_paragraph()
            i += 1
            continue

        # 画像 ![alt](path)
        img_match = re.match(r"!\[([^\]]*)\]\(([^)]+)\)", stripped)
        if img_match:
            flush_paragraph()
            alt_text = img_match.group(1)
            img_path = img_match.group(2)
            # ファイル名を抽出
            img_filename = Path(img_path).name
            img_url = image_url_map.get(img_filename)
            if img_url:
                blocks.append(create_image_block(img_url, alt_text))
            else:
                blocks.append(create_paragraph_block(f"[画像: {alt_text}]"))
            i += 1
            continue

        # H1見出し
        if stripped.startswith("# ") and not stripped.startswith("## "):
            flush_paragraph()
            blocks.append(create_heading1_block(stripped[2:].strip()))
            i += 1
            continue

        # H2見出し
        if stripped.startswith("## ") and not stripped.startswith("### "):
            flush_paragraph()
            blocks.append(create_heading2_block(stripped[3:].strip()))
            i += 1
            continue

        # H3見出し
        if stripped.startswith("### ") and not stripped.startswith("#### "):
            flush_paragraph()
            blocks.append(create_heading3_block(stripped[4:].strip()))
            i += 1
            continue

        # H4見出し（H3として表示）
        if stripped.startswith("#### "):
            flush_paragraph()
            blocks.append(create_heading3_block(stripped[5:].strip()))
            i += 1
            continue

        # 区切り線
        if stripped == "---" or stripped == "***":
            flush_paragraph()
            blocks.append({"type": "divider", "divider": {}})
            i += 1
            continue

        # 「--- ここから有料 ---」のような行
        if "ここから有料" in stripped:
            flush_paragraph()
            blocks.append(create_callout_block("ここから有料", "🔒"))
            i += 1
            continue

        # 引用 > テキスト
        if stripped.startswith("> "):
            flush_paragraph()
            quote_text = stripped[2:]
            # 💡マークがある場合はcalloutに
            if quote_text.startswith("💡"):
                blocks.append(create_callout_block(quote_text[2:].strip(), "💡"))
            else:
                blocks.append(create_quote_block(quote_text))
            i += 1
            continue

        # 箇条書き - テキスト
        if stripped.startswith("- ") or stripped.startswith("* "):
            flush_paragraph()
            blocks.append(create_bullet_block(stripped[2:]))
            i += 1
            continue

        # 番号リスト
        num_match = re.match(r"^(\d+)\.\s+(.+)", stripped)
        if num_match:
            flush_paragraph()
            blocks.append(create_numbered_block(num_match.group(2)))
            i += 1
            continue

        # テーブル
        if stripped.startswith("|") and i + 1 < len(lines) and re.match(r"^\|[\s\-:]+\|", lines[i + 1].strip()):
            flush_paragraph()
            # ヘッダー行
            headers = [c.strip() for c in stripped.strip("|").split("|")]
            i += 2  # ヘッダー行と区切り行をスキップ
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                row = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                rows.append(row)
                i += 1
            blocks.append(create_table_block(headers, rows))
            continue

        # コードブロック
        if stripped.startswith("```"):
            flush_paragraph()
            language = stripped.replace("```", "").strip() or "plain text"
            code_lines = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                code_lines.append(lines[i])
                i += 1
            if i < len(lines):
                i += 1  # 閉じ```
            if code_lines:
                blocks.append(create_code_block("\n".join(code_lines), language))
            continue

        # 通常テキスト
        current_paragraph.append(line)
        i += 1

    flush_paragraph()
    return blocks


# ── Notion API ────────────────────────────────


def create_notion_page(config: dict, title: str, blocks: list) -> dict:
    """Notionにページを作成"""
    headers = {
        "Authorization": f"Bearer {config['notion_api']['api_key']}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28",
    }

    blocks_to_send = blocks[:100]
    data = {
        "parent": {"page_id": config["notion_api"]["parent_page_id"]},
        "properties": {"title": {"title": [{"text": {"content": title}}]}},
        "children": blocks_to_send,
    }

    response = requests.post("https://api.notion.com/v1/pages", headers=headers, json=data)

    if response.status_code == 200:
        page_data = response.json()
        page_id = page_data["id"]
        # 残りのブロックを追加
        if len(blocks) > 100:
            append_blocks(config, page_id, blocks[100:])
        return page_data
    else:
        print(f"   ❌ エラー: {response.status_code}")
        print(f"   {json.dumps(response.json(), ensure_ascii=False, indent=2)[:500]}")
        return None


def append_blocks(config: dict, page_id: str, blocks: list):
    """追加のブロックをページに追加"""
    headers = {
        "Authorization": f"Bearer {config['notion_api']['api_key']}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28",
    }
    url = f"https://api.notion.com/v1/blocks/{page_id}/children"

    for i in range(0, len(blocks), 100):
        chunk = blocks[i : i + 100]
        response = requests.patch(url, headers=headers, json={"children": chunk})
        if response.status_code != 200:
            print(f"   ⚠️ ブロック追加エラー: {response.status_code}")


# ── メイン処理 ────────────────────────────────


def main():
    print("=" * 80)
    print("📝 オンラインテキスト商品化 → Notionアップロード")
    print("=" * 80)

    # 設定読み込み
    print("\n📂 設定ファイルを読み込み中...")
    config = load_config()
    if not config:
        return
    imgbb_key = config.get("imgbb_api", {}).get("api_key")
    print("   ✅ 完了")

    uploaded_urls = []

    for article_info in ARTICLES:
        print(f"\n{'='*80}")
        print(f"📄 {article_info['title']}")
        print(f"{'='*80}")

        # ファイル確認
        if not article_info["file"].exists():
            print(f"   ❌ ファイルが見つかりません: {article_info['file']}")
            continue

        # 画像をimgBBにアップロード
        image_url_map = {}
        if article_info["images"] and imgbb_key:
            print(f"\n🖼️  画像をimgBBにアップロード中... ({len(article_info['images'])}枚)")
            for img_name in article_info["images"]:
                img_path = IMAGES_DIR / img_name
                if img_path.exists():
                    url = upload_to_imgbb(img_path, imgbb_key)
                    if url:
                        image_url_map[img_name] = url
                else:
                    print(f"   ⚠️ 画像が見つかりません: {img_name}")

        # Markdownを読み込み
        print(f"\n📖 Markdownを読み込み中...")
        with open(article_info["file"], "r", encoding="utf-8") as f:
            content = f.read()

        # Notionブロックに変換
        print(f"📦 Notionブロックに変換中...")
        blocks = parse_markdown_to_blocks(content, image_url_map)
        print(f"   ブロック数: {len(blocks)}")

        # Notionにアップロード
        print(f"\n🚀 Notionにアップロード中...")
        result = create_notion_page(config, article_info["title"], blocks)

        if result:
            page_url = result.get("url", "N/A")
            print(f"   ✅ アップロード成功！")
            print(f"   📍 URL: {page_url}")
            uploaded_urls.append({"title": article_info["title"], "url": page_url})
        else:
            print(f"   ❌ アップロード失敗")

    # 結果を保存
    if uploaded_urls:
        result_file = Path(__file__).parent / "notion_urls.txt"
        with open(result_file, "w", encoding="utf-8") as f:
            f.write("オンラインテキスト商品化 Notion URL一覧\n")
            f.write("=" * 80 + "\n\n")
            for item in uploaded_urls:
                f.write(f"【{item['title']}】\n")
                f.write(f"{item['url']}\n\n")
        print(f"\n💾 URL一覧を保存: {result_file}")

    print(f"\n{'='*80}")
    print("✅ 全処理完了！")
    print("=" * 80)


if __name__ == "__main__":
    main()
