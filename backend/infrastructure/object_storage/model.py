"""Object storage infrastructure models."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass
class ObjectStorageInfo:
    storage_id: str
    name: str
    storage_type: str
    bucket_name: str = ""
    region: str = ""
    provider: str = ""
    endpoint: str = ""
    capacity_gb: float = 0
    used_gb: float = 0
    status: str = "PLANNED"
    public_access: bool = False
    encryption_enabled: bool = True
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
            "bucket_name": self.bucket_name,
            "region": self.region,
            "provider": self.provider,
            "endpoint": self.endpoint,
            "capacity_gb": self.capacity_gb,
            "used_gb": self.used_gb,
            "status": self.status,
            "public_access": self.public_access,
            "encryption_enabled": self.encryption_enabled,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
