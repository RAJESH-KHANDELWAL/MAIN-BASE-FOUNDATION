"""Storage infrastructure models."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass
class StorageInfo:
    storage_id: str
    name: str
    storage_type: str
    server_id: str = ""
    provider: str = ""
    region: str = ""
    capacity_gb: float = 0
    used_gb: float = 0
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
            "storage_id": self.storage_id,
            "name": self.name,
            "storage_type": self.storage_type,
            "server_id": self.server_id,
            "provider": self.provider,
            "region": self.region,
            "capacity_gb": self.capacity_gb,
            "used_gb": self.used_gb,
            "status": self.status,
            "description": self.description,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
