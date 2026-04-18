# -*- coding: utf-8 -*-
"""Kenji Spirit 各動画フォルダ用 comments.md を JSON（yt-dlp --write-comments）から生成する。"""
from __future__ import annotations

import json
import re
from pathlib import Path

TEMP = Path(r"C:\Users\somed\AppData\Local\Temp")

VIDEOS: list[dict] = [
    {
        "id": "QGiTQMpLcuM",
        "folder": "VID001_20260329_人生は逆ハードモード卒業",
        "title": "【人生は逆】努力をやめた途端…ハードモード卒業",
        "theme": "嫌な気分→現実／感じていること／努力やめ・イージーモード",
    },
    {
        "id": "b5d5EhNK_O8",
        "folder": "VID002_20251223_実証済み1年で人生根こそぎ変える",
        "title": "【実証済み】1年で人生を根こそぎ変える／気分コミット・心地よさ",
        "theme": "気分100%コミット／心地よさ3選／努力からの転換",
    },
    {
        "id": "HYavz89bIf4",
        "folder": "VID003_20210217_鳥肌コレやめるだけ現実が変わる",
        "title": "鳥肌／やめるだけで現実が変わる／感謝こじらせ",
        "theme": "感謝をdoingで頑張る誤解／したほうがいいですか／状態とエネルギー",
    },
    {
        "id": "8GRc3WE1N-E",
        "folder": "VID004_20200908_緊急配信変化の兆し3パターン",
        "title": "緊急配信／変化の兆し3パターン／二極化",
        "theme": "妙な安心感・感情低下・興味変化／地球エネルギー・ゼロポイント",
    },
    {
        "id": "DKVU-VaTuFg",
        "folder": "VID005_20201217_別人レベル波動アップ",
        "title": "心地よさを簡単に／別人レベル波動／できない事はやらない",
        "theme": "波動=元気／夢ノート等への質問／自分への許可",
    },
]

BASE = Path(
    r"g:\その他のパソコン\マイ コンピュータ\Obsidian\思考の地図\authoring\notes"
    r"\02.Youtube\01_スピリチュアル系\30_チャンネル調査\CH013_Kenji_Spirit"
)


def reaction_type(text: str) -> str:
    t = text.strip()
    if not t or len(t) <= 1:
        return "極短文・スタンプ的"
    if re.search(r"https?://|t\.me/|line\.me", t, re.I):
        return "リンク・宣伝・外部誘因在"
    if re.search(r"[?？]", t) and len(t) < 200:
        return "質問・確認"
    if any(
        x in t
        for x in (
            "ありがとう",
            "感謝",
            "おかげ",
            "素敵",
            "最高",
            "すごい",
            "勉強になり",
        )
    ):
        return "感謝・称賛"
    if any(x in t for x in ("共感", "わかる", "わかります", "その通り", "同感")):
        return "共感"
    if any(
        x in t
        for x in (
            "私も",
            "自分も",
            "経験",
            "昔",
            "今まで",
            "実は",
            "結果",
            "やってみ",
        )
    ):
        return "体験談・自己開示"
    if any(x in t for x in ("嘘", "怪しい", "違う", "間違い", "批判", "注意")):
        return "懐疑・反論・注意喚起"
    if any(x in t for x in ("ケンジ", "Kenji", "応援", "頑張って", "チャンネル")):
        return "ホストへの反応・応援"
    return "感想・その他"


def analyze_block(text: str, theme: str) -> str:
    """ルールベースの短い分析（調査ノート用）。"""
    rt = reaction_type(text)
    one = text.replace("\n", " ").strip()
    if len(one) > 120:
        one = one[:117] + "…"

    parts = [f"**反応タイプ**: {rt}。"]

    if rt == "リンク・宣伝・外部誘因在":
        parts.append("調査上は **スパム／ノイズ** 寄り。本編論点との接続は薄いことが多い。")
    elif rt == "質問・確認":
        parts.append(
            f"本編テーマ（{theme}）に対し、**実践や解釈の補助線** を求めている様子。"
        )
    elif rt in ("共感", "感謝・称賛", "ホストへの反応・応援"):
        parts.append("**エンゲージメント** が高く、チャンネル世界観への **馴化・支持** を示すコメント群に典型的。")
    elif rt == "体験談・自己開示":
        parts.append(
            f"視聴者が **自伝データ** を足しており、語りの「再現可能性」の外部証言として扱える。"
        )
    elif rt == "懐疑・反論・注意喚起":
        parts.append(
            "**バイアス注意** として残す価値あり。スピ系動画で起きうる温度差のサンプル。"
        )
    elif rt == "感想・その他":
        parts.append(
            f"テーマ「{theme}」に対する **断片的フィードバック**。情緒・印象の補助線として参照。"
        )
    else:
        parts.append("短文のためタイプ推定のみ。文脈は前後コメントと併読が有効。")

    return "".join(parts)


def sort_comments(comments: list[dict]) -> list[dict]:
    def key(c: dict):
        pinned = 0 if c.get("is_pinned") else 1
        likes = c.get("like_count") or 0
        return (pinned, -likes)

    return sorted(comments, key=key)


def build_md(meta: dict, comments: list[dict]) -> str:
    lines: list[str] = []
    lines.append("# コメント欄（YouTube）")
    lines.append("")
    lines.append(f"- **動画ID**: `{meta['id']}`")
    lines.append(f"- **公開タイトル（索引）**: {meta['title']}")
    lines.append(f"- **取得方法**: `yt-dlp --dump-json --write-comments`（取得日: 2026-04-17）")
    lines.append(f"- **本編の論点メモ**: {meta['theme']}")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 1. コメント欄の原文一覧")
    lines.append("")
    lines.append(
        "以下は **いいね数が多い順**（同率時は取得データの順）。"
        "**本文のみ**を列挙（投稿者名・いいね数は第2節のセットに記載）。"
    )
    lines.append("")

    sorted_cs = sort_comments(comments)
    for i, c in enumerate(sorted_cs, 1):
        body = (c.get("text") or "").strip()
        # 空はスキップしないで番号を飛ばさない: 空なら（本文なし）
        if not body:
            body = "（本文なし）"
        lines.append(f"{i}. {body}")
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("## 2. 原文と分析結果のセット")
    lines.append("")
    lines.append(
        "並び順は **第1節と同じ**（いいね数の多い順）。"
        "（原文／分析）が一目で分かるよう **【原文】** と **【分析】** で表記。"
    )
    lines.append("")

    for i, c in enumerate(sorted_cs, 1):
        body = (c.get("text") or "").strip()
        if not body:
            body = "（本文なし）"
        author = (c.get("author") or "（不明）").strip()
        likes = c.get("like_count")
        pinned = "はい" if c.get("is_pinned") else "いいえ"
        lines.append(f"### No.{i}")
        lines.append("")
        lines.append("| 項目 | 内容 |")
        lines.append("|---|---|")
        lines.append(f"| 投稿者（表示名） | {author} |")
        lines.append(f"| いいね数 | {likes} |")
        lines.append(f"| ピン留め | {pinned} |")
        lines.append("")
        lines.append("**【原文】**")
        lines.append("")
        lines.append("```")
        lines.append(body)
        lines.append("```")
        lines.append("")
        lines.append("**【分析】**")
        lines.append("")
        lines.append(analyze_block(c.get("text") or "", meta["theme"]))
        lines.append("")
        lines.append("---")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    for meta in VIDEOS:
        path = TEMP / f"kenji_{meta['id']}.json"
        if not path.exists():
            raise SystemExit(f"missing: {path}")
        with path.open(encoding="utf-8-sig") as f:
            data = json.load(f)
        comments = data.get("comments") or []
        md = build_md(meta, comments)
        out = BASE / meta["folder"] / "comments.md"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(md, encoding="utf-8")
        print("wrote", out, "comments", len(comments))


if __name__ == "__main__":
    main()
