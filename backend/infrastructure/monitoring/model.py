"""Monitoring infrastructure models."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass
class MonitoringInfo:
    monitoring_id: str
    name: str
    resource_type: str
    resource_id: str = ""
    endpoint: str = ""
    check_type: str = "HEALTH"
    interval_seconds: int = 60
    status: str = "PLANNED"
    last_check_at: str = ""
    last_status: str = ""
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
            "monitoring_id": self.monitoring_id,
            "name": self.name,
            "resource_type": self.resource_type,
            "resource_id": self.resource_id,
            "endpoint": self.endpoint,
            "check_type": self.check_type,
            "interval_seconds": self.interval_seconds,
            "status": self.status,
            "last_check_at": self.last_check_at,
            "last_status": self.last_status,
            "description": self.description,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
