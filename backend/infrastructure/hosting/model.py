"""Hosting infrastructure models."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass
class HostingInfo:
    hosting_id: str
    name: str
    hosting_type: str
    server_id: str = ""
    domain: str = ""
    provider: str = ""
    plan: str = ""
    storage_gb: float = 0
    bandwidth_gb: float = 0
    status: str = "PLANNED"
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
            "hosting_id": self.hosting_id,
            "name": self.name,
            "hosting_type": self.hosting_type,
            "server_id": self.server_id,
            "domain": self.domain,
            "provider": self.provider,
            "plan": self.plan,
            "storage_gb": self.storage_gb,
            "bandwidth_gb": self.bandwidth_gb,
            "status": self.status,
            "description": self.description,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
