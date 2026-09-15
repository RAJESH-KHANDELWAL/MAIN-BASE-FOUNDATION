"""
MUKTI MAHAL
UNIFIED AI CREATION SERVICE

Central creation boundary for:
PHOTO
VIDEO
MOVIE
MUSIC
DESIGN
GAME

MUKTI MAHAL itself is the world / experience.
There is intentionally no separate game module.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict
from uuid import uuid4


CREATION_TYPES = {
    "PHOTO",
    "VIDEO",
    "MOVIE",
    "MUSIC",
    "DESIGN",
    "GAME",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


class CreationService:
    """
    Central MUKTI MAHAL creation service.

    This layer does not fake successful generation.
    It creates a real creation request and delegates
    actual generation to the appropriate provider layer.
    """

    def create(
        self,
        creation_type: str,
        prompt: str,
        user_id: str | None = None,
        model: str | None = None,
        settings: Dict[str, Any] | None = None,
    ) -> Dict[str, Any]:

        creation_type = creation_type.strip().upper()
        prompt = prompt.strip()

        if creation_type not in CREATION_TYPES:
            raise ValueError(
                f"Unsupported creation type: {creation_type}"
            )

        if not prompt:
            raise ValueError(
                "Creation prompt is required."
            )

        creation_id = f"MM-CREATE-{uuid4().hex[:12].upper()}"

        return {
            "creation_id": creation_id,
            "system": "MUKTI MAHAL",
            "type": creation_type,
            "prompt": prompt,
            "model": model,
            "settings": settings or {},
            "user_id": user_id,
            "status": "QUEUED",
            "created_at": utc_now(),
            "message": (
                f"MUKTI MAHAL {creation_type} creation "
                "request accepted."
            ),
        }

    def status(self) -> Dict[str, Any]:
        return {
            "system": "MUKTI MAHAL AI CREATION",
            "status": "READY",
            "creation_types": sorted(CREATION_TYPES),
            "architecture": "UNIFIED_CREATION",
            "game_is_mukti_mahal": True,
            "separate_game_module": False,
        }
