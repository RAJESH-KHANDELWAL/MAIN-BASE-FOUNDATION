"""User API routes for MAIN-BASE-FOUNDATION."""

from __future__ import annotations

import sqlite3
from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.users.controller import UserController


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

controller = UserController()


class UserCreateRequest(BaseModel):
    user_id: Optional[str] = None
    full_name: str
    username: str
    email: str
    phone: str
    password: str
    role: str = "USER"
    status: str = "ACTIVE"


class UserUpdateRequest(BaseModel):
    full_name: Optional[str] = None
    username: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
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


@router.post("/")
def create_user(payload: UserCreateRequest):
    try:
        user = controller.register(
            user_id=payload.user_id,
            full_name=payload.full_name,
            username=payload.username,
            email=payload.email,
            phone=payload.phone,
            password=payload.password,
            role=payload.role,
            status=payload.status,
        )

        return {
            "message": "User created successfully",
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
            detail="User ID or username already exists.",
        ) from exc


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
            email=payload.email,
            phone=payload.phone,
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
            detail="Username already exists.",
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
