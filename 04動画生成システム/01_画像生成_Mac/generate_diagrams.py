#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Faceless収益化ワークフロー用 図解画像生成スクリプト

Nano Banana 2を使用してビジネス図解を生成する。
"""

from pathlib import Path
from google_image_client import GoogleImageClient

# ============================================================
#  出力先
# ============================================================

OUTPUT_DIR = Path.home() / "Documents" / "Obsidian Vault" / "Faceless_収益化ワークフロー" / "図解"

# ============================================================
#  共通スタイル（ビジネス図解用）
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
No Japanese characters in the image - use simple English labels or icons only.
No speech bubbles, no watermarks, no decorative text.
"""

# ============================================================
#  図解定義
# ============================================================

DIAGRAMS = [
    {
        "filename": "16_D-BE_UNICK_8要素関係図.png",
        "title": "D-BE UNICK 8要素関係図",
        "prompt": f"""
{DIAGRAM_STYLE}

Diagram type: Framework diagram showing 8 elements in two phases.

Layout description:
- Two horizontal rows of 4 rounded rectangle cards each
- Top row has a header label "Phase 1" with subtitle about foundation
- Bottom row has a header label "Phase 2" with subtitle about action
- Large downward arrow connecting the two rows in the center
- Each card contains: a single letter (D, B, E, U, N, I, C, K) prominently displayed
- Cards have alternating accent colors (teal and orange)
- Clean spacing between elements

Top row cards (left to right):
- Card 1: Large "D" letter, teal accent
- Card 2: Large "B" letter, orange accent
- Card 3: Large "E" letter, teal accent
- Card 4: Large "U" letter, orange accent

Bottom row cards (left to right):
- Card 5: Large "N" letter, purple accent
- Card 6: Large "I" letter, teal accent
- Card 7: Large "C" letter, orange accent
- Card 8: Large "K" letter, purple accent

Visual style: Minimalist, bold typography, geometric shapes only.
"""
    },
    {
        "filename": "28_動画制作パイプライン.png",
        "title": "動画制作パイプライン",
        "prompt": f"""
{DIAGRAM_STYLE}

Diagram type: Horizontal pipeline/flow chart showing video production process.

Layout description:
- 5 stages connected by arrows flowing left to right
- Each stage is a rounded rectangle card with an icon at top
- Large arrows between each stage
- All on dark navy background
- Professional infographic style

Stages (left to right):
1. Document/script icon - "Script" label
2. Image/photo icon - "Images" label (with "AI" badge)
3. Microphone/audio icon - "Voice" label (with "AI" badge)
4. Film/video icon - "Edit" label
5. Upload/publish icon - "Publish" label

Visual elements:
- Each card has white background with rounded corners
- Icons are simple line icons in teal or orange
- Arrows are large, bold, teal colored
- "AI" badges are small orange pills on relevant stages
- Clean, minimal, professional look
"""
    },
    {
        "filename": "08_商品企画5つの大黒柱.png",
        "title": "商品企画の5つの大黒柱",
        "prompt": f"""
{DIAGRAM_STYLE}

Diagram type: 5-pillar structure diagram showing key elements of product planning.

Layout description:
- A temple/building-like structure with 5 vertical pillars
- Roof/header at top showing the concept
- 5 equal-width pillars side by side
- Foundation/base at bottom
- Professional architectural metaphor

Structure:
- Top roof element: triangular or curved top piece
- 5 Pillars (left to right), each a tall rounded rectangle:
  - Pillar 1: Target icon (bullseye)
  - Pillar 2: Star/goal icon
  - Pillar 3: Lightbulb/solution icon
  - Pillar 4: Document/format icon
  - Pillar 5: Person/unique icon
- Bottom foundation: horizontal bar connecting all pillars

Colors:
- Pillars alternate between white and light blue backgrounds
- Icons in teal and orange
- Foundation in darker shade
- Overall professional business look
"""
    },
    {
        "filename": "19_ステップ配信10日間フロー.png",
        "title": "ステップ配信10日間フロー",
        "prompt": f"""
{DIAGRAM_STYLE}

Diagram type: Timeline/calendar flow showing 10-day email sequence.

Layout description:
- Horizontal timeline with 10 day markers
- Each day represented by a small card or circle
- Grouped into 4 phases with different colors
- Arrows showing progression
- Key milestones highlighted

Timeline structure:
- Days 1-3: First phase (teal color) - "Build Trust"
- Days 4-6: Second phase (orange color) - "Show Value"
- Days 7-8: Third phase (purple color) - "Create Urgency"
- Days 9-10: Fourth phase (green color) - "Close Sale"

Visual elements:
- 10 numbered circles or small cards in a row
- Color-coded sections with phase labels above
- Large arrow flowing left to right
- Star or highlight on Day 10 (final goal)
- Clean, minimal timeline design
"""
    },
    {
        "filename": "30_改善サイクル図.png",
        "title": "改善サイクル（PDCA）",
        "prompt": f"""
{DIAGRAM_STYLE}

Diagram type: Circular PDCA cycle diagram.

Layout description:
- Large circular flow with 4 quadrants
- Arrows connecting each quadrant in clockwise direction
- Each quadrant is a different color
- Center shows the cycle concept
- Professional business cycle visualization

Quadrants (clockwise from top):
1. Top-right: "P" (Plan) - teal background
2. Bottom-right: "D" (Do) - orange background
3. Bottom-left: "C" (Check) - purple background
4. Top-left: "A" (Act) - green background

Visual elements:
- Large curved arrows connecting quadrants
- Each quadrant has a large letter and simple icon
- Center circle with cycle/refresh icon
- Clean, bold, geometric design
- Professional corporate look
"""
    },
]

# ============================================================
#  メイン処理
# ============================================================

def main():
    print("=" * 60)
    print("  Faceless収益化ワークフロー — 図解画像生成")
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
