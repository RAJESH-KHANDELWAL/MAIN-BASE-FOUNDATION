from __future__ import annotations

from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from backend.auth.service import AuthenticationService

from backend.api.auth import router as auth_router
from backend.api.businesses import router as businesses_router
from backend.api.dashboard import router as dashboard_router
from backend.api.dns import router as dns_router
from backend.api.gallary_woult import router as gallary_woult_router
from backend.api.identity import router as identity_router
from backend.api.infrastructure import router as infrastructure_router
from backend.api.matching import router as matching_router
from backend.api.mukti_mahal import router as mukti_mahal_router
from backend.api.mukti_mahal_creation import (
    router as mukti_mahal_creation_router,
)
from backend.api.mukti_mahal_media import (
    router as mukti_mahal_media_router,
)
from backend.api.opportunities import router as opportunities_router
from backend.api.profiles import router as profiles_router
from backend.api.projects import router as projects_router
from backend.api.roles import router as roles_router
from backend.api.supreme import router as supreme_router
from backend.api.users import router as users_router


app = FastAPI(
    title="MAIN-BASE-FOUNDATION",
    version="1.0.0",
)
# ============================================================
# FRONTEND / WEBSITE CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        # ----------------------------------------------------
        # GITHUB PAGES
        # ----------------------------------------------------
        "https://rajeshkhandelwal.github.io",
        "https://rajeshkhandelwalofficial.github.io",
        "https://drrajeshkhandelwalibc.github.io",
        "https://drrajeshkhandelwalibcofficial.github.io",

        # ----------------------------------------------------
        # MAIN DOMAINS
        # ----------------------------------------------------
        "https://rajeshkhandelwal.com",
        "https://www.rajeshkhandelwal.com",

        "https://rajeshkhandelwalofficial.com",
        "https://www.rajeshkhandelwalofficial.com",

        "https://drrajeshkhandelwalibc.com",
        "https://www.drrajeshkhandelwalibc.com",

        "https://drrajeshkhandelwalibcofficial.com",
        "https://www.drrajeshkhandelwalibcofficial.com",

        # ----------------------------------------------------
        # CURRENT GITHUB PAGES FRONTEND
        # ----------------------------------------------------
        "https://rajeshkhandelwalofficial.github.io",
    ],

    allow_credentials=True,

    allow_methods=[
        "*"
    ],

    allow_headers=[
        "*"
    ],
)

authentication_service = AuthenticationService()


def _require_ai_store_actor(
    authorization: Optional[str],
) -> str:

    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="AUTHORIZATION_REQUIRED",
        )

    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="INVALID_AUTHORIZATION_HEADER",
        )

    token = authorization[len("Bearer "):].strip()

    if not token:
        raise HTTPException(
            status_code=401,
            detail="EMPTY_AUTH_TOKEN",
        )

    result = authentication_service.validate_token(token)

    if not result.get("authenticated"):
        raise HTTPException(
            status_code=401,
            detail=result.get(
                "message",
                "INVALID_AUTHENTICATION_TOKEN",
            ),
        )

    username = result.get("username")

    if not username:
        raise HTTPException(
            status_code=401,
            detail="AUTHENTICATED_USERNAME_NOT_FOUND",
        )

    return username


# ============================================================
# CORE API ROUTERS
# ============================================================

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(identity_router)
app.include_router(profiles_router)
app.include_router(businesses_router)
app.include_router(projects_router)
app.include_router(opportunities_router)
app.include_router(matching_router)
app.include_router(roles_router)
app.include_router(supreme_router)
app.include_router(dashboard_router)
app.include_router(infrastructure_router)
app.include_router(dns_router)


# ============================================================
# GALLARY WOULT
# ============================================================

app.include_router(
    gallary_woult_router
)


# ============================================================
# MUKTI MAHAL
# ============================================================

app.include_router(
    mukti_mahal_router
)

app.include_router(
    mukti_mahal_creation_router
)

app.include_router(
    mukti_mahal_media_router
)


# ============================================================
# ROOT
# ============================================================

@app.get("/")
def root():

    return {
        "name": "MAIN-BASE-FOUNDATION",
        "status": "RUNNING",
        "gallary_woult": "CONNECTED",
        "api_surface": "CONNECTED",
        "mukti_mahal": "CONNECTED",
    }


# ============================================================
# HEALTH
# ============================================================

@app.get("/health")
def health():

    return {
        "status": "healthy",
        "service": "MAIN-BASE-FOUNDATION",
    }
