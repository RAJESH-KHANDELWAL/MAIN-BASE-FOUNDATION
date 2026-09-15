"""
MUKTI MAHAL
REAL AI VIDEO PROVIDER

Provider adapter for OpenAI Videos API.

The provider is isolated from the Mukti Mahal
creation engine so the provider can be replaced
without changing the rest of the architecture.
"""

from __future__ import annotations

import os
from typing import Any, Dict, Optional

from openai import OpenAI


class VideoProvider:

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
            "type": "VIDEO",
            "status": (
                "READY"
                if self.client
                else "CONFIGURATION_REQUIRED"
            ),
            "model": "sora-2",
        }

    def generate(
        self,
        prompt: str,
        model: str = "sora-2",
        seconds: str = "4",
        size: str = "1280x720",
    ) -> Dict[str, Any]:

        if not self.client:

            raise RuntimeError(
                "OPENAI_API_KEY is not configured."
            )

        if not prompt.strip():

            raise ValueError(
                "Video prompt is required."
            )

        video = self.client.videos.create(
            model=model,
            prompt=prompt,
            seconds=seconds,
            size=size,
        )

        return self._serialize(video)

    def retrieve(
        self,
        video_id: str,
    ) -> Dict[str, Any]:

        if not self.client:

            raise RuntimeError(
                "OPENAI_API_KEY is not configured."
            )

        if not video_id.strip():

            raise ValueError(
                "Video ID is required."
            )

        video = self.client.videos.retrieve(
            video_id
        )

        return self._serialize(video)

    def _serialize(
        self,
        video: Any,
    ) -> Dict[str, Any]:

        return {
            "id": getattr(
                video,
                "id",
                None,
            ),
            "object": getattr(
                video,
                "object",
                "video",
            ),
            "model": getattr(
                video,
                "model",
                None,
            ),
            "status": getattr(
                video,
                "status",
                None,
            ),
            "progress": getattr(
                video,
                "progress",
                0,
            ),
            "prompt": getattr(
                video,
                "prompt",
                None,
            ),
            "seconds": getattr(
                video,
                "seconds",
                None,
            ),
            "size": getattr(
                video,
                "size",
                None,
            ),
            "created_at": getattr(
                video,
                "created_at",
                None,
            ),
            "completed_at": getattr(
                video,
                "completed_at",
                None,
            ),
            "expires_at": getattr(
                video,
                "expires_at",
                None,
            ),
            "error": self._serialize_error(
                getattr(
                    video,
                    "error",
                    None,
                )
            ),
        }

    def _serialize_error(
        self,
        error: Any,
    ) -> Optional[Dict[str, Any]]:

        if error is None:

            return None

        return {
            "code": getattr(
                error,
                "code",
                None,
            ),
            "message": getattr(
                error,
                "message",
                None,
            ),
        }
