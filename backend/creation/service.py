"""
MUKTI MAHAL
UNIFIED AI CREATION SERVICE

MUKTI MAHAL itself is the world,
game and experience.

Supported creation types:

PHOTO
VIDEO
MOVIE
MUSIC
DESIGN
GAME
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict
from uuid import uuid4

from backend.creation.image_service import (
    ImageCreationService,
)

from backend.creation.video_service import (
    VideoCreationService,
)


CREATION_TYPES = {
    "PHOTO",
    "VIDEO",
    "MOVIE",
    "MUSIC",
    "DESIGN",
    "GAME",
}


def utc_now() -> str:

    return datetime.now(
        timezone.utc
    ).isoformat()


class CreationService:

    def __init__(self) -> None:

        self.image_service = (
            ImageCreationService()
        )

        self.video_service = (
            VideoCreationService()
        )

    def create(
        self,
        creation_type: str,
        prompt: str,
        user_id: str | None = None,
        model: str | None = None,
        settings: Dict[str, Any] | None = None,
    ) -> Dict[str, Any]:

        creation_type = (
            creation_type.strip().upper()
        )

        prompt = prompt.strip()

        if creation_type not in CREATION_TYPES:

            raise ValueError(
                f"Unsupported creation type: "
                f"{creation_type}"
            )

        if not prompt:

            raise ValueError(
                "Creation prompt is required."
            )

        creation_id = (
            f"MM-CREATE-"
            f"{uuid4().hex[:12].upper()}"
        )

        settings = settings or {}

        # =========================================
        # REAL PHOTO
        # =========================================

        if creation_type == "PHOTO":

            result = (
                self.image_service.create_image(
                    prompt=prompt,
                    size=settings.get(
                        "size",
                        "1536x1024",
                    ),
                )
            )

            return {
                "creation_id": creation_id,
                "system": "MUKTI MAHAL",
                "type": "PHOTO",
                "status": "COMPLETED",
                "prompt": prompt,
                "result": result,
                "created_at": utc_now(),
            }

        # =========================================
        # REAL VIDEO
        # =========================================

        if creation_type == "VIDEO":

            result = (
                self.video_service.create_video(
                    prompt=prompt,
                )
            )

            return {
                "creation_id": creation_id,
                "system": "MUKTI MAHAL",
                "type": "VIDEO",
                "status": "COMPLETED",
                "prompt": prompt,
                "result": result,
                "created_at": utc_now(),
            }

        # =========================================
        # MOVIE
        # =========================================

        if creation_type == "MOVIE":

            return {
                "creation_id": creation_id,
                "system": "MUKTI MAHAL",
                "type": "MOVIE",
                "status": "PLANNED_PIPELINE",
                "prompt": prompt,
                "message": (
                    "Movie pipeline will use "
                    "multiple MUKTI MAHAL video scenes."
                ),
                "created_at": utc_now(),
            }

        # =========================================
        # GAME
        # =========================================

        if creation_type == "GAME":

            return {
                "creation_id": creation_id,
                "system": "MUKTI MAHAL",
                "type": "GAME",
                "status": "MUKTI_MAHAL_EXPERIENCE",
                "prompt": prompt,
                "message": (
                    "MUKTI MAHAL itself is the "
                    "interactive game/world experience."
                ),
                "created_at": utc_now(),
            }

        # =========================================
        # MUSIC / DESIGN
        # =========================================

        return {
            "creation_id": creation_id,
            "system": "MUKTI MAHAL",
            "type": creation_type,
            "status": "CREATION_PIPELINE",
            "prompt": prompt,
            "model": model,
            "settings": settings,
            "user_id": user_id,
            "created_at": utc_now(),
        }

    def status(self) -> Dict[str, Any]:

        return {
            "system": "MUKTI MAHAL AI CREATION",
            "status": "READY",
            "creation_types": sorted(
                CREATION_TYPES
            ),
            "providers": {
                "photo": (
                    self.image_service.status()
                ),
                "video": (
                    self.video_service.status()
                ),
            },
            "architecture": (
                "UNIFIED_CREATION"
            ),
            "game_is_mukti_mahal": True,
            "separate_game_module": False,
        }
