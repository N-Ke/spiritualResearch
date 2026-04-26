#!/usr/bin/env python3
"""
YouTubeタイトル記事（Notion用改行版）再アップロード
既にimgBBにアップロード済みの画像URLを使用
"""

import json
import re
import requests
from pathlib import Path

CONFIG_PATH = Path("/Users/taisuke/Documents/Obsidian Vault/📺_YouTube/セミナー関係/notion_config.json")
ARTICLE_PATH = Path(__file__).parent / "Step3_YouTubeタイトル_Notion用.md"

# 前回アップロード済みの画像URL
IMAGE_URLS = {
    "図解1_3つの構造.png": "https://i.ibb.co/h54njW9/1-3.png",
    "図解2_欲求パターン.png": "https://i.ibb.co/4wL3Qq7D/2.png",
    "図解3_粒度スケール.png": "https://i.ibb.co/wFZ7JhP5/3.png",
    "図解4_クリック引力.png": "https://i.ibb.co/214B4g6k/4.png",
    "図解5_失敗パターン.png": "https://i.ibb.co/wZ9GFR0J/5.png",
}


def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def create_rich_text(text, bold=False, code=False, color="default"):
    return {
        "type": "text",
        "text": {"content": text},
        "annotations": {"bold": bold, "italic": False, "strikethrough": False, "underline": False, "code": code, "color": color},
    }


def parse_inline_formatting(text):
    rich_text = []
    pattern = r"\*\*(.+?)\*\*|`([^`]+)`"
    last_end = 0
    for match in re.finditer(pattern, text):
        if match.start() > last_end:
            before = text[last_end:match.start()]
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


def parse_markdown_to_blocks(content, image_urls):
    blocks = []
    lines = content.split("\n")
    i = 0

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if not stripped:
            i += 1
            continue

        # 画像
        img_match = re.match(r"!\[([^\]]*)\]\(([^)]+)\)", stripped)
        if img_match:
            alt_text = img_match.group(1)
            img_path = img_match.group(2)
            img_filename = Path(img_path).name
            img_url = image_urls.get(img_filename)
            if img_url:
                block = {"type": "image", "image": {"type": "external", "external": {"url": img_url}}}
                if alt_text:
                    block["image"]["caption"] = [create_rich_text(alt_text)]
                blocks.append(block)
            i += 1
            continue

        # H1
        if stripped.startswith("# ") and not stripped.startswith("## "):
            blocks.append({"type": "heading_1", "heading_1": {"rich_text": [create_rich_text(stripped[2:].strip(), bold=True)], "is_toggleable": False}})
            i += 1
            continue

        # H2
        if stripped.startswith("## ") and not stripped.startswith("### "):
            blocks.append({"type": "heading_2", "heading_2": {"rich_text": [create_rich_text(stripped[3:].strip(), bold=True)], "is_toggleable": False}})
            i += 1
            continue

        # H3
        if stripped.startswith("### "):
            blocks.append({"type": "heading_3", "heading_3": {"rich_text": [create_rich_text(stripped[4:].strip(), bold=True)]}})
            i += 1
            continue

        # 区切り線
        if stripped == "---" or stripped == "***":
            blocks.append({"type": "divider", "divider": {}})
            i += 1
            continue

        # ここから有料
        if "ここから有料" in stripped:
            blocks.append({"type": "callout", "callout": {"rich_text": [create_rich_text("ここから有料")], "icon": {"type": "emoji", "emoji": "🔒"}}})
            i += 1
            continue

        # 引用
        if stripped.startswith("> "):
            quote_text = stripped[2:]
            blocks.append({"type": "quote", "quote": {"rich_text": parse_inline_formatting(quote_text)}})
            i += 1
            continue

        # 箇条書き（インデント付き含む）
        if stripped.startswith("- ") or stripped.startswith("* "):
            blocks.append({"type": "bulleted_list_item", "bulleted_list_item": {"rich_text": parse_inline_formatting(stripped[2:])}})
            # インデント付きの子項目を確認
            i += 1
            while i < len(lines) and lines[i].strip().startswith("  - "):
                child_text = lines[i].strip()[4:]
                # 子項目はbullet_list_itemのchildrenとして追加するべきだが、
                # Notion APIの制約上、別のbulletとして追加
                blocks.append({"type": "bulleted_list_item", "bulleted_list_item": {"rich_text": parse_inline_formatting(child_text)}})
                i += 1
            continue

        # コードブロック
        if stripped.startswith("```"):
            language = stripped.replace("```", "").strip() or "plain text"
            code_lines = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                code_lines.append(lines[i])
                i += 1
            if i < len(lines):
                i += 1
            if code_lines:
                blocks.append({"type": "code", "code": {"rich_text": [create_rich_text("\n".join(code_lines))], "language": language}})
            continue

        # 通常テキスト
        blocks.append({"type": "paragraph", "paragraph": {"rich_text": parse_inline_formatting(stripped)}})
        i += 1

    return blocks


def create_notion_page(config, title, blocks):
    headers = {
        "Authorization": f"Bearer {config['notion_api']['api_key']}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28",
    }

    data = {
        "parent": {"page_id": config["notion_api"]["parent_page_id"]},
        "properties": {"title": {"title": [{"text": {"content": title}}]}},
        "children": blocks[:100],
    }

    response = requests.post("https://api.notion.com/v1/pages", headers=headers, json=data)

    if response.status_code == 200:
        page_data = response.json()
        page_id = page_data["id"]
        # 残りのブロックを追加
        remaining = blocks[100:]
        url = f"https://api.notion.com/v1/blocks/{page_id}/children"
        for j in range(0, len(remaining), 100):
            chunk = remaining[j:j+100]
            requests.patch(url, headers=headers, json={"children": chunk})
        return page_data
    else:
        print(f"❌ エラー: {response.status_code}")
        print(response.text[:500])
        return None


def main():
    print("=" * 60)
    print("📝 YouTubeタイトル記事（改行改善版）→ Notion再アップロード")
    print("=" * 60)

    config = load_config()

    print("\n📖 記事を読み込み中...")
    with open(ARTICLE_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    print("📦 Notionブロックに変換中...")
    blocks = parse_markdown_to_blocks(content, IMAGE_URLS)
    print(f"   ブロック数: {len(blocks)}")

    print("\n🚀 Notionにアップロード中...")
    result = create_notion_page(
        config,
        "YouTubeタイトルの考え方｜センスじゃなく構造で作る【図解付き・改行改善版】",
        blocks,
    )

    if result:
        url = result.get("url", "N/A")
        print(f"\n✅ アップロード成功！")
        print(f"📍 URL: {url}")

        # URL保存
        url_file = Path(__file__).parent / "notion_urls_v2.txt"
        with open(url_file, "w", encoding="utf-8") as f:
            f.write(f"YouTubeタイトル記事（改行改善版）\n{url}\n")
        print(f"💾 URL保存: {url_file}")
    else:
        print("❌ アップロード失敗")


if __name__ == "__main__":
    main()
