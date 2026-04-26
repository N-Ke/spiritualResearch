#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Google API専用 画像生成クライアント (Mac版)

Google AI の Nano Banana 2 / Nano Banana Pro を使用して
高品質なアニメ系イラストを生成する共通クライアントモジュール。

- Nano Banana 2 を優先使用し、失敗時のみ Nano Banana Pro にフォールバック
- Google API 以外のサービスへのフォールバックは一切行わない
- 新SDK google-genai (google.genai) を使用
"""

import io
import os
import sys
import time
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from google import genai
from google.genai import types
from PIL import Image


# ============================================================
#  モデル定義
# ============================================================

MODELS = [
    {
        "name": "Nano Banana 2",
        "model_id": "gemini-3.1-flash-image-preview",
        "description": "高速・高効率、Pro品質をFlashの速度で生成",
    },
    {
        "name": "Nano Banana Pro",
        "model_id": "gemini-3-pro-image-preview",
        "description": "高品質、複雑な編集・精密描画向け",
    },
]

# ============================================================
#  .env 検索パス（Mac用）
# ============================================================

ENV_SEARCH_PATHS = [
    Path.home() / "Documents" / "Obsidian Vault" / "demo" / "05_設定" / ".env",
    Path.home() / "Documents" / "Obsidian Vault" / "X_Post_System" / "2_Config" / ".env",
]


class GoogleImageClient:
    """
    Google API 専用の画像生成クライアント

    使い方:
        client = GoogleImageClient()
        success = client.generate_image("プロンプト", Path("output.png"))
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        クライアントを初期化する

        Args:
            api_key: Google API キー。未指定の場合は .env から自動読み込み
        """
        self.api_key = api_key or self._load_api_key()
        if not self.api_key:
            print("[NG] GOOGLE_API_KEY が設定されていません。")
            print("     以下のいずれかの場所に .env ファイルを作成してください:")
            for path in ENV_SEARCH_PATHS:
                print(f"     - {path}")
            print('     記入例: GOOGLE_API_KEY=AIzaSyXXXXXXXXXXXXXXX')
            sys.exit(1)

        self.client = genai.Client(api_key=self.api_key)
        masked_key = self.api_key[:10] + "..." if len(self.api_key) > 10 else "***"
        print(f"[OK] Google API Key: {masked_key}")
        print(f"[OK] モデル優先順位: {' → '.join(m['name'] for m in MODELS)}")

    def _load_api_key(self) -> Optional[str]:
        """
        .env ファイルから GOOGLE_API_KEY を読み込む
        複数の候補パスを順に検索し、最初に見つかったものを使用する
        """
        for env_path in ENV_SEARCH_PATHS:
            if env_path.exists():
                load_dotenv(env_path)
                key = os.getenv("GOOGLE_API_KEY")
                if key:
                    print(f"[OK] .env読み込み: {env_path}")
                    return key.strip()

        # カレントディレクトリの .env もチェック
        load_dotenv()
        key = os.getenv("GOOGLE_API_KEY")
        if key:
            print("[OK] .env読み込み: カレントディレクトリ")
            return key.strip()

        return None

    def generate_image(
        self,
        prompt: str,
        output_path: Path,
        retry: int = 3,
        retry_delay: float = 10.0,
        preferred_model: Optional[str] = None,
    ) -> bool:
        """
        プロンプトから画像を生成し、PNGファイルとして保存する

        Args:
            prompt: 画像生成プロンプト
            output_path: 保存先パス（.png）
            retry: 各モデルでのリトライ回数
            retry_delay: リトライ間の待機秒数
            preferred_model: 特定モデルを優先する場合のモデルID

        Returns:
            bool: 生成成功時 True、全モデル・全リトライで失敗時 False
        """
        # 出力ディレクトリを作成
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # モデルの順番を決定
        models = list(MODELS)
        if preferred_model:
            # 指定モデルを先頭に移動
            models.sort(key=lambda m: 0 if m["model_id"] == preferred_model else 1)

        for model_info in models:
            model_id = model_info["model_id"]
            model_name = model_info["name"]
            print(f"  モデル: {model_name} ({model_id})")

            for attempt in range(1, retry + 1):
                try:
                    response = self.client.models.generate_content(
                        model=model_id,
                        contents=[prompt],
                        config=types.GenerateContentConfig(
                            response_modalities=["IMAGE", "TEXT"]
                        ),
                    )

                    # レスポンスから画像データを抽出
                    image_data = self._extract_image_data(response)
                    if image_data is None:
                        print(f"    [NG] 画像データなし (試行 {attempt}/{retry})")
                        if attempt < retry:
                            print(f"    ... {retry_delay}秒後にリトライします")
                            time.sleep(retry_delay)
                        continue

                    # PNG形式で保存
                    with open(output_path, "wb") as f:
                        f.write(image_data)

                    # サイズ情報を表示
                    img = Image.open(output_path)
                    w, h = img.size
                    ratio = w / h if h > 0 else 0
                    print(f"    [OK] 保存完了: {output_path.name}")
                    print(f"    [OK] サイズ: {w}x{h} (比率: {ratio:.2f})")
                    return True

                except Exception as e:
                    error_msg = str(e)
                    print(f"    [NG] エラー (試行 {attempt}/{retry}): {error_msg[:100]}")
                    if attempt < retry:
                        print(f"    ... {retry_delay}秒後にリトライします")
                        time.sleep(retry_delay)

            print(f"  [NG] {model_name} での生成に失敗しました。次のモデルを試行します...")

        print(f"  [NG] すべてのモデルで生成に失敗しました: {output_path.name}")
        return False

    def _extract_image_data(self, response) -> Optional[bytes]:
        """
        APIレスポンスから画像データを抽出し、PNG形式で返す

        Args:
            response: Google AI のレスポンスオブジェクト

        Returns:
            bytes: PNG形式の画像データ、取得できなかった場合は None
        """
        if not hasattr(response, "candidates") or not response.candidates:
            return None

        for candidate in response.candidates:
            if not hasattr(candidate, "content") or not candidate.content:
                continue
            if not hasattr(candidate.content, "parts") or not candidate.content.parts:
                continue

            for part in candidate.content.parts:
                if hasattr(part, "inline_data") and part.inline_data is not None:
                    image_data = part.inline_data.data
                    mime_type = getattr(part.inline_data, "mime_type", "")

                    # JPEG → PNG 変換
                    if mime_type == "image/jpeg":
                        try:
                            img = Image.open(io.BytesIO(image_data))
                            buf = io.BytesIO()
                            img.save(buf, format="PNG")
                            image_data = buf.getvalue()
                        except Exception as e:
                            print(f"    [WARNING] JPEG→PNG変換失敗: {e}")

                    return image_data

        return None

    def verify_aspect_ratio(
        self, image_path: Path, expected_ratio: float = 16 / 9, tolerance: float = 0.15
    ) -> bool:
        """
        画像のアスペクト比を検証する

        Args:
            image_path: 検証する画像のパス
            expected_ratio: 期待するアスペクト比（デフォルト: 16:9 ≈ 1.778）
            tolerance: 許容誤差（デフォルト: 0.15）

        Returns:
            bool: 期待する比率に近ければ True
        """
        try:
            img = Image.open(image_path)
            w, h = img.size
            actual_ratio = w / h if h > 0 else 0

            is_ok = abs(actual_ratio - expected_ratio) <= tolerance
            status = "[OK]" if is_ok else "[WARNING]"
            print(
                f"    {status} アスペクト比検証: {w}x{h} "
                f"(比率: {actual_ratio:.2f}, 期待: {expected_ratio:.2f})"
            )
            return is_ok
        except Exception as e:
            print(f"    [NG] アスペクト比検証失敗: {e}")
            return False


# ============================================================
#  直接実行時のテスト
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("  Google Image Client — 動作テスト")
    print("=" * 60)
    print()

    client = GoogleImageClient()

    test_prompt = """
IMPORTANT: Generate this image in LANDSCAPE 16:9 widescreen aspect ratio.
Art style: Soft, warm Japanese anime illustration style inspired by Studio Ghibli.
Clean linework, soft coloring, pastel palette, warm golden lighting.
No text, no speech bubbles, no writing in the image.

Scene: A peaceful Japanese countryside at sunset.
A small traditional wooden house surrounded by green rice fields.
Cherry blossom petals floating in the warm orange evening sky.
Distant mountains bathed in golden light.
"""

    output_dir = Path(__file__).parent / "output"
    output_path = output_dir / "test_image.png"

    print()
    print("テスト画像を生成中...")
    print()

    success = client.generate_image(test_prompt, output_path)

    if success:
        client.verify_aspect_ratio(output_path)
        print()
        print(f"[OK] テスト成功！ 画像保存先: {output_path}")
        print(f"     Finderで確認: open {output_path.parent}")
    else:
        print()
        print("[NG] テスト失敗。APIキーとネットワーク接続を確認してください。")
