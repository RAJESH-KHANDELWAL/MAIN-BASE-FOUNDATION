"""Core identity models for MAIN-BASE-FOUNDATION."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


def _utc_now() -> str:
    return datetime.utcnow().isoformat()


@dataclass
class MasterIdentity:
    """Represent the master identity of a platform user."""

    id: Optional[int] = None
    master_id: str = ""
    identity_id: str = ""
    supreme_id: str = ""
    full_name: str = ""
    display_name: str = ""
    username: str = ""
    email: str = ""
    phone: str = ""
    country: str = ""
    state: str = ""
    city: str = ""
    language: str = "en"
    timezone: str = "UTC"
    status: str = "ACTIVE"
    verified: bool = False
    profile_photo: str = ""
    profile_type: str = "PERSONAL"
    version: int = 1
    created_at: str = field(default_factory=_utc_now)
    updated_at: str = field(default_factory=_utc_now)

    def to_dict(self) -> dict:
        """Return the complete public identity representation."""
        return {
            "id": self.id,
            "master_id": self.master_id,
            "identity_id": self.identity_id,
            "supreme_id": self.supreme_id,
            "full_name": self.full_name,
            "display_name": self.display_name,
            "username": self.username,
            "email": self.email,
            "phone": self.phone,
            "country": self.country,
            "state": self.state,
            "city": self.city,
            "language": self.language,
            "timezone": self.timezone,
            "status": self.status,
            "verified": self.verified,
            "profile_photo": self.profile_photo,
            "profile_type": self.profile_type,
            "version": self.version,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


__all__ = ["MasterIdentity"]
