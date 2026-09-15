"""
MUKTI MAHAL
REAL AI VIDEO CREATION SERVICE

Current provider:
Google Gemini API / Veo 3.1
"""

from __future__ import annotations

import os
import time
from pathlib import Path
from typing import Any, Dict, Optional

from google import genai


class VideoCreationService:

    def __init__(self) -> None:

        self.api_key = os.getenv(
            "GEMINI_API_KEY"
        )

        self.client: Optional[Any] = None

        if self.api_key:

            self.client = genai.Client(
                api_key=self.api_key
            )

        self.model = os.getenv(
            "MUKTI_MAHAL_VIDEO_MODEL",
            "veo-3.1-generate-preview",
        )

        self.asset_directory = (
            Path(__file__).resolve().parents[2]
            / "data"
            / "mukti_mahal"
            / "assets"
        )

        self.asset_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

    def status(self) -> Dict[str, Any]:

        return {
            "system": "MUKTI MAHAL AI VIDEO CREATION",
            "status": (
                "READY"
                if self.client
                else "CONFIGURATION_REQUIRED"
            ),
            "provider": "google",
            "provider_model": self.model,
        }

    def create_video(
        self,
        prompt: str,
    ) -> Dict[str, Any]:

        if not self.client:

            raise RuntimeError(
                "GEMINI_API_KEY is not configured."
            )

        prompt = prompt.strip()

        if not prompt:

            raise ValueError(
                "Video prompt is required."
            )

        operation = (
            self.client.models.generate_videos(
                model=self.model,
                prompt=prompt,
            )
        )

        while not operation.done:

            time.sleep(10)

            operation = (
                self.client.operations.get(
                    operation
                )
            )

        generated_video = (
            operation.response.generated_videos[0]
        )

        asset_id = (
            f"MM-VID-{os.urandom(6).hex().upper()}"
        )

        file_path = (
            self.asset_directory
            / f"{asset_id}.mp4"
        )

        self.client.files.download(
            file=generated_video.video,
            download_path=str(file_path),
        )

        return {
            "asset_id": asset_id,
            "type": "VIDEO",
            "status": "COMPLETED",
            "provider": "google",
            "model": self.model,
            "prompt": prompt,
            "file": str(file_path),
            "filename": file_path.name,
        }
