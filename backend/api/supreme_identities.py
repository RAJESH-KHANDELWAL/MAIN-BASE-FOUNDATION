"""Read-only registry for the four identities owned by one central owner.

This endpoint reports configured identity/repository metadata only.
It does not claim that remote repositories are authenticated or synchronized.
"""

from __future__ import annotations

from fastapi import APIRouter
from supreme_config import CONNECTED_REPOS, SUPREME_OWNER

router = APIRouter(prefix="/supreme", tags=["Supreme Identity Registry"])

IDENTITY_KEYS = (
    "RAJESHKHANDELWAL",
    "RAJESHKHANDELWALOFFICIAL",
    "DRRAJESHKHANDELWALIBC",
    "DRRAJESHKHANDELWALIBCOFFICIAL",
)


@router.get("/identities")
def list_supreme_identities() -> dict:
    records = []

    for key in IDENTITY_KEYS:
        repo = CONNECTED_REPOS.get(key, {})
        records.append({
            "identity_key": key,
            "username": key,
            "owner_person_id": SUPREME_OWNER["person_id"],
            "owner_role": "OWNER_ADMIN",
            "repository": repo.get("name", key),
            "repository_url": repo.get("url"),
            "homepage": repo.get("homepage"),
            "registry_status": "CONFIGURED",
            "connection_verified": False,
            "data_sync_status": "NOT_VERIFIED",
        })

    return {
        "hub": "SUPREMESETUHUB",
        "foundation": "MAIN BASE FOUNDATION",
        "owner_person_id": SUPREME_OWNER["person_id"],
        "owner_role": "OWNER_ADMIN",
        "identity_count": len(records),
        "identities": records,
        "integration_status": "REGISTRY_ONLY_REMOTE_CONNECTIONS_NOT_VERIFIED",
        "preserve_existing_data": True,
    }


@router.get("/identity-integration/status")
def identity_integration_status() -> dict:
    return {
        "hub": "SUPREMESETUHUB",
        "foundation": "MAIN BASE FOUNDATION",
        "owner_role": "OWNER_ADMIN",
        "configured_identity_count": len(IDENTITY_KEYS),
        "configured_identities": list(IDENTITY_KEYS),
        "remote_authentication": "NOT_CONFIGURED_OR_VERIFIED_HERE",
        "remote_data_import": "NOT_RUN",
        "automatic_sync": "NOT_VERIFIED",
        "existing_data_policy": "PRESERVE; NO DELETE OR OVERWRITE",
    }
