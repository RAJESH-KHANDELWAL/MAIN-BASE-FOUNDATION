"""Universal profile models."""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional


@dataclass
class Profile:
    """Represent a profile owned by a master identity."""

    profile_id: str
    master_id: str
    profile_type: str
    profile_name: str
    display_name: str = ""
    description: str = ""
    language: str = "en"
    country: str = ""
    state: str = ""
    city: str = ""
    verified: bool = False
    status: str = "ACTIVE"
    metadata: dict = field(default_factory=dict)
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    updated_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def to_dict(self) -> dict:
        return {
            "profile_id": self.profile_id,
            "master_id": self.master_id,
            "profile_type": self.profile_type,
            "profile_name": self.profile_name,
            "display_name": self.display_name,
            "description": self.description,
            "language": self.language,
            "country": self.country,
            "state": self.state,
            "city": self.city,
            "verified": self.verified,
            "status": self.status,
            "metadata": self.metadata,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


__all__ = ["Profile"]
