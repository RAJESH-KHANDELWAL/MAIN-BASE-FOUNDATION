"""Identity API routes for MAIN-BASE-FOUNDATION."""

from __future__ import annotations

import sqlite3
from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.identity.controller import IdentityController


router = APIRouter(
    prefix="/identity",
    tags=["Identity"],
)

controller = IdentityController()


class IdentityCreateRequest(BaseModel):
    full_name: str
    username: str
    email: str
    phone: str

    supreme_id: str = ""
    display_name: str = ""

    name: str = ""
    domain: str = ""
    identity_type: str = "PERSON"

    country: str = ""
    state: str = ""
    city: str = ""

    language: str = "en"
    timezone: str = "UTC"

    status: str = "ACTIVE"

    profile_photo: str = ""
    profile_type: str = "PERSONAL"


class IdentityUpdateRequest(BaseModel):
    supreme_id: Optional[str] = None

    full_name: Optional[str] = None
    display_name: Optional[str] = None

    name: Optional[str] = None
    username: Optional[str] = None
    domain: Optional[str] = None
    identity_type: Optional[str] = None

    email: Optional[str] = None
    phone: Optional[str] = None

    country: Optional[str] = None
    state: Optional[str] = None
    city: Optional[str] = None

    language: Optional[str] = None
    timezone: Optional[str] = None

    status: Optional[str] = None

    profile_photo: Optional[str] = None
    profile_type: Optional[str] = None


@router.get("/")
def get_identity(master_id: str):
    """Get an identity by master ID."""

    identity = controller.get(master_id)

    if identity is None:
        raise HTTPException(
            status_code=404,
            detail="IDENTITY_NOT_FOUND",
        )

    return {
        "message": "Identity retrieved successfully",
        "data": identity.to_dict(),
    }


@router.get("/list")
def list_identity():
    """List all identities."""

    identities = controller.list()

    return {
        "message": "Identities retrieved successfully",
        "data": [
            identity.to_dict()
            for identity in identities
        ],
    }


@router.get("/unique/{unique_id}")
def get_identity_by_unique_id(
    unique_id: str,
):
    """Get an identity by its permanent 8-character unique ID."""

    unique_id = unique_id.strip().upper()

    if len(unique_id) != 8:
        raise HTTPException(
            status_code=400,
            detail="UNIQUE_ID_MUST_BE_8_CHARACTERS",
        )

    identities = controller.search(unique_id)

    identity = next(
        (
            item
            for item in identities
            if item.unique_id == unique_id
        ),
        None,
    )

    if identity is None:
        raise HTTPException(
            status_code=404,
            detail="IDENTITY_NOT_FOUND",
        )

    return {
        "message": "Identity retrieved successfully",
        "data": identity.to_dict(),
    }


@router.get("/search")
def search_identity(keyword: str):
    """Search identities."""

    identities = controller.search(keyword)

    return {
        "message": "Identity search completed",
        "data": [
            identity.to_dict()
            for identity in identities
        ],
    }


@router.get("/exists/{master_id}")
def identity_exists(master_id: str):
    """Check whether an identity exists."""

    return {
        "master_id": master_id,
        "exists": controller.exists(master_id),
    }


@router.post("/")
def create_identity(
    payload: IdentityCreateRequest,
):
    """Create and persist a new identity."""

    try:
        identity = controller.create(
            full_name=payload.full_name,
            username=payload.username,
            email=payload.email,
            phone=payload.phone,

            supreme_id=payload.supreme_id,
            display_name=payload.display_name,

            name=payload.name,
            domain=payload.domain,
            identity_type=payload.identity_type,

            country=payload.country,
            state=payload.state,
            city=payload.city,

            language=payload.language,
            timezone=payload.timezone,

            status=payload.status,

            profile_photo=payload.profile_photo,
            profile_type=payload.profile_type,
        )

        return {
            "message": "Identity created successfully",
            "data": identity.to_dict(),
        }

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except sqlite3.IntegrityError as exc:
        raise HTTPException(
            status_code=409,
            detail="Identity already exists.",
        ) from exc


@router.put("/verify/{master_id}")
def verify_identity(master_id: str):
    """Verify an identity."""

    identity = controller.verify(master_id)

    if identity is None:
        raise HTTPException(
            status_code=404,
            detail="IDENTITY_NOT_FOUND",
        )

    return {
        "message": "Identity verified successfully",
        "data": identity.to_dict(),
    }


@router.put("/{master_id}")
def update_identity(
    master_id: str,
    payload: IdentityUpdateRequest,
):
    """Update an existing identity."""

    try:
        identity = controller.update(
            master_id,
            **payload.model_dump(
                exclude_none=True
            ),
        )

        if identity is None:
            raise HTTPException(
                status_code=404,
                detail="IDENTITY_NOT_FOUND",
            )

        return {
            "message": "Identity updated successfully",
            "data": identity.to_dict(),
        }

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except sqlite3.IntegrityError as exc:
        raise HTTPException(
            status_code=409,
            detail="Identity already exists.",
        ) from exc


@router.delete("/{master_id}")
def delete_identity(master_id: str):
    """Delete an identity."""

    deleted = controller.delete(master_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="IDENTITY_NOT_FOUND",
        )

    return {
        "message": "Identity deleted successfully",
        "data": {
            "master_id": master_id,
            "deleted": True,
        },
    }
