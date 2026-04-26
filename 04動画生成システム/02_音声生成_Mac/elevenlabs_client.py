#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ElevenLabs 共通クライアント（Mac版）

ElevenLabs API を使用して音声生成を行う共通モジュール。
eleven_v3 モデル + with-timestamps エンドポイントを使用。
Audio Tags（感情タグ）対応。

使い方:
    from elevenlabs_client import ElevenLabsClient

    client = ElevenLabsClient()
    result = client.generate_speech(
        text="こんにちは、皆さん。",
        voice_id="XkfxZatpPaUTadDUJKRH",
        output_path=Path("output/narration.mp3"),
    )
"""

import base64
import io
import json
import time
from pathlib import Path

import httpx
from dotenv import load_dotenv
import os


# ============================================================
#  .env 読み込み（Mac用パス）
# ============================================================

ENV_PATHS = [
    Path.home() / "Documents" / "Obsidian Vault" / "demo" / "05_設定" / ".env",
    Path.home() / "Documents" / "Obsidian Vault" / "X_Post_System" / "2_Config" / ".env",
    Path(__file__).parent / ".env",
]


def _load_api_key() -> str:
    """複数の .env パスから ELEVENLABS_API_KEY を読み込む"""
    for env_path in ENV_PATHS:
        if env_path.exists():
            load_dotenv(env_path, override=False)
            print(f"[OK] .env読み込み: {env_path}")

    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise RuntimeError(
            "[NG] ELEVENLABS_API_KEY が見つかりません。\n"
            "以下のいずれかの .env に設定してください:\n"
            + "\n".join(f"  - {p}" for p in ENV_PATHS)
        )
    return api_key


# ============================================================
#  定数
# ============================================================

BASE_URL = "https://api.elevenlabs.io/v1"
DEFAULT_MODEL = "eleven_v3"

# シーン種別ごとのデフォルト voice_settings
VOICE_PRESETS = {
    "narration": {
        "stability": 0.55,
        "similarity_boost": 0.80,
        "style": 0.25,
        "use_speaker_boost": True,
    },
    "emotional": {
        "stability": 0.45,
        "similarity_boost": 0.80,
        "style": 0.30,
        "use_speaker_boost": True,
    },
    "bright": {
        "stability": 0.60,
        "similarity_boost": 0.80,
        "style": 0.15,
        "use_speaker_boost": True,
    },
}


# ============================================================
#  ElevenLabs クライアント
# ============================================================

class ElevenLabsClient:
    """ElevenLabs TTS API クライアント（Mac版）"""

    def __init__(self):
        self.api_key = _load_api_key()
        masked = self.api_key[:8] + "..."
        print(f"[OK] ElevenLabs API Key: {masked}")

    def generate_speech(
        self,
        text: str,
        voice_id: str,
        output_path: Path,
        preset: str = "narration",
        custom_settings: dict = None,
        model_id: str = DEFAULT_MODEL,
        retry: int = 3,
        retry_delay: float = 5.0,
    ) -> dict:
        """
        音声生成 + タイムスタンプ取得

        Args:
            text: 読み上げテキスト（Audio Tags対応）
            voice_id: ElevenLabs voice ID
            output_path: 出力 MP3 ファイルパス
            preset: プリセット名（'narration', 'emotional', 'bright'）
            custom_settings: カスタム voice_settings（プリセットより優先）
            model_id: モデルID
            retry: リトライ回数
            retry_delay: リトライ間隔（秒）

        Returns:
            dict: {
                "success": bool,
                "output_path": str,
                "duration_seconds": float,
                "alignment": dict (characters, start_times, end_times),
            }
        """
        # voice_settings の決定
        settings = custom_settings or VOICE_PRESETS.get(preset, VOICE_PRESETS["narration"])

        url = f"{BASE_URL}/text-to-speech/{voice_id}/with-timestamps"
        headers = {
            "xi-api-key": self.api_key,
            "Content-Type": "application/json",
        }
        payload = {
            "text": text,
            "model_id": model_id,
            "voice_settings": settings,
        }

        for attempt in range(1, retry + 1):
            try:
                with httpx.Client(timeout=60.0) as http_client:
                    response = http_client.post(url, headers=headers, json=payload)

                if response.status_code != 200:
                    print(f"    [NG] HTTP {response.status_code}: {response.text[:200]}")
                    if attempt < retry:
                        print(f"    ... {retry_delay}秒後にリトライします")
                        time.sleep(retry_delay)
                    continue

                data = response.json()

                # 音声データを保存
                audio_data = base64.b64decode(data["audio_base64"])
                output_path.parent.mkdir(parents=True, exist_ok=True)
                with open(output_path, "wb") as f:
                    f.write(audio_data)

                # タイムスタンプ取得
                alignment = data.get("alignment", {})
                characters = alignment.get("characters", [])
                start_times = alignment.get("character_start_times_seconds", [])
                end_times = alignment.get("character_end_times_seconds", [])

                # 音声尺を計算
                duration = end_times[-1] if end_times else 0.0

                print(f"    [OK] 保存完了: {output_path.name}")
                print(f"    [OK] 尺: {duration:.2f}秒")

                return {
                    "success": True,
                    "output_path": str(output_path),
                    "duration_seconds": duration,
                    "alignment": {
                        "characters": characters,
                        "start_times": start_times,
                        "end_times": end_times,
                    },
                }

            except Exception as e:
                print(f"    [NG] エラー (試行 {attempt}/{retry}): {e}")
                if attempt < retry:
                    print(f"    ... {retry_delay}秒後にリトライします")
                    time.sleep(retry_delay)

        return {"success": False, "output_path": None, "duration_seconds": 0, "alignment": None}

    def get_telop_segments(self, alignment: dict, fps: int = 30) -> list:
        """
        タイムスタンプからテロップ分割点を計算

        Args:
            alignment: generate_speech の返り値の alignment
            fps: フレームレート

        Returns:
            list: [{"text": str, "start_frame": int, "end_frame": int}, ...]
        """
        if not alignment:
            return []

        characters = alignment["characters"]
        start_times = alignment["start_times"]
        end_times = alignment["end_times"]

        segments = []
        current_text = ""
        segment_start_frame = 0

        for i, char in enumerate(characters):
            current_text += char
            if char in ["。", "？", "！", "\n"]:
                end_frame = round(end_times[i] * fps)
                segments.append({
                    "text": current_text.strip(),
                    "start_frame": segment_start_frame,
                    "end_frame": end_frame + 3,  # 少し余裕
                })
                current_text = ""
                segment_start_frame = end_frame

        # 残りのテキスト
        if current_text.strip():
            end_frame = round(end_times[-1] * fps) if end_times else segment_start_frame
            segments.append({
                "text": current_text.strip(),
                "start_frame": segment_start_frame,
                "end_frame": end_frame + 3,
            })

        return segments
