"""MAIN BASE FOUNDATION profile API."""

from __future__ import annotations

from typing import Any, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from backend.profiles.controller import ProfileController


router = APIRouter(
    prefix="/profiles",
    tags=["Profiles"],
)

controller = ProfileController()


class ProfileCreateRequest(BaseModel):
    """Request model for creating a profile."""

    profile_id: str = Field(min_length=1)
    master_id: str = Field(min_length=1)
    profile_type: str = Field(min_length=1)
    profile_name: str = Field(min_length=1)

    display_name: str = ""
    description: str = ""

    language: str = "en"

    country: str = ""
    state: str = ""
    city: str = ""

    metadata: dict[str, Any] = Field(default_factory=dict)


class ProfileUpdateRequest(BaseModel):
    """Request model for updating a profile."""

    profile_type: Optional[str] = None
    profile_name: Optional[str] = None

    display_name: Optional[str] = None
    description: Optional[str] = None

    language: Optional[str] = None

    country: Optional[str] = None
    state: Optional[str] = None
    city: Optional[str] = None

    verified: Optional[bool] = None
    status: Optional[str] = None

    metadata: Optional[dict[str, Any]] = None


@router.get("/")
def list_profiles(
    master_id: Optional[str] = None,
    profile_type: Optional[str] = None,
    status: Optional[str] = None,
):
    """List profiles."""

    profiles = controller.list(
        master_id=master_id,
        profile_type=profile_type,
        status=status,
    )

    return [profile.to_dict() for profile in profiles]


@router.get("/{profile_id}")
def get_profile(profile_id: str):
    """Get one profile."""

    profile = controller.get(profile_id)

    if profile is None:
        raise HTTPException(
            status_code=404,
            detail="Profile not found",
        )

    return profile.to_dict()


@router.post("/")
def create_profile(request: ProfileCreateRequest):
    """Create a new profile."""

    try:
        profile = controller.create(
            profile_id=request.profile_id,
            master_id=request.master_id,
            profile_type=request.profile_type,
            profile_name=request.profile_name,
            display_name=request.display_name,
            description=request.description,
            language=request.language,
            country=request.country,
            state=request.state,
            city=request.city,
            metadata=request.metadata,
        )

        return profile.to_dict()

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc


@router.put("/{profile_id}")
def update_profile(
    profile_id: str,
    request: ProfileUpdateRequest,
):
    """Update an existing profile."""

    updates = request.model_dump(
        exclude_none=True
    )

    try:
        profile = controller.update(
            profile_id=profile_id,
            updates=updates,
        )

        if profile is None:
            raise HTTPException(
                status_code=404,
                detail="Profile not found",
            )

        return profile.to_dict()

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc


@router.delete("/{profile_id}")
def delete_profile(profile_id: str):
    """Delete a profile."""

    deleted = controller.delete(profile_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Profile not found",
        )

    return {
        "profile_id": profile_id,
        "deleted": True,
    }


@router.get("/exists/{profile_id}")
def profile_exists(profile_id: str):
    """Check whether a profile exists."""

    return {
        "profile_id": profile_id,
        "exists": controller.exists(profile_id),
    }
