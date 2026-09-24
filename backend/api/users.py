
"""User API routes for MAIN-BASE-FOUNDATION."""

from __future__ import annotations

import re
import sqlite3
from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr, Field, field_validator

from backend.users.controller import UserController


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

controller = UserController()


class UserCreateRequest(BaseModel):
    """Request model for account creation."""

    full_name: str = Field(..., min_length=1, max_length=120)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)
    confirm_password: str = Field(..., min_length=8, max_length=128)

    @field_validator("full_name")
    @classmethod
    def validate_full_name(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Full name is required.")
        return value

    @field_validator("email")
    @classmethod
    def validate_gmail(cls, value: EmailStr) -> str:
        email = str(value).strip().lower()
        if not re.fullmatch(r"[a-zA-Z0-9._%+-]+@gmail\.com", email):
            raise ValueError("Please enter a valid Gmail address.")
        return email

    @field_validator("confirm_password")
    @classmethod
    def validate_password_match(cls, value: str, info):
        password = info.data.get("password")
        if password and value != password:
            raise ValueError("Passwords do not match.")
        return value


class UserUpdateRequest(BaseModel):
    """Request model for updating user profile."""

    full_name: Optional[str] = None
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    phone_no: Optional[str] = None
    mobile_no: Optional[str] = None
    whatsapp_no: Optional[str] = None
    password: Optional[str] = None
    role: Optional[str] = None
    status: Optional[str] = None


class PasswordVerifyRequest(BaseModel):
    username: str
    password: str


@router.get("/")
def get_users():
    users = controller.list()

    return {
        "message": "Users retrieved successfully",
        "data": [user.to_dict() for user in users],
    }


@router.get("/search")
def search_user(username: str):
    user = controller.search(username)

    return {
        "message": "User found" if user else "User not found",
        "data": user.to_dict() if user else None,
    }


@router.post("/register", status_code=201)
def register_user(payload: UserCreateRequest):
    """Register an account using full name, Gmail, and password."""

    try:
        user = controller.register(
            full_name=payload.full_name,
            email=str(payload.email),
            password=payload.password,
        )

        return {
            "message": (
                "Account created successfully. "
                "Email verification is not yet enabled."
            ),
            "data": user.to_dict(),
        }

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except sqlite3.IntegrityError as exc:
        raise HTTPException(
            status_code=409,
            detail="Account already exists or a unique field conflicts.",
        ) from exc


@router.post("/")
def create_user(payload: UserCreateRequest):
    """Compatibility endpoint for account creation."""
    return register_user(payload)


@router.post("/verify-password")
def verify_password(payload: PasswordVerifyRequest):
    authenticated = controller.verify_password(
        payload.username,
        payload.password,
    )

    return {
        "authenticated": authenticated,
        "username": payload.username,
    }


@router.get("/{user_id}")
def get_user(user_id: str):
    user = controller.get(user_id)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="USER_NOT_FOUND",
        )

    return {
        "message": "User retrieved successfully",
        "data": user.to_dict(),
    }


@router.put("/{user_id}")
def update_user(
    user_id: str,
    payload: UserUpdateRequest,
):
    try:
        user = controller.update(
            user_id=user_id,
            full_name=payload.full_name,
            username=payload.username,
            email=str(payload.email) if payload.email else None,
            phone=payload.phone,
            phone_no=payload.phone_no,
            mobile_no=payload.mobile_no,
            whatsapp_no=payload.whatsapp_no,
            password=payload.password,
            role=payload.role,
            status=payload.status,
        )

        if user is None:
            raise HTTPException(
                status_code=404,
                detail="USER_NOT_FOUND",
            )

        return {
            "message": "User updated successfully",
            "data": user.to_dict(),
        }

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except sqlite3.IntegrityError as exc:
        raise HTTPException(
            status_code=409,
            detail="Username or email already exists.",
        ) from exc


@router.delete("/{user_id}")
def delete_user(user_id: str):
    deleted = controller.delete(user_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="USER_NOT_FOUND",
        )

    return {
        "message": "User deleted successfully",
        "data": {
            "user_id": user_id,
            "deleted": True,
        },
    }
