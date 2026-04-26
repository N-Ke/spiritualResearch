#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
年金台本用シーン画像生成スクリプト (Mac版)

年金関連の台本に合わせた4枚のシーン画像を生成する。
harumiスタイル（ジブリ風温かいアニメ調）で統一。

使い方:
    python3 generate_pension_scenes.py
    python3 generate_pension_scenes.py --output ~/Desktop/pension_images
"""

import argparse
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from google_image_client import GoogleImageClient


# ============================================================
#  Harumi スタイル定義
# ============================================================

HARUMI_STYLE = """IMPORTANT: Generate this image in LANDSCAPE 16:9 widescreen aspect ratio
(e.g. 1792x1024 or similar wide format). NOT square.
The width must be significantly larger than the height.

Art style: Soft, warm Japanese anime illustration style inspired by Studio Ghibli.
Clean linework, soft coloring, pastel palette, warm golden lighting.
No text, no speech bubbles, no writing in the image.
No watermarks, no signatures, no UI elements."""


# ============================================================
#  年金シーン定義（4枚）
# ============================================================

PENSION_SCENES = [
    {
        "id": "pension-1",
        "filename": "pension_scene1_worry.png",
        "title": "老後の不安",
        "prompt": f"""{HARUMI_STYLE}

Scene: An elderly Japanese man (68 years old, gray hair, gentle wrinkles)
sitting alone on a park bench in autumn. He is looking down at a pension notice
letter in his hands with a worried, contemplative expression.
Fallen yellow ginkgo leaves scattered on the ground around him.
The autumn light is soft but the overall mood is slightly melancholic.
Camera angle: medium shot, slightly from the side, capturing his profile.""",
    },
    {
        "id": "pension-2",
        "filename": "pension_scene2_discovery.png",
        "title": "新しい発見",
        "prompt": f"""{HARUMI_STYLE}

Scene: The same elderly Japanese man (68, gray hair) now sitting at a bright,
modern community center. A kind young female staff member (late 20s, professional
attire) is explaining something on a document, pointing at it with a warm smile.
The man's expression is changing from worry to hope — his eyes are slightly wider.
Warm sunlight streaming through large windows. Books and informational pamphlets
visible in the background.
Camera angle: medium shot showing both characters, slightly from the man's perspective.""",
    },
    {
        "id": "pension-3",
        "filename": "pension_scene3_action.png",
        "title": "行動を起こす",
        "prompt": f"""{HARUMI_STYLE}

Scene: The elderly Japanese man (68, gray hair) sitting at his home desk,
filling out an application form with determination and a slight smile.
A cup of green tea steams gently beside him. His reading glasses are perched
on his nose. The room is cozy with warm lamplight and family photos on the shelf.
A calendar on the wall shows circled dates. His posture shows newfound confidence.
Camera angle: close-up to medium shot, slightly above, showing him writing.""",
    },
    {
        "id": "pension-4",
        "filename": "pension_scene4_peace.png",
        "title": "安心の未来",
        "prompt": f"""{HARUMI_STYLE}

Scene: The elderly Japanese man (68, gray hair) and his wife (65, gentle smile,
short dark hair with some gray) enjoying a peaceful morning in their garden.
They are having breakfast at a small outdoor table — rice, miso soup, grilled fish.
Cherry blossoms are in full bloom overhead. A small dog sits at their feet.
Both are smiling warmly, radiating contentment and peace of mind.
The morning golden light makes everything glow softly.
Camera angle: wide shot showing the beautiful garden and the peaceful couple.""",
    },
]


# ============================================================
#  メイン処理
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="年金台本用シーン画像生成（Mac版）— 4枚のharumiスタイルイラスト",
    )
    parser.add_argument(
        "--output",
        type=str,
        help="画像の出力先ディレクトリ（デフォルト: ../03_Remotion/public/images/）",
    )
    parser.add_argument(
        "--scene",
        nargs="+",
        help="特定のシーンIDのみ生成（例: pension-1 pension-3）",
    )

    args = parser.parse_args()

    print()
    print("=" * 60)
    print("  🏛️ 年金台本用シーン画像生成（Mac版）")
    print("  harumiスタイル — 4枚セット")
    print("=" * 60)
    print()

    # 出力先
    script_dir = Path(__file__).parent
    if args.output:
        output_dir = Path(args.output).expanduser()
    else:
        output_dir = script_dir.parent / "03_Remotion" / "public" / "images"
    output_dir.mkdir(parents=True, exist_ok=True)
    print(f"[OK] 出力先: {output_dir}")
    print()

    # シーンフィルタリング
    scenes = PENSION_SCENES
    if args.scene:
        target_ids = set(args.scene)
        scenes = [s for s in scenes if s["id"] in target_ids]
        if not scenes:
            print("[NG] 指定されたシーンが見つかりません。")
            print("  利用可能なID:", ", ".join(s["id"] for s in PENSION_SCENES))
            sys.exit(1)

    # クライアント初期化
    client = GoogleImageClient()
    print()

    # 生成ループ
    total = len(scenes)
    success_count = 0

    for i, scene in enumerate(scenes, 1):
        print()
        print("=" * 60)
        print(f"  [{i}/{total}] {scene['title']}")
        print("=" * 60)

        output_path = output_dir / scene["filename"]
        success = client.generate_image(
            prompt=scene["prompt"],
            output_path=output_path,
        )

        if success:
            client.verify_aspect_ratio(output_path)
            success_count += 1

        if i < total:
            time.sleep(2.0)

    # サマリー
    print()
    print("=" * 60)
    print(f"  完了: {success_count}/{total} シーン成功")
    print(f"  出力先: {output_dir}")
    print(f"  💡 Finderで確認: open \"{output_dir}\"")
    print("=" * 60)
    print()


if __name__ == "__main__":
    main()
