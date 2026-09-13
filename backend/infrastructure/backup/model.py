"""Backup infrastructure models."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass
class BackupInfo:
    backup_id: str
    name: str
    backup_type: str
    source_type: str = ""
    source_id: str = ""
    storage_id: str = ""
    provider: str = ""
    size_gb: float = 0
    status: str = "PLANNED"
    retention_days: int = 30
    encrypted: bool = True
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
            "backup_id": self.backup_id,
            "name": self.name,
            "backup_type": self.backup_type,
            "source_type": self.source_type,
            "source_id": self.source_id,
            "storage_id": self.storage_id,
            "provider": self.provider,
            "size_gb": self.size_gb,
            "status": self.status,
            "retention_days": self.retention_days,
            "encrypted": self.encrypted,
            "description": self.description,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
