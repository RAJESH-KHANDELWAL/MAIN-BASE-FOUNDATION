"""Identity models for MAIN-BASE-FOUNDATION."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone


def utc_now() -> str:
    """Return the current UTC timestamp."""
    return datetime.now(timezone.utc).isoformat()


@dataclass
class MasterIdentity:
    """Central identity record for the ecosystem."""

    id: int = 0

    master_id: str = ""
    identity_id: str = ""
    supreme_id: str = ""
    unique_id: str = ""

    full_name: str = ""
    display_name: str = ""
    name: str = ""
    username: str = ""
    domain: str = ""

    email: str = ""
    phone: str = ""

    country: str = ""
    state: str = ""
    city: str = ""

    language: str = "en"
    timezone: str = "UTC"

    identity_type: str = "PERSON"
    profile_type: str = "PERSONAL"

    status: str = "ACTIVE"
    verified: bool = False

    profile_photo: str = ""

    version: int = 1

    created_at: str = field(default_factory=utc_now)
    updated_at: str = field(default_factory=utc_now)

    def to_dict(self) -> dict:
        """Return the identity as a JSON-safe dictionary."""
        return {
            "id": self.id,
            "master_id": self.master_id,
            "identity_id": self.identity_id,
            "supreme_id": self.supreme_id,
            "unique_id": self.unique_id,
            "full_name": self.full_name,
            "display_name": self.display_name,
            "name": self.name,
            "username": self.username,
            "domain": self.domain,
            "email": self.email,
            "phone": self.phone,
            "country": self.country,
            "state": self.state,
            "city": self.city,
            "language": self.language,
            "timezone": self.timezone,
            "identity_type": self.identity_type,
            "profile_type": self.profile_type,
            "status": self.status,
            "verified": self.verified,
            "profile_photo": self.profile_photo,
            "version": self.version,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


@dataclass
class FoundationIdentity:
    """Core foundation identity."""

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
