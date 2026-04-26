#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Faceless収益化ワークフロー — 全体像用の図解画像生成スクリプト

00_全体ワークフロー.md に必要な図解を生成する。
日本語ラベル版。
"""

from pathlib import Path
from google_image_client import GoogleImageClient

# ============================================================
#  出力先
# ============================================================

OUTPUT_DIR = Path.home() / "Documents" / "Obsidian Vault" / "Faceless_収益化ワークフロー" / "図解"

# ============================================================
#  共通スタイル（ビジネス図解用・日本語対応）
# ============================================================

DIAGRAM_STYLE = """
IMPORTANT: Generate this image in LANDSCAPE 16:9 widescreen aspect ratio.
NOT square. The width must be significantly larger than the height.
Width should be approximately 1.78 times the height (e.g., 1792x1008 or 1376x768).

Art style: Clean, modern business infographic style.
- Dark navy blue background (#1a1f3c or similar dark blue)
- White and light colored text/icons for contrast
- Accent colors: teal (#4ecdc4), orange (#ff6b35), purple (#a855f7)
- Flat design with minimal shadows
- Clear visual hierarchy
- Rounded rectangles for cards/boxes
- Simple geometric icons (not detailed illustrations)
- Professional, corporate, modern look
- High contrast for readability

CRITICAL: No realistic human figures or faces. Use only abstract icons, symbols, arrows, and geometric shapes.
Use Japanese text labels as specified in the layout.
No speech bubbles, no watermarks, no decorative text.
"""

# ============================================================
#  図解定義（全体像用・日本語版）
# ============================================================

DIAGRAMS = [
    {
        "filename": "00_受け皿と集客の概念図.png",
        "title": "受け皿を先に作る概念図",
        "prompt": f"""
{DIAGRAM_STYLE}

Diagram type: Concept diagram showing "受け皿を先に作り、それから集客する"

Layout description:
- Two main sections side by side
- Left section (larger, about 60% width): "受け皿" area with 3 stacked boxes
- Right section (smaller, about 40% width): "集客" area with single box
- Large arrow pointing from right to left (traffic flows into foundation)

Left section "受け皿を作る" (3 stacked rounded rectangles):
- Header label above: "受け皿を作る"
- Box 1 (top): Lightbulb icon + "Phase 1 企画・設計" label (teal accent)
- Box 2 (middle): Package/box icon + "Phase 2 商品作成" label (orange accent)
- Box 3 (bottom): Gear/system icon + "Phase 3 セールス構築" label (purple accent)
- A bracket or container shape grouping these 3 boxes

Right section "人を流す":
- Header label above: "人を流す"
- Single box with video/play icon + "Phase 4 集客動画" label (green accent)
- Multiple small arrow icons flowing toward the left section

Bottom text: "仕組みを完成させてから集客を始める"

Visual elements:
- The left section should look like a "container" or "bucket" ready to catch
- Arrows show flow direction: traffic (right) flows into foundation (left)
- Clean, simple, easy to understand at a glance
"""
    },
    {
        "filename": "00_継続運用サイクル.png",
        "title": "継続運用サイクル（毎日/毎週/毎月）",
        "prompt": f"""
{DIAGRAM_STYLE}

Diagram type: Nested cycle diagram showing 毎日/毎週/毎月 routines

Layout description:
- Three concentric rounded rectangles (nested boxes)
- Outer box: 毎月 cycle (largest, purple border)
- Middle box: 毎週 cycle (medium, orange border)
- Inner box: 毎日 cycle (smallest, teal border, in center)

Structure:
- Outer rectangle (毎月 - purple border):
  - Label: "毎月" with calendar icon
  - 4 items with icons:
    - Star icon: "キャラクター進化"
    - Database icon: "悩みDB更新"
    - Package icon: "商品アップデート"
    - Chart icon: "ステップ配信改善"

- Middle rectangle (毎週 - orange border):
  - Label: "毎週" with calendar icon
  - 3 items with icons:
    - Analytics icon: "アナリティクス確認"
    - Chat/LINE icon: "LINE登録数確認"
    - Lightbulb icon: "次週ネタ計画"

- Inner rectangle (毎日 - teal border):
  - Label: "毎日" with sun icon
  - 4 connected items in a horizontal flow with arrows:
    - Bulb: "ネタ出し" → Document: "台本" → Video: "動画制作" → Upload: "投稿"

Visual elements:
- Clear nesting - each box clearly inside the other
- Japanese labels clearly readable
- Professional, clean, organized look
"""
    },
    {
        "filename": "00_成長シミュレーション.png",
        "title": "成長シミュレーション（LINE登録者と収益）",
        "prompt": f"""
{DIAGRAM_STYLE}

Diagram type: Growth chart showing LINE登録者数 vs 収益 milestones

Layout description:
- Horizontal timeline/progress bar at bottom
- Rising stepped chart showing growth stages
- 5 milestone markers along the progression, ascending left to right

Timeline milestones (left to right, ascending height):

1. First milestone (lowest, gray):
   - Gear/build icon
   - Label: "Phase 1〜3 仕組み構築"
   - Sublabel: "1〜2ヶ月目"
   - Revenue: "0円（準備期間）"

2. Second milestone (teal):
   - Video/play icon
   - Label: "動画投稿開始"
   - Sublabel: "2〜3ヶ月目"
   - Revenue: "数千円〜数万円"

3. Third milestone (orange):
   - Person icon with "100"
   - Label: "LINE 100人"
   - Sublabel: "3〜5ヶ月目"
   - Revenue: "5〜15万円/月"

4. Fourth milestone (purple):
   - Group icon with "300"
   - Label: "LINE 300人"
   - Sublabel: "5〜7ヶ月目"
   - Revenue: "15〜30万円/月"

5. Fifth milestone (highest, gold/yellow):
   - Star/trophy icon with "1000"
   - Label: "LINE 1,000人"
   - Sublabel: "7〜12ヶ月目"
   - Revenue: "30〜100万円/月"

Visual elements:
- Ascending stair-step or curved growth line connecting milestones
- Arrow pointing upward showing growth direction
- Clean, motivational design
"""
    },
    {
        "filename": "00_成功の3原則.png",
        "title": "成功のための3つの原則",
        "prompt": f"""
{DIAGRAM_STYLE}

Diagram type: Three-pillar principle diagram

Layout description:
- 3 equal-sized rounded rectangle cards in a horizontal row
- Each card has a large number (1, 2, 3) at top
- Each card has a central icon and Japanese title
- Cards have different accent colors

Card 1 (leftmost - teal accent):
- Large "1" at top
- Icon: Container/bucket catching drops
- Title: "受け皿を先に作る"
- Subtitle: "動画より仕組みが先"

Card 2 (middle - orange accent):
- Large "2" at top
- Icon: Rocket launching or checkmark
- Title: "「完璧」より「完成」"
- Subtitle: "まず世に出す"

Card 3 (rightmost - purple accent):
- Large "3" at top
- Icon: Gears/cogs working together
- Title: "仕組みで勝つ"
- Subtitle: "システム化で効率化"

Visual elements:
- Equal spacing between all three cards
- Japanese text clearly readable
- Numbers are bold and prominent
- Icons are simple and geometric
- Professional, inspirational business design
"""
    },
]

# ============================================================
#  メイン処理
# ============================================================

def main():
    print("=" * 60)
    print("  Faceless収益化ワークフロー — 全体像用 図解画像生成")
    print("  （日本語ラベル版）")
    print("=" * 60)
    print()
    print(f"出力先: {OUTPUT_DIR}")
    print(f"生成数: {len(DIAGRAMS)}枚")
    print()

    # 出力ディレクトリ確認
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # クライアント初期化
    client = GoogleImageClient()
    print()

    # 各図解を生成
    success_count = 0
    for i, diagram in enumerate(DIAGRAMS, 1):
        print("=" * 60)
        print(f"  [{i}/{len(DIAGRAMS)}] {diagram['title']}")
        print("=" * 60)

        output_path = OUTPUT_DIR / diagram["filename"]

        success = client.generate_image(
            prompt=diagram["prompt"],
            output_path=output_path,
            retry=3,
            retry_delay=10.0,
        )

        if success:
            success_count += 1
            client.verify_aspect_ratio(output_path)

        print()

    # 結果サマリー
    print("=" * 60)
    print(f"  完了: {success_count}/{len(DIAGRAMS)}枚 生成成功")
    print("=" * 60)
    print()
    print(f"Finderで確認: open '{OUTPUT_DIR}'")


if __name__ == "__main__":
    main()
