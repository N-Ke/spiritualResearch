#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
漫画イラスト一括生成スクリプト (Mac版)

台本のシーン定義に基づいて、アニメ風イラストを一括生成する。
scene_data.json からシーン情報を読み込むか、
JSON がない場合はデフォルトのサンプルシーンで動作する。

使い方:
    python3 generate_manga.py                          # 全シーンを生成
    python3 generate_manga.py --scene A-1 A-2 B-1      # 特定シーンのみ
    python3 generate_manga.py --output ~/Desktop/images # 出力先を指定
    python3 generate_manga.py --list                    # シーン一覧を表示
"""

import argparse
import json
import sys
import time
from pathlib import Path

# 同じフォルダの google_image_client を読み込む
sys.path.insert(0, str(Path(__file__).parent))
from google_image_client import GoogleImageClient


# ============================================================
#  Harumi スタイル定義（ジブリ風温かいアニメ調）
# ============================================================

HARUMI_STYLE = """IMPORTANT: Generate this image in LANDSCAPE 16:9 widescreen aspect ratio
(e.g. 1792x1024 or similar wide format). NOT square.
The width must be significantly larger than the height.

Art style: Soft, warm Japanese anime illustration style inspired by Studio Ghibli.
Clean linework, soft coloring, pastel palette, warm golden lighting.
No text, no speech bubbles, no writing in the image.
No watermarks, no signatures, no UI elements."""


# ============================================================
#  デフォルトのサンプルシーン定義
# ============================================================

DEFAULT_SCENES = [
    {
        "id": "A-1",
        "filename": "scene1_narrator_intro.png",
        "title": "ナレーター導入（質問）",
        "prompt": f"""{HARUMI_STYLE}

Scene: A thoughtful young Japanese woman in her late 20s sitting at a cozy desk
in a warmly lit room. She is looking at her laptop screen with a curious expression.
The room has bookshelves, warm lamplight, and a window showing twilight sky.
Camera angle: slightly above, capturing both the woman and the warm atmosphere.
Gentle, inviting mood that draws the viewer in.""",
    },
    {
        "id": "A-2",
        "filename": "scene2_problem_presentation.png",
        "title": "問題提示",
        "prompt": f"""{HARUMI_STYLE}

Scene: A worried-looking middle-aged Japanese man (around 55 years old, graying hair)
sitting alone at a kitchen table. Documents and bills are spread on the table.
He is resting his chin on his hand with a troubled expression.
The kitchen has a window showing a rainy day outside.
Muted, slightly melancholic atmosphere with soft shadows.
Camera angle: medium shot from slightly below eye level.""",
    },
    {
        "id": "B-1",
        "filename": "scene3_solution_reveal.png",
        "title": "解決策の提示",
        "prompt": f"""{HARUMI_STYLE}

Scene: Split composition — left side shows the same worried man from before
(dark, muted colors), right side shows him smiling and relaxed in a bright garden
(warm, vibrant colors). A subtle golden light separates the two halves.
The contrast between worry and relief should be clearly visible.
Camera angle: wide shot showing both halves equally.""",
    },
    {
        "id": "B-2",
        "filename": "scene4_happy_ending.png",
        "title": "ハッピーエンド",
        "prompt": f"""{HARUMI_STYLE}

Scene: A happy elderly Japanese couple (both around 65-70 years old) walking together
in a beautiful Japanese garden during autumn. Golden sunlight streams through
red and orange maple leaves. They are smiling warmly at each other.
Cherry blossom petals and maple leaves float gently in the air.
Warm, nostalgic, heartwarming atmosphere.
Camera angle: medium-wide shot from slightly behind, showing the garden path ahead.""",
    },
]


# ============================================================
#  シーンデータの読み込み
# ============================================================

def load_scenes(scene_data_path: Path) -> list:
    """
    scene_data.json からシーンデータを読み込む
    ファイルが存在しない場合はデフォルトシーンを使用する

    Args:
        scene_data_path: scene_data.json のパス

    Returns:
        list: シーン定義のリスト
    """
    if scene_data_path.exists():
        try:
            with open(scene_data_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            scenes = []
            for scene in data.get("scenes", data if isinstance(data, list) else []):
                # JSONのシーンにHARUMIスタイルを付与
                prompt = scene.get("prompt", "")
                if "LANDSCAPE 16:9" not in prompt:
                    prompt = f"{HARUMI_STYLE}\n\n{prompt}"

                scenes.append({
                    "id": scene.get("id", f"scene_{len(scenes)+1}"),
                    "filename": scene.get("filename", f"scene{len(scenes)+1}.png"),
                    "title": scene.get("title", f"シーン {len(scenes)+1}"),
                    "prompt": prompt,
                })

            print(f"[OK] シーンデータ読み込み: {scene_data_path} ({len(scenes)}シーン)")
            return scenes

        except json.JSONDecodeError as e:
            print(f"[WARNING] scene_data.json の解析に失敗: {e}")
            print("         デフォルトシーンを使用します")

    print(f"[INFO] scene_data.json なし → デフォルトシーン ({len(DEFAULT_SCENES)}シーン) を使用")
    return DEFAULT_SCENES


# ============================================================
#  メイン処理
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="漫画イラスト一括生成ツール（Mac版）— Google AI専用",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  python3 generate_manga.py                          全シーンを生成
  python3 generate_manga.py --scene A-1 A-2          特定シーンのみ生成
  python3 generate_manga.py --output ~/Desktop/out   出力先を指定
  python3 generate_manga.py --list                   シーン一覧を表示
  python3 generate_manga.py --scenes scene_data.json カスタムシーンファイルを使用
        """,
    )
    parser.add_argument(
        "--scene",
        nargs="+",
        help="生成するシーンのIDを指定（例: A-1 A-2 B-1）",
    )
    parser.add_argument(
        "--output",
        type=str,
        help="画像の出力先ディレクトリ（デフォルト: ../03_Remotion/public/images/）",
    )
    parser.add_argument(
        "--scenes",
        type=str,
        default="scene_data.json",
        help="シーン定義JSONファイルのパス（デフォルト: scene_data.json）",
    )
    parser.add_argument(
        "--retry",
        type=int,
        default=3,
        help="各モデルでのリトライ回数（デフォルト: 3）",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=10.0,
        help="リトライ間の待機秒数（デフォルト: 10.0）",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="シーン一覧を表示して終了",
    )
    parser.add_argument(
        "--model",
        type=str,
        choices=["nano-banana-2", "nano-banana-pro"],
        help="使用モデルを指定（デフォルト: Nano Banana 2 優先）",
    )

    args = parser.parse_args()

    # ヘッダー表示
    print()
    print("=" * 60)
    print("  🎨 漫画イラスト一括生成ツール（Mac版）")
    print("  Google API 専用 — Nano Banana 2 / Pro")
    print("=" * 60)
    print()

    # シーンデータ読み込み
    script_dir = Path(__file__).parent
    scene_data_path = Path(args.scenes) if Path(args.scenes).is_absolute() else script_dir / args.scenes
    scenes = load_scenes(scene_data_path)

    if not scenes:
        print("[NG] 生成するシーンがありません。")
        sys.exit(1)

    # シーン一覧表示モード
    if args.list:
        print()
        print(f"{'ID':<8} {'ファイル名':<35} {'タイトル'}")
        print("-" * 70)
        for scene in scenes:
            print(f"{scene['id']:<8} {scene['filename']:<35} {scene['title']}")
        print()
        print(f"合計: {len(scenes)} シーン")
        sys.exit(0)

    # シーンのフィルタリング
    if args.scene:
        target_ids = set(args.scene)
        filtered = [s for s in scenes if s["id"] in target_ids]
        not_found = target_ids - {s["id"] for s in filtered}
        if not_found:
            print(f"[WARNING] 見つからないシーンID: {', '.join(not_found)}")
        scenes = filtered
        if not scenes:
            print("[NG] 指定されたシーンが見つかりません。--list で一覧を確認してください。")
            sys.exit(1)

    # 出力先の決定
    if args.output:
        output_dir = Path(args.output).expanduser()
    else:
        output_dir = script_dir.parent / "03_Remotion" / "public" / "images"
    output_dir.mkdir(parents=True, exist_ok=True)
    print(f"[OK] 出力先: {output_dir}")

    # モデル指定
    preferred_model = None
    if args.model == "nano-banana-2":
        preferred_model = "gemini-3.1-flash-image-preview"
    elif args.model == "nano-banana-pro":
        preferred_model = "gemini-3-pro-image-preview"

    # クライアント初期化
    print()
    client = GoogleImageClient()
    print()

    # 画像生成ループ
    total = len(scenes)
    success_count = 0
    fail_count = 0
    start_time = time.time()

    for i, scene in enumerate(scenes, 1):
        print()
        print("=" * 60)
        print(f"  [{i}/{total}] {scene['title']}")
        print("=" * 60)

        output_path = output_dir / scene["filename"]

        success = client.generate_image(
            prompt=scene["prompt"],
            output_path=output_path,
            retry=args.retry,
            retry_delay=args.delay,
            preferred_model=preferred_model,
        )

        if success:
            client.verify_aspect_ratio(output_path)
            success_count += 1
        else:
            fail_count += 1

        # レート制限対策: シーン間に少し間隔を空ける
        if i < total:
            time.sleep(2.0)

    # 結果サマリー
    elapsed = time.time() - start_time
    print()
    print("=" * 60)
    print("  生成完了サマリー")
    print("=" * 60)
    print(f"  合計:   {total} シーン")
    print(f"  成功:   {success_count} シーン")
    print(f"  失敗:   {fail_count} シーン")
    print(f"  所要時間: {elapsed:.1f} 秒")
    print(f"  出力先: {output_dir}")
    print()

    if fail_count > 0:
        print(f"  [WARNING] {fail_count} シーンの生成に失敗しました。")
        print("  失敗したシーンは --scene オプションで個別に再生成できます。")
        print()

    # Finderで出力フォルダを開く案内
    print(f"  💡 Finderで確認: open \"{output_dir}\"")
    print()

    sys.exit(0 if fail_count == 0 else 1)


if __name__ == "__main__":
    main()
