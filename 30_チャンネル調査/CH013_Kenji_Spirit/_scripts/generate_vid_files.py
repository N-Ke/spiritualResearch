#!/usr/bin/env python3
"""Generate description.md / comments.md / transcript.md / research.md skeleton
for VID006-VID010 from yt-dlp info.json + auto subtitles.

Run from CH013_Kenji_Spirit directory.
"""
from __future__ import annotations

import json
import re
import sys
from datetime import datetime
from pathlib import Path

CHANNEL_ROOT = Path(__file__).resolve().parent.parent
TODAY = datetime.now().strftime("%Y-%m-%d")

VIDEOS = [
    {
        "folder": "VID006_20220525_もうダメな時に使う想像以上",
        "video_num": "VID006",
        "thumb_id": "TH-CH013-VID006-01",
        "topic_memo": "もうダメな時の対処／想像以上",
    },
    {
        "folder": "VID007_20201126_12月22日までに絶対にするべき事",
        "video_num": "VID007",
        "thumb_id": "TH-CH013-VID007-01",
        "topic_memo": "年末までにするべき事／超重要",
    },
    {
        "folder": "VID008_20210102_祝福すごいスピード現実変わる人サイン",
        "video_num": "VID008",
        "thumb_id": "TH-CH013-VID008-01",
        "topic_memo": "現実が変わる人のサイン／祝福",
    },
    {
        "folder": "VID009_20210214_シンクロゾロ目頻繁に見る",
        "video_num": "VID009",
        "thumb_id": "TH-CH013-VID009-01",
        "topic_memo": "シンクロ／ゾロ目を頻繁に見る",
    },
    {
        "folder": "VID010_20210711_超解説潜在意識心の奥底知ってる",
        "video_num": "VID010",
        "thumb_id": "TH-CH013-VID010-01",
        "topic_memo": "潜在意識は心の奥底を知っている",
    },
]


def fmt_seconds(secs: int | float) -> str:
    s = int(secs)
    m, sec = divmod(s, 60)
    return f"約 {m} 分 {sec} 秒（{s} 秒）"


def fmt_upload_date(ymd: str) -> str:
    return f"{ymd[:4]}-{ymd[4:6]}-{ymd[6:8]}"


def parse_vtt_to_text(vtt_path: Path) -> str:
    """Strip cue numbers/timecodes/markup from a webvtt and dedupe rolling captions."""
    if not vtt_path.exists():
        return ""
    raw = vtt_path.read_text(encoding="utf-8", errors="replace")
    lines = raw.splitlines()
    out: list[str] = []
    seen: set[str] = set()
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.startswith("WEBVTT"):
            continue
        if line.startswith("Kind:") or line.startswith("Language:"):
            continue
        if "-->" in line:
            continue
        if re.fullmatch(r"\d+", line):
            continue
        clean = re.sub(r"<[^>]+>", "", line)
        clean = clean.strip()
        if not clean:
            continue
        if clean in seen:
            continue
        seen.add(clean)
        out.append(clean)
    return "\n".join(out)


def select_top_comments(comments: list[dict], n: int = 50) -> list[dict]:
    """Top comments by like count, top-level only."""
    top = [c for c in comments if c.get("parent") in (None, "root")]
    top.sort(key=lambda c: (c.get("like_count") or 0), reverse=True)
    return top[:n]


def write_description_md(folder: Path, info: dict) -> None:
    desc = info.get("description") or ""
    out = []
    out.append("# 概要欄（YouTube 説明文）\n")
    out.append(f"出典: `yt-dlp` 抽出（取得日: {TODAY}）\n")
    out.append("---\n")
    out.append(desc)
    out.append("")
    (folder / "description.md").write_text("\n".join(out), encoding="utf-8")


def write_comments_md(folder: Path, info: dict, video_id: str, title: str, topic_memo: str) -> None:
    comments = info.get("comments") or []
    top = select_top_comments(comments, 50)
    out: list[str] = []
    out.append("# コメント欄（YouTube）\n")
    out.append(f"- **動画ID**: `{video_id}`")
    out.append(f"- **公開タイトル（索引）**: {title}")
    out.append(f"- **取得方法**: `yt-dlp --write-info-json --write-comments`（取得日: {TODAY}）")
    out.append(f"- **取得件数（上位）**: {len(top)} 件（top-level、いいね数順）")
    out.append(f"- **本編の論点メモ**: {topic_memo}")
    out.append("")
    out.append("---\n")
    out.append("## 1. コメント欄の原文一覧\n")
    out.append("以下は **いいね数が多い順**（同率時は取得データの順）。**本文のみ**を列挙（投稿者名・いいね数は第 2 節のセットに記載）。\n")
    for i, c in enumerate(top, 1):
        body = (c.get("text") or "").rstrip()
        out.append(f"{i}. {body}\n")
    out.append("---\n")
    out.append("## 2. 投稿者名・いいね数（対応セット）\n")
    out.append("| # | 投稿者 | いいね | 返信数 |")
    out.append("|---|---|---:|---:|")
    for i, c in enumerate(top, 1):
        author = (c.get("author") or "").replace("|", "/")
        likes = c.get("like_count") or 0
        replies = c.get("reply_count") or 0
        out.append(f"| {i} | {author} | {likes} | {replies} |")
    out.append("")
    (folder / "comments.md").write_text("\n".join(out), encoding="utf-8")


def write_transcript_md(folder: Path, info: dict, video_id: str, title: str, vtt_text: str) -> None:
    title_short = title
    out = []
    out.append("# 文字起こし（本編）\n")
    out.append(f"- **動画**: [{video_id}](https://www.youtube.com/watch?v={video_id}) — {title_short}")
    out.append(f"- **取得**: 自動字幕（`yt-dlp --write-auto-sub --sub-lang ja`、取得日: {TODAY}）。**手入力フル文字起こしは未実施**。")
    out.append(f"- **補助**: [[assets/sub.ja.vtt]]")
    out.append("")
    out.append("> ⚠️ **品質注意**: 自動字幕由来のため、句読点・改行・誤認識を含む。重要動画として深掘りする場合は、ユーザー側で `transcript.md` を上書き（手入力フル）してください。")
    out.append("")
    out.append("---\n")
    out.append("## 自動字幕の整形テキスト（重複行除去のみ）\n")
    out.append(vtt_text or "_自動字幕が取得できなかった可能性があります。_")
    out.append("")
    (folder / "transcript.md").write_text("\n".join(out), encoding="utf-8")


def write_research_md(folder: Path, info: dict, v: dict, video_id: str, title: str) -> None:
    upload = info.get("upload_date") or ""
    duration = info.get("duration") or 0
    view = info.get("view_count") or 0
    out: list[str] = []
    out.append(f"# 動画1本リサーチ — CH013-{v['video_num']}\n")
    out.append("> 🚧 **未着手スケルトン**: 自動取得データのみで作成。深掘り（§4 以降）は手作業推奨。\n")
    out.append("## 1. 人が入力するところ\n")
    out.append("### 管理ID\n")
    out.append("- channel_id: `CH013`")
    out.append(f"- video_id: `CH013-{v['video_num']}`")
    out.append(f"- thumbnail_id: `{v['thumb_id']}`")
    out.append(f"- thumbnail_file: `./assets/{v['thumb_id']}.jpg`（`i.ytimg.com` maxresdefault 取得）")
    out.append("")
    out.append("### 基本情報\n")
    out.append("- チャンネル名: Kenji Spirit（@kenjispirit11）")
    out.append(f"- 動画名: {title}")
    out.append(f"- 動画URL: [https://www.youtube.com/watch?v={video_id}](https://www.youtube.com/watch?v={video_id})")
    out.append("- 属人 / 準属人 / 非属人: **属人**（顔出し・「ケンジ」・ホワイトボード）")
    out.append(f"- 再生数: 約 {view:,} 回（取得時点 `yt-dlp`・都度変動）")
    out.append(f"- 投稿日: {fmt_upload_date(upload) if upload else '_未取得_'}（メタデータ `upload_date`）")
    out.append(f"- 尺: {fmt_seconds(duration)}")
    out.append("- 主テーマ: _要記入（自動字幕を読んで要約）_")
    out.append("- 収益導線の有無: _要確認（description.md より）_")
    out.append("")
    out.append("### 人の第一印象\n")
    out.append("- ユーザー記入欄: （任意）\n")
    out.append("---\n")
    out.append("## 2. 台本 / 素材\n")
    out.append("### サムネ素材\n")
    out.append(f"- thumbnail_id: `{v['thumb_id']}`")
    out.append(f"- thumbnail_file: `./assets/{v['thumb_id']}.jpg`")
    out.append(f"- サムネリンク: `https://www.youtube.com/watch?v={video_id}`\n")
    out.append("### 台本 or 文字起こし\n")
    out.append("- **全文**: [[transcript.md]]")
    out.append(f"- transcript_status: **自動字幕のみ**（{TODAY}）。手入力フルは未実施。\n")
    out.append("### 概要欄（YouTube 説明文）\n")
    out.append("- **全文**: [[description.md]]")
    out.append(f"- description_status: `yt-dlp` 経由抽出（取得日: {TODAY}）\n")
    out.append("### コメント欄（YouTube）\n")
    out.append(f"- **原文一覧・分析セット**: [[comments.md]]（`yt-dlp --write-comments`・取得日: {TODAY}）\n")
    out.append("---\n")
    out.append("## 3. 概要欄分析（`description.md` ベース）\n")
    out.append("| 観点 | メモ |\n|---|---|\n| 文字量・構造 | _要記入_ |\n| 動画との役割分担 | _要記入_ |\n| CTA | _要記入_ |\n| キーワード | _要記入_ |\n")
    out.append("---\n")
    out.append("## 4. クリックの約束（タイトル・構成）\n")
    out.append("- _要記入：タイトル要素分解、サムネ要素、構成。_\n")
    out.append("---\n")
    out.append("## 5. 本編の骨子（文字起こしベース）\n")
    out.append("- _要記入：本編の主要ポイントをリスト化。_\n")
    out.append("---\n")
    out.append("## 6. 信頼・差別化\n")
    out.append("- _要記入_\n")
    out.append("---\n")
    out.append("## 7. 収益・コンプラ観測メモ（分析用・非法律判断）\n")
    out.append("- _要記入_\n")
    out.append("---\n")
    out.append("## 8. 属人置換と自チャンネル示唆\n")
    out.append("| 区分 | 内容 |\n|---|---|\n| **そのまま使う** | _要記入_ |\n| **変えて使う** | _要記入_ |\n| **捨てる** | _要記入_ |\n")
    out.append("---\n")
    out.append("## 9. 横断メモ（G001 転記用）\n")
    out.append("- _要記入_\n")
    out.append("---\n")
    out.append("## 10. 付記\n")
    out.append(f"- 自動字幕のみ取得。`{v['video_num']}` は **再生数上位**として補完取得（{TODAY}）。深掘りは別タスク。\n")
    (folder / "research.md").write_text("\n".join(out), encoding="utf-8")


def main() -> int:
    for v in VIDEOS:
        folder = CHANNEL_ROOT / v["folder"]
        info_path = folder / "assets" / "sub.info.json"
        if not info_path.exists():
            print(f"SKIP {v['folder']}: no info.json", file=sys.stderr)
            continue
        info = json.loads(info_path.read_text(encoding="utf-8"))
        video_id = info.get("id") or ""
        title = info.get("title") or ""
        vtt_path = folder / "assets" / "sub.ja.vtt"
        vtt_text = parse_vtt_to_text(vtt_path)
        write_description_md(folder, info)
        write_comments_md(folder, info, video_id, title, v["topic_memo"])
        write_transcript_md(folder, info, video_id, title, vtt_text)
        write_research_md(folder, info, v, video_id, title)
        print(f"OK {v['folder']}: comments={len(info.get('comments') or [])}, transcript_lines={len(vtt_text.splitlines())}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
