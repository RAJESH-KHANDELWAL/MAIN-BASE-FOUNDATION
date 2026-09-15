"""
MUKTI MAHAL
REAL AI PHOTO PROVIDER

Generates actual images through OpenAI's image API.

The provider is isolated so it can be replaced later
without changing the Mukti Mahal creation architecture.
"""

from __future__ import annotations

import os
from typing import Any, Dict, Optional

from openai import OpenAI


class PhotoProvider:

    def __init__(self) -> None:

        self.api_key = os.getenv(
            "OPENAI_API_KEY"
        )

        self.client: Optional[OpenAI] = None

        if self.api_key:

            self.client = OpenAI(
                api_key=self.api_key
            )

    def status(self) -> Dict[str, Any]:

        return {
            "provider": "openai",
            "type": "PHOTO",
            "status": (
                "READY"
                if self.client
                else "CONFIGURATION_REQUIRED"
            ),
        }

    def generate(
        self,
        prompt: str,
        model: str = "gpt-image-1",
        size: str = "1024x1024",
    ) -> Dict[str, Any]:

        if not self.client:

            raise RuntimeError(
                "OPENAI_API_KEY is not configured."
            )

        if not prompt.strip():

            raise ValueError(
                "Photo prompt is required."
            )

        result = self.client.images.generate(
            model=model,
            prompt=prompt,
            size=size,
        )

        data = getattr(
            result,
            "data",
            None,
        )

        if not data:

            raise RuntimeError(
                "Photo provider returned no image data."
            )

        first = data[0]

        return {
            "provider": "openai",
            "type": "PHOTO",
            "status": "COMPLETED",
            "model": model,
            "size": size,
            "image_url": getattr(
                first,
                "url",
                None,
            ),
            "revised_prompt": getattr(
                first,
                "revised_prompt",
                None,
            ),
        }
