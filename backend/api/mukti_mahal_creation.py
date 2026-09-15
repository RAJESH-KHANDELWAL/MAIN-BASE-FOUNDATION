"""
MUKTI MAHAL
AI CREATION API
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from backend.creation.video_service import (
    VideoCreationService,
)


router = APIRouter(
    prefix="/mukti-mahal/creation",
    tags=["Mukti Mahal AI Creation"],
)


video_service =
    VideoCreationService()


class VideoCreateRequest(BaseModel):

    prompt: str = Field(
        min_length=1,
        max_length=32000,
    )

    model: str = "sora-2"

    seconds: str = "4"

    size: str = "1280x720"


@router.get("/status")
def creation_status():

    return video_service.status()


@router.post("/video")
def create_video(
    request: VideoCreateRequest,
):

    try:

        return video_service.create_video(
            prompt=request.prompt,
            model=request.model,
            seconds=request.seconds,
            size=request.size,
        )

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=f"{type(exc).__name__}: {exc}",
        )


@router.get("/video/{video_id}")
def get_video(
    video_id: str,
):

    try:

        return video_service.get_video(
            video_id
        )

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=f"{type(exc).__name__}: {exc}",
        )
