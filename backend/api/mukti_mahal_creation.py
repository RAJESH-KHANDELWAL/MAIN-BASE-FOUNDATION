"""
MUKTI MAHAL
UNIFIED AI CREATION API
"""

from typing import Any, Dict, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from backend.creation.service import (
    CreationService,
)


router = APIRouter(
    prefix="/mukti-mahal/creation",
    tags=["Mukti Mahal Creation"],
)


creation_service = CreationService()


class CreationRequest(BaseModel):
    creation_type: str = Field(
        min_length=1,
        max_length=32,
    )

    prompt: str = Field(
        min_length=1,
        max_length=32000,
    )

    user_id: Optional[str] = None

    model: Optional[str] = None

    settings: Dict[str, Any] = Field(
        default_factory=dict
    )


@router.get("/status")
def creation_status():

    return creation_service.status()


@router.post("/")
def create_content(
    request: CreationRequest,
):

    try:

        return creation_service.create(
            creation_type=request.creation_type,
            prompt=request.prompt,
            user_id=request.user_id,
            model=request.model,
            settings=request.settings,
        )

    except ValueError as exc:

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=f"{type(exc).__name__}: {exc}",
        )


@router.post("/{creation_type}")
def create_content_by_type(
    creation_type: str,
    request: CreationRequest,
):

    try:

        return creation_service.create(
            creation_type=creation_type,
            prompt=request.prompt,
            user_id=request.user_id,
            model=request.model,
            settings=request.settings,
        )

    except ValueError as exc:

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=f"{type(exc).__name__}: {exc}",
        )
