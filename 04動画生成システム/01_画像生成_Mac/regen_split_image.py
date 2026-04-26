#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
個別画像再生成スクリプト (Mac版)

特定のプロンプトを指定して、1枚の画像を再生成する。
対比カットやスプリットスクリーン等、特殊な構図の再生成に最適。

使い方:
    python3 regen_split_image.py --prompt "Scene description..." --output image.png
    python3 regen_split_image.py --prompt-file my_prompt.txt --output scene3.png
    python3 regen_split_image.py --preset split_comparison --output comparison.png
"""

import argparse
import sys
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
#  プリセットプロンプト
# ============================================================

PRESETS = {
    "split_comparison": {
        "title": "対比カット（ビフォー・アフター）",
        "prompt": f"""{HARUMI_STYLE}

Scene: Split screen composition divided vertically in the center.
LEFT HALF (dark, muted colors): A tired, worried elderly Japanese man (65+)
hunched over a desk covered in bills and documents. Dark shadows, rainy window.
RIGHT HALF (bright, warm colors): The same man standing tall in a sunlit garden,
smiling confidently, arms relaxed at his sides. Cherry blossoms.
A subtle golden light beam separates the two halves.
The contrast between despair and hope should be immediately clear.""",
    },
    "character_closeup": {
        "title": "キャラクター接写",
        "prompt": f"""{HARUMI_STYLE}

Scene: Close-up portrait of a kind elderly Japanese woman (around 70 years old).
Silver-white hair in a neat bun. Gentle wrinkles around warm, smiling eyes.
She wears a soft lavender cardigan. The background is a blur of warm golden light
and soft green nature. Her expression conveys wisdom, warmth, and quiet strength.
Lighting: soft rim light from behind, warm fill light on face.""",
    },
    "dramatic_reveal": {
        "title": "ドラマチックな展開",
        "prompt": f"""{HARUMI_STYLE}

Scene: A dramatic moment of realization. A middle-aged Japanese businessman
(around 50, wearing a suit, loosened tie) standing on a rooftop at golden hour.
The city skyline stretches behind him. He is looking up at the sky with
wide eyes and a dawning smile — as if he has just understood something important.
The wind gently moves his hair and tie. Dramatic backlighting from the setting sun.
Rays of golden light break through clouds above.""",
    },
    "peaceful_daily": {
        "title": "平和な日常",
        "prompt": f"""{HARUMI_STYLE}

Scene: A cozy Japanese living room on a quiet Sunday afternoon.
An elderly couple: the husband (70s, reading glasses, gentle face) reading a newspaper,
the wife (late 60s, warm smile) pouring green tea from a beautiful ceramic teapot.
A cat is sleeping on a cushion by the window. Soft afternoon sunlight streams in
through shoji screens. A small vase of seasonal flowers on the low table.
Everything feels peaceful, warm, and timeless.""",
    },
}


# ============================================================
#  メイン処理
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="個別画像再生成ツール（Mac版）— 特殊構図や再生成に最適",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
プリセット一覧:
{chr(10).join(f'  {key:<20} {val["title"]}' for key, val in PRESETS.items())}

使用例:
  python3 regen_split_image.py --preset split_comparison --output split.png
  python3 regen_split_image.py --prompt "A beautiful sunset..." --output sunset.png
  python3 regen_split_image.py --prompt-file my_prompt.txt --output custom.png
        """,
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--prompt",
        type=str,
        help="画像生成プロンプト（直接指定）",
    )
    group.add_argument(
        "--prompt-file",
        type=str,
        help="プロンプトが書かれたテキストファイルのパス",
    )
    group.add_argument(
        "--preset",
        type=str,
        choices=list(PRESETS.keys()),
        help="プリセットプロンプトの名前",
    )

    parser.add_argument(
        "--output",
        type=str,
        required=True,
        help="出力ファイル名またはパス（例: my_image.png）",
    )
    parser.add_argument(
        "--no-style",
        action="store_true",
        help="Harumiスタイルを付与しない（--prompt 使用時のみ有効）",
    )
    parser.add_argument(
        "--model",
        type=str,
        choices=["nano-banana-2", "nano-banana-pro"],
        help="使用モデルを指定",
    )
    parser.add_argument(
        "--retry",
        type=int,
        default=3,
        help="リトライ回数（デフォルト: 3）",
    )

    args = parser.parse_args()

    print()
    print("=" * 60)
    print("  🔄 個別画像再生成ツール（Mac版）")
    print("=" * 60)
    print()

    # プロンプトの決定
    if args.preset:
        preset = PRESETS[args.preset]
        prompt = preset["prompt"]
        print(f"[OK] プリセット: {preset['title']}")
    elif args.prompt_file:
        prompt_path = Path(args.prompt_file).expanduser()
        if not prompt_path.exists():
            print(f"[NG] ファイルが見つかりません: {prompt_path}")
            sys.exit(1)
        prompt = prompt_path.read_text(encoding="utf-8").strip()
        if not args.no_style and "LANDSCAPE 16:9" not in prompt:
            prompt = f"{HARUMI_STYLE}\n\n{prompt}"
        print(f"[OK] プロンプトファイル: {prompt_path}")
    else:
        prompt = args.prompt
        if not args.no_style and "LANDSCAPE 16:9" not in prompt:
            prompt = f"{HARUMI_STYLE}\n\n{prompt}"
        print("[OK] カスタムプロンプトを使用")

    # 出力パスの決定
    output_path = Path(args.output).expanduser()
    if not output_path.suffix:
        output_path = output_path.with_suffix(".png")
    if not output_path.is_absolute():
        output_path = Path(__file__).parent / "output" / output_path
    output_path.parent.mkdir(parents=True, exist_ok=True)
    print(f"[OK] 出力先: {output_path}")

    # モデル指定
    preferred_model = None
    if args.model == "nano-banana-2":
        preferred_model = "gemini-3.1-flash-image-preview"
    elif args.model == "nano-banana-pro":
        preferred_model = "gemini-3-pro-image-preview"

    # クライアント初期化＆生成
    print()
    client = GoogleImageClient()
    print()

    success = client.generate_image(
        prompt=prompt,
        output_path=output_path,
        retry=args.retry,
        preferred_model=preferred_model,
    )

    if success:
        client.verify_aspect_ratio(output_path)
        print()
        print(f"[OK] 生成成功: {output_path}")
        print(f"  💡 Finderで確認: open \"{output_path}\"")
    else:
        print()
        print("[NG] 生成に失敗しました。プロンプトの内容を調整してみてください。")
        sys.exit(1)

    print()


if __name__ == "__main__":
    main()
