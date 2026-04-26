import json
import os
import glob

FPS = 30

def format_japanese_text(text):
    """Windows版 SimpleVideo.tsx 準拠: 最大2行、句読点で1箇所だけ分割"""
    if len(text) <= 15:
        return text

    punctuation = ['\u3001', '\u3002', '\uff01', '\uff1f']
    mid = len(text) // 2
    best_pos = -1
    best_dist = len(text)

    for i, ch in enumerate(text):
        if ch in punctuation:
            pos = i + 1
            dist = abs(pos - mid)
            if dist < best_dist:
                best_dist = dist
                best_pos = pos

    if best_pos > 0:
        return text[:best_pos] + "\n" + text[best_pos:]

    return text[:mid] + "\n" + text[mid:]

import re

def highlight_keywords(text):
    """重要キーワードを {keyword} でマーキング（TelopSegmentViewで色変え）"""
    # 数字+単位 (月50万円, 3つ, 12年 など)
    text = re.sub(r'(\d+[\u4e07\u5104\u5343\u767e]?\u5186)', r'{\1}', text)  # ○万円
    text = re.sub(r'(\d+\u3064)', r'{\1}', text)                              # ○つ
    text = re.sub(r'(\d+\u5e74)', r'{\1}', text)                              # ○年
    text = re.sub(r'(\d+%)', r'{\1}', text)                                   # ○%
    
    # 重要ワード
    important = [
        '\u30bc\u30ed',      # ゼロ
        '\u7a81\u7136',      # 突然
        '\u7b11\u3063\u3066', # 笑って
        '\u53ce\u76ca\u306e\u67f1', # 収益の柱
    ]
    for word in important:
        text = text.replace(word, '{' + word + '}')
    
    # 二重マーキング防止 {{word}} → {word}
    text = re.sub(r'\{\{([^}]+)\}\}', r'{\1}', text)
    
    return text


def generate_layout():
    with open("public/audio/timestamps.json", "r", encoding="utf-8") as f:
        ts_data = json.load(f)[0]

    chars = ts_data['alignment']['characters']
    starts = ts_data['alignment']['start_times']
    ends = ts_data['alignment']['end_times']

    sentences = []
    current_boundary = 0.0
    current_sentence_chars = []
    current_sentence_starts = []
    current_sentence_ends = []

    for i, char in enumerate(chars):
        current_sentence_chars.append(char)
        current_sentence_starts.append(starts[i])
        current_sentence_ends.append(ends[i])

        if char == '\u3002':
            end_time = ends[i]

            in_tag = False
            actual_speech_start = None
            for j, c in enumerate(current_sentence_chars):
                if c == "[":
                    in_tag = True
                elif c == "]":
                    in_tag = False
                elif not in_tag and c.strip():
                    actual_speech_start = current_sentence_starts[j]
                    break

            if actual_speech_start is None:
                actual_speech_start = current_sentence_starts[0]

            sentences.append({
                "text": "".join(current_sentence_chars).strip(),
                "panelStartSec": current_boundary,
                "speechStartSec": actual_speech_start,
                "endSec": end_time
            })
            current_boundary = end_time

            current_sentence_chars = []
            current_sentence_starts = []
            current_sentence_ends = []

    images = sorted([os.path.basename(p) for p in glob.glob("public/images/*.png")])
    if len(images) != 6:
        print("Warning: Expected 6 images, found", len(images))

    mapping = [
        [0],
        [1],
        [2],
        [3, 4],
        [5],
        [6]
    ]

    panels = []

    for idx, (img, sent_indices) in enumerate(zip(images, mapping)):
        panel_start_sec = sentences[sent_indices[0]]["panelStartSec"]
        panel_end_sec = sentences[sent_indices[-1]]["endSec"]

        panel_start_frame = int(panel_start_sec * FPS)
        panel_duration_frames = int((panel_end_sec - panel_start_sec) * FPS)

        telop_segments = []
        for s_idx in sent_indices:
            sent = sentences[s_idx]
            seg_start_relative = int((sent["speechStartSec"] - panel_start_sec) * FPS)
            seg_duration = int((sent["endSec"] - sent["speechStartSec"]) * FPS)

            # Remove audio tags, then format
            clean = sent["text"]
            for tag in ["[quietly]", "[pauses]", "[happily]"]:
                clean = clean.replace(tag, "")
            clean = clean.strip()
            formatted = format_japanese_text(clean)
            formatted = highlight_keywords(formatted)

            telop_segments.append({
                "text": formatted,
                "startFrame": seg_start_relative,
                "durationFrames": seg_duration
            })

        kens = [
            {"scaleStart": 1.0, "scaleEnd": 1.05, "xStart": 0, "xEnd": 0, "yStart": 0, "yEnd": 0},
            {"scaleStart": 1.05, "scaleEnd": 1.05, "xStart": -2, "xEnd": 2, "yStart": 0, "yEnd": 0},
            {"scaleStart": 1.0, "scaleEnd": 1.06, "xStart": 0, "xEnd": 0, "yStart": 0, "yEnd": 0},
            {"scaleStart": 1.05, "scaleEnd": 1.0, "xStart": 0, "xEnd": 0, "yStart": 0, "yEnd": 0},
            {"scaleStart": 1.0, "scaleEnd": 1.05, "xStart": 0, "xEnd": 0, "yStart": 0, "yEnd": 0},
            {"scaleStart": 1.0, "scaleEnd": 1.03, "xStart": 0, "xEnd": 0, "yStart": 0, "yEnd": 0},
        ]

        panels.append({
            "id": f"P{idx+1}",
            "title": f"Scene {idx+1}",
            "image": img,
            "startFrame": panel_start_frame,
            "durationFrames": panel_duration_frames,
            "kenBurns": kens[idx % len(kens)],
            "telopSegments": telop_segments,
            "audio": "s1_nar_01_hook_with_tags.mp3" if idx == 0 else ""
        })

    layout = {
        "title": "AdSense Dependency",
        "fps": FPS,
        "width": 1920,
        "height": 1080,
        "panels": panels
    }

    with open("src/data/demo_seminar_layout.json", "w", encoding="utf-8") as f:
        json.dump(layout, f, indent=4, ensure_ascii=False)

    # Print verification
    for p in panels:
        for seg in p["telopSegments"]:
            lines = seg["text"].split("\n")
            print(f"  {p['id']}: {len(lines)}L | {seg['text'].replace(chr(10), ' / ')}")

    print(f"\nLayout generated! {len(panels)} panels")

if __name__ == "__main__":
    generate_layout()
