"""
MUKTI MAHAL
CREATION ENGINE ROUTER

Central routing layer for real AI content creation.

Supported creation types:
PHOTO
VIDEO
MOVIE
MUSIC
DESIGN
GAME

MUKTI MAHAL itself is the game/world/experience.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict
from uuid import uuid4


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
    """
    Routes MUKTI MAHAL creation requests to the
    appropriate real generation engine.

    This class deliberately does not fabricate output URLs,
    files, completed statuses, or provider results.
    """

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

        engine = self._resolve_engine(
            creation_type
        )

        return {
            "generation_id": generation_id,
            "system": "MUKTI MAHAL",
            "creation_type": creation_type,
            "engine": engine,
            "prompt": prompt,
            "model": model,
            "settings": settings or {},
            "user_id": user_id,
            "status": "QUEUED",
            "created_at": utc_now(),
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
            "engines": {
                "PHOTO": "PHOTO_GENERATION",
                "VIDEO": "VIDEO_GENERATION",
                "MOVIE": "MOVIE_PRODUCTION",
                "MUSIC": "MUSIC_GENERATION",
                "DESIGN": "DESIGN_GENERATION",
                "GAME": "MUKTI_MAHAL_WORLD_GENERATION",
            },
        }
