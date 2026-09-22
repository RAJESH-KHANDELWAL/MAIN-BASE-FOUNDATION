"""Identity models for MAIN-BASE-FOUNDATION."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional


def utc_now() -> str:
    """Return the current UTC timestamp."""
    return datetime.now(timezone.utc).isoformat()


@dataclass
class MasterIdentity:
    """Central identity record for the MAIN-BASE-FOUNDATION ecosystem."""

    master_id: str = ""
    identity_id: str = ""
    unique_id: str = ""

    name: str = ""
    username: str = ""
    domain: str = ""

    identity_type: str = "PERSON"
    profile_type: str = "PERSONAL"

    email: str = ""
    phone: str = ""

    profile_photo: str = ""
    status: str = "ACTIVE"

    version: int = 1

    created_at: str = field(default_factory=utc_now)
    updated_at: str = field(default_factory=utc_now)

    def to_dict(self) -> dict:
        """Return the identity as a JSON-safe dictionary."""
        return {
            "master_id": self.master_id,
            "identity_id": self.identity_id,
            "unique_id": self.unique_id,
            "name": self.name,
            "username": self.username,
            "domain": self.domain,
            "identity_type": self.identity_type,
            "profile_type": self.profile_type,
            "email": self.email,
            "phone": self.phone,
            "profile_photo": self.profile_photo,
            "status": self.status,
            "version": self.version,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


@dataclass
class FoundationIdentity:
    """Core foundation identity for MAIN-BASE-FOUNDATION."""

    foundation_id: str = ""
    unique_id: str = ""

    name: str = "MAIN BASE FOUNDATION"
    username: str = ""
    domain: str = ""

    identity_type: str = "FOUNDATION"
    profile_type: str = "CORE"

    status: str = "ACTIVE"
    version: int = 1

    created_at: str = field(default_factory=utc_now)
    updated_at: str = field(default_factory=utc_now)

    def to_dict(self) -> dict:
        """Return the foundation identity as a JSON-safe dictionary."""
        return {
            "foundation_id": self.foundation_id,
            "unique_id": self.unique_id,
            "name": self.name,
            "username": self.username,
            "domain": self.domain,
            "identity_type": self.identity_type,
            "profile_type": self.profile_type,
            "status": self.status,
            "version": self.version,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


__all__ = [
    "MasterIdentity",
    "FoundationIdentity",
]
