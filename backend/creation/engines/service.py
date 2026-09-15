"""
MUKTI MAHAL
CREATION ENGINE

Central routing layer for real AI content creation.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict
from uuid import uuid4

from backend.creation.providers.photo_provider import (
    PhotoProvider,
)


SUPPORTED_TYPES = {
    "PHOTO",
    "VIDEO",
    "MOVIE",
    "MUSIC",
    "DESIGN",
    "GAME",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


class GenerationEngineService:

    def __init__(self) -> None:

        self.photo_provider = PhotoProvider()

    def create_request(
        self,
        creation_type: str,
        prompt: str,
        model: str | None = None,
        settings: Dict[str, Any] | None = None,
        user_id: str | None = None,
    ) -> Dict[str, Any]:

        creation_type = creation_type.strip().upper()
        prompt = prompt.strip()
        settings = settings or {}

        if creation_type not in SUPPORTED_TYPES:
            raise ValueError(
                f"Unsupported creation type: {creation_type}"
            )

        if not prompt:
            raise ValueError(
                "Creation prompt is required."
            )

        generation_id = (
            f"MM-GEN-{uuid4().hex[:12].upper()}"
        )

        if creation_type == "PHOTO":

            return self._create_photo(
                generation_id=generation_id,
                prompt=prompt,
                model=model,
                settings=settings,
                user_id=user_id,
            )

        return {
            "generation_id": generation_id,
            "system": "MUKTI MAHAL",
            "creation_type": creation_type,
            "engine": self._resolve_engine(
                creation_type
            ),
            "prompt": prompt,
            "model": model,
            "settings": settings,
            "user_id": user_id,
            "status": "QUEUED",
            "created_at": utc_now(),
            "message": (
                f"{creation_type} provider is "
                "not connected yet."
            ),
        }

    def _create_photo(
        self,
        generation_id: str,
        prompt: str,
        model: str | None,
        settings: Dict[str, Any],
        user_id: str | None,
    ) -> Dict[str, Any]:

        selected_model = (
            model or "gpt-image-1"
        )

        size = settings.get(
            "size",
            "1024x1024",
        )

        result = self.photo_provider.generate(
            prompt=prompt,
            model=selected_model,
            size=size,
        )

        return {
            "generation_id": generation_id,
            "system": "MUKTI MAHAL",
            "creation_type": "PHOTO",
            "engine": "PHOTO_GENERATION",
            "user_id": user_id,
            "created_at": utc_now(),
            "result": result,
        }

    def _resolve_engine(
        self,
        creation_type: str,
    ) -> str:

        engines = {
            "PHOTO": "PHOTO_GENERATION",
            "VIDEO": "VIDEO_GENERATION",
            "MOVIE": "MOVIE_PRODUCTION",
            "MUSIC": "MUSIC_GENERATION",
            "DESIGN": "DESIGN_GENERATION",
            "GAME": "MUKTI_MAHAL_WORLD_GENERATION",
        }

        return engines[creation_type]

    def status(self) -> Dict[str, Any]:

        return {
            "system": "MUKTI MAHAL CREATION ENGINE",
            "status": "READY",
            "supported_types": sorted(
                SUPPORTED_TYPES
            ),
            "providers": {
                "PHOTO": self.photo_provider.status(),
                "VIDEO": "NOT_CONNECTED",
                "MOVIE": "NOT_CONNECTED",
                "MUSIC": "NOT_CONNECTED",
                "DESIGN": "NOT_CONNECTED",
                "GAME": "NOT_CONNECTED",
            },
        }
