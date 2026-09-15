"""
MUKTI MAHAL MEDIA API
"""

from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from backend.supreme.ecosystem.mukti_mahal.media.controller import (
    MuktiMahalMediaController,
)


router = APIRouter(
    prefix="/mukti-mahal/media",
    tags=["Mukti Mahal Media"],
)


controller = MuktiMahalMediaController()


# =========================================================
# REQUEST MODELS
# =========================================================

class MediaCreateRequest(BaseModel):
    mahal_id: str
    title: str
    asset_type: str

    project_id: Optional[str] = None
    division_id: Optional[str] = None

    description: str = ""

    file_url: Optional[str] = None
    storage_key: Optional[str] = None
    mime_type: Optional[str] = None

    file_size: int = Field(
        default=0,
        ge=0,
    )

    status: str = "DRAFT"


class MediaUpdateRequest(BaseModel):
    title: Optional[str] = None
    asset_type: Optional[str] = None

    project_id: Optional[str] = None
    division_id: Optional[str] = None

    description: Optional[str] = None

    file_url: Optional[str] = None
    storage_key: Optional[str] = None
    mime_type: Optional[str] = None

    file_size: Optional[int] = Field(
        default=None,
        ge=0,
    )

    status: Optional[str] = None


# =========================================================
# SERIALIZATION
# =========================================================

def _to_dict(item):

    if item is None:
        return None

    if hasattr(item, "__dataclass_fields__"):
        return {
            key: getattr(item, key)
            for key in item.__dataclass_fields__
        }

    return item


# =========================================================
# STATUS
# =========================================================

@router.get("/")
def media_status():

    return controller.status()


@router.get("/status")
def media_system_status():

    return controller.status()


# =========================================================
# CREATE
# =========================================================

@router.post("/assets")
def create_media_asset(
    request: MediaCreateRequest,
):

    try:

        asset = controller.create_asset(
            mahal_id=request.mahal_id,
            title=request.title,
            asset_type=request.asset_type,
            project_id=request.project_id,
            division_id=request.division_id,
            description=request.description,
            file_url=request.file_url,
            storage_key=request.storage_key,
            mime_type=request.mime_type,
            file_size=request.file_size,
            status=request.status,
        )

        return {
            "status": "CREATED",
            "data": _to_dict(asset),
        }

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=f"{type(exc).__name__}: {exc}",
        )


# =========================================================
# LIST
# =========================================================

@router.get("/assets")
def list_media_assets(
    mahal_id: Optional[str] = None,
    project_id: Optional[str] = None,
    division_id: Optional[str] = None,
    asset_type: Optional[str] = None,
    status: Optional[str] = None,
):

    assets = controller.list_assets(
        mahal_id=mahal_id,
        project_id=project_id,
        division_id=division_id,
        asset_type=asset_type,
        status=status,
    )

    return {
        "status": "LIVE",
        "count": len(assets),
        "data": [
            _to_dict(asset)
            for asset in assets
        ],
    }


# =========================================================
# GET
# =========================================================

@router.get("/assets/{asset_id}")
def get_media_asset(
    asset_id: str,
):

    asset = controller.get_asset(asset_id)

    if not asset:

        raise HTTPException(
            status_code=404,
            detail="Media asset not found",
        )

    return {
        "status": "LIVE",
        "data": _to_dict(asset),
    }


# =========================================================
# UPDATE
# =========================================================

@router.put("/assets/{asset_id}")
def update_media_asset(
    asset_id: str,
    request: MediaUpdateRequest,
):

    asset = controller.update_asset(
        asset_id,
        **request.model_dump(
            exclude_unset=True
        ),
    )

    if not asset:

        raise HTTPException(
            status_code=404,
            detail="Media asset not found",
        )

    return {
        "status": "UPDATED",
        "data": _to_dict(asset),
    }


# =========================================================
# DELETE
# =========================================================

@router.delete("/assets/{asset_id}")
def delete_media_asset(
    asset_id: str,
):

    deleted = controller.delete_asset(
        asset_id
    )

    if not deleted:

        raise HTTPException(
            status_code=404,
            detail="Media asset not found",
        )

    return {
        "status": "DELETED",
        "asset_id": asset_id,
    }
