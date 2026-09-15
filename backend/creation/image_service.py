"""
MUKTI MAHAL
REAL AI IMAGE CREATION SERVICE

Provider:
OpenAI Images API
"""

from __future__ import annotations

import base64
import os
from pathlib import Path
from typing import Any, Dict, Optional

from openai import OpenAI


class ImageCreationService:

    def __init__(self) -> None:

        self.api_key = os.getenv("OPENAI_API_KEY")

        self.client: Optional[OpenAI] = None

        if self.api_key:
            self.client = OpenAI(
                api_key=self.api_key
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
            "system": "MUKTI MAHAL AI IMAGE CREATION",
            "status": (
                "READY"
                if self.client
                else "CONFIGURATION_REQUIRED"
            ),
            "provider": "openai",
            "model": "gpt-image-1",
        }

    def create_image(
        self,
        prompt: str,
        size: str = "1536x1024",
    ) -> Dict[str, Any]:

        if not self.client:

            raise RuntimeError(
                "OPENAI_API_KEY is not configured."
            )

        prompt = prompt.strip()

        if not prompt:

            raise ValueError(
                "Image prompt is required."
            )

        result = self.client.images.generate(
            model="gpt-image-1",
            prompt=prompt,
            size=size,
        )

        data = result.data[0]

        asset_id = (
            f"MM-IMG-{os.urandom(6).hex().upper()}"
        )

        file_path = (
            self.asset_directory
            / f"{asset_id}.png"
        )

        image_url = getattr(
            data,
            "url",
            None,
        )

        image_base64 = getattr(
            data,
            "b64_json",
            None,
        )

        if image_base64:

            image_bytes = base64.b64decode(
                image_base64
            )

            file_path.write_bytes(
                image_bytes
            )

        elif image_url:

            import httpx

            response = httpx.get(
                image_url,
                timeout=120,
            )

            response.raise_for_status()

            file_path.write_bytes(
                response.content
            )

        else:

            raise RuntimeError(
                "Image provider returned no image data."
            )

        return {
            "asset_id": asset_id,
            "type": "PHOTO",
            "status": "COMPLETED",
            "provider": "openai",
            "model": "gpt-image-1",
            "prompt": prompt,
            "file": str(file_path),
            "filename": file_path.name,
        }
