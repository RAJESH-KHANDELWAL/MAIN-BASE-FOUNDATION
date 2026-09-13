"""Security infrastructure models."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass
class SecurityInfo:
    security_id: str
    name: str
    security_type: str
    resource_type: str = ""
    resource_id: str = ""
    provider: str = ""
    status: str = "PLANNED"
    enabled: bool = True
    description: str = ""
    created_at: str = ""
    updated_at: str = ""

    def __post_init__(self):
        now = datetime.now(timezone.utc).isoformat()

        if not self.created_at:
            self.created_at = now

        if not self.updated_at:
            self.updated_at = now

    def to_dict(self) -> dict:
        return {
            "security_id": self.security_id,
            "name": self.name,
            "security_type": self.security_type,
            "resource_type": self.resource_type,
            "resource_id": self.resource_id,
            "provider": self.provider,
            "status": self.status,
            "enabled": self.enabled,
            "description": self.description,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
