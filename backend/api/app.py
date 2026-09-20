from __future__ import annotations

from typing import Optional

from fastapi import (
    FastAPI,
    HTTPException,
)

from backend.auth.service import AuthenticationService
from backend.api.gallary_woult import router as gallary_woult_router


app = FastAPI(
    title="MAIN-BASE-FOUNDATION",
    version="1.0.0",
)


authentication_service = AuthenticationService()


def _require_ai_store_actor(
    authorization: Optional[str]
) -> str:
    """
    Authenticate the caller using the existing authentication system.

    The caller must provide:
        Authorization: Bearer <token>

    The token is validated through AuthenticationService.
    The authenticated username becomes the current AI Store actor.
    """

    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="AUTHORIZATION_REQUIRED"
        )

    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="INVALID_AUTHORIZATION_HEADER"
        )

    token = authorization[len("Bearer "):].strip()

    if not token:
        raise HTTPException(
            status_code=401,
            detail="EMPTY_AUTH_TOKEN"
        )

    result = authentication_service.validate_token(token)

    if not result.get("authenticated"):
        raise HTTPException(
            status_code=401,
            detail=result.get(
                "message",
                "INVALID_AUTHENTICATION_TOKEN"
            )
        )

    username = result.get("username")

    if not username:
        raise HTTPException(
            status_code=401,
            detail="AUTHENTICATED_USERNAME_NOT_FOUND"
        )

    return username


# ============================================================
# GALLARY WOULT
# ============================================================

app.include_router(
    gallary_woult_router
)


# ============================================================
# ROOT
# ============================================================

@app.get("/")
def root():
    return {
        "system": "MAIN-BASE-FOUNDATION",
        "status": "RUNNING",
        "gallary_woult": "CONNECTED",
        "ai_store": "CENTRAL",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "system": "MAIN-BASE-FOUNDATION",
    }
