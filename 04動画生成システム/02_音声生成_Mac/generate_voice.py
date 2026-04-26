#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
音声一括生成スクリプト（Mac版）

台本のセリフ定義に基づいて、ElevenLabs APIで音声を一括生成する。
voice_data.json からセリフ情報を読み込み、キャラクター別の音声を生成。

使い方:
    python3 generate_voice.py                              # 全セリフを生成
    python3 generate_voice.py --scene S1-01 S1-02          # 特定セリフのみ
    python3 generate_voice.py --output ~/Desktop/audio     # 出力先を指定
    python3 generate_voice.py --list                       # セリフ一覧を表示
    python3 generate_voice.py --timestamps                 # タイムスタンプJSONも出力
"""

import argparse
import json
import sys
import time
from pathlib import Path

# 同じフォルダの elevenlabs_client を読み込む
sys.path.insert(0, str(Path(__file__).parent))
from elevenlabs_client import ElevenLabsClient


# ============================================================
#  デフォルトのサンプルセリフ定義
# ============================================================

DEFAULT_LINES = [
    {
        "id": "S1-NAR-01",
        "filename": "s1_nar_01_hook.mp3",
        "character": "ナレーター",
        "voice_id": "XkfxZatpPaUTadDUJKRH",
        "preset": "narration",
        "title": "冒頭フック（ナレーション）",
        "text": "これ、面白い話があるんだけど。今から話す男は、アドセンスだけで月50万円を稼いでいた。でも、ある日突然それがほぼゼロになった。今、彼は笑っている。アドセンスだけじゃない、3つの収益の柱を持って。",
    },
    {
        "id": "S1-NAR-02",
        "filename": "s1_nar_02_intro.mp3",
        "character": "ナレーター",
        "voice_id": "XkfxZatpPaUTadDUJKRH",
        "preset": "narration",
        "title": "自己紹介（ナレーション）",
        "text": "僕はね、12年YouTubeをやってきて、こういう人を何人も見てきた。今日は彼の話をしたいんです。",
    },
]


# ============================================================
#  セリフデータの読み込み
# ============================================================

def load_lines(voice_data_path: Path) -> list:
    """
    voice_data.json からセリフデータを読み込む

    Args:
        voice_data_path: voice_data.json のパス

    Returns:
        list: セリフ定義のリスト
    """
    if voice_data_path.exists():
        try:
            with open(voice_data_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            lines = data.get("lines", data if isinstance(data, list) else [])
            print(f"[OK] セリフデータ読み込み: {voice_data_path} ({len(lines)}件)")
            return lines

        except json.JSONDecodeError as e:
            print(f"[WARNING] voice_data.json の解析に失敗: {e}")
            print("         デフォルトセリフを使用します")

    print(f"[INFO] voice_data.json なし → デフォルトセリフ ({len(DEFAULT_LINES)}件) を使用")
    return DEFAULT_LINES


# ============================================================
#  メイン処理
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="音声一括生成ツール（Mac版）— ElevenLabs API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  python3 generate_voice.py                              全セリフを生成
  python3 generate_voice.py --scene S1-NAR-01            特定セリフのみ生成
  python3 generate_voice.py --output ~/Desktop/audio     出力先を指定
  python3 generate_voice.py --list                       セリフ一覧を表示
  python3 generate_voice.py --data voice_data.json       カスタムデータファイル
  python3 generate_voice.py --timestamps                 タイムスタンプJSONも出力
        """,
    )
    parser.add_argument(
        "--scene",
        nargs="+",
        help="生成するセリフのIDを指定（例: S1-NAR-01 S1-NAR-02）",
    )
    parser.add_argument(
        "--output",
        type=str,
        help="音声の出力先ディレクトリ（デフォルト: ./output/）",
    )
    parser.add_argument(
        "--data",
        type=str,
        default="voice_data.json",
        help="セリフ定義JSONファイルのパス（デフォルト: voice_data.json）",
    )
    parser.add_argument(
        "--retry",
        type=int,
        default=3,
        help="リトライ回数（デフォルト: 3）",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=5.0,
        help="リトライ間の待機秒数（デフォルト: 5.0）",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="セリフ一覧を表示して終了",
    )
    parser.add_argument(
        "--timestamps",
        action="store_true",
        help="タイムスタンプJSONも出力する",
    )

    args = parser.parse_args()

    # ヘッダー表示
    print()
    print("=" * 60)
    print("  🎙️ 音声一括生成ツール（Mac版）")
    print("  ElevenLabs API — eleven_v3 + with-timestamps")
    print("=" * 60)
    print()

    # セリフデータ読み込み
    script_dir = Path(__file__).parent
    data_path = Path(args.data) if Path(args.data).is_absolute() else script_dir / args.data
    lines = load_lines(data_path)

    if not lines:
        print("[NG] 生成するセリフがありません。")
        sys.exit(1)

    # セリフ一覧表示モード
    if args.list:
        print()
        print(f"{'ID':<14} {'キャラクター':<12} {'タイトル'}")
        print("-" * 70)
        for line in lines:
            print(f"{line['id']:<14} {line.get('character', '?'):<12} {line['title']}")
        print()
        print(f"合計: {len(lines)} 件")
        sys.exit(0)

    # セリフのフィルタリング
    if args.scene:
        target_ids = set(args.scene)
        filtered = [l for l in lines if l["id"] in target_ids]
        not_found = target_ids - {l["id"] for l in filtered}
        if not_found:
            print(f"[WARNING] 見つからないID: {', '.join(not_found)}")
        lines = filtered
        if not lines:
            print("[NG] 指定されたセリフが見つかりません。--list で一覧を確認してください。")
            sys.exit(1)

    # 出力先の決定
    if args.output:
        output_dir = Path(args.output).expanduser()
    else:
        output_dir = script_dir / "output"
    output_dir.mkdir(parents=True, exist_ok=True)
    print(f"[OK] 出力先: {output_dir}")

    # クライアント初期化
    print()
    client = ElevenLabsClient()
    print()

    # 音声生成ループ
    total = len(lines)
    success_count = 0
    fail_count = 0
    all_results = []
    start_time = time.time()

    for i, line in enumerate(lines, 1):
        print()
        print("=" * 60)
        print(f"  [{i}/{total}] {line.get('character', '?')} — {line['title']}")
        print("=" * 60)

        output_path = output_dir / line["filename"]

        # custom_settings があればそれを使う
        custom_settings = line.get("voice_settings", None)
        preset = line.get("preset", "narration")

        result = client.generate_speech(
            text=line["text"],
            voice_id=line["voice_id"],
            output_path=output_path,
            preset=preset,
            custom_settings=custom_settings,
            retry=args.retry,
            retry_delay=args.delay,
        )

        if result["success"]:
            success_count += 1
            all_results.append({
                "id": line["id"],
                "character": line.get("character", "?"),
                "title": line["title"],
                "output_path": result["output_path"],
                "duration_seconds": result["duration_seconds"],
                "alignment": result["alignment"] if args.timestamps else None,
            })

            # テロップ分割も表示
            if args.timestamps and result["alignment"]:
                segments = client.get_telop_segments(result["alignment"])
                print(f"    [OK] テロップ分割: {len(segments)} セグメント")
                for seg in segments:
                    print(f"         [{seg['start_frame']:>5} - {seg['end_frame']:>5}] {seg['text'][:40]}")
        else:
            fail_count += 1

        # レート制限対策: セリフ間に間隔を空ける
        if i < total:
            time.sleep(1.5)

    # タイムスタンプJSON出力
    if args.timestamps and all_results:
        ts_path = output_dir / "timestamps.json"
        with open(ts_path, "w", encoding="utf-8") as f:
            json.dump(all_results, f, ensure_ascii=False, indent=2)
        print(f"\n[OK] タイムスタンプJSON: {ts_path}")

    # 結果サマリー
    elapsed = time.time() - start_time
    print()
    print("=" * 60)
    print("  生成完了サマリー")
    print("=" * 60)
    print(f"  合計:     {total} セリフ")
    print(f"  成功:     {success_count} セリフ")
    print(f"  失敗:     {fail_count} セリフ")
    print(f"  所要時間: {elapsed:.1f} 秒")
    print(f"  出力先:   {output_dir}")
    print()

    if fail_count > 0:
        print(f"  [WARNING] {fail_count} セリフの生成に失敗しました。")
        print("  失敗したセリフは --scene オプションで個別に再生成できます。")
        print()

    # Finderで出力フォルダを開く案内
    print(f'  💡 Finderで確認: open "{output_dir}"')
    print()

    sys.exit(0 if fail_count == 0 else 1)


if __name__ == "__main__":
    main()
