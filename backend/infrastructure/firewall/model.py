"""Firewall infrastructure models."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass
class FirewallInfo:
    firewall_id: str
    name: str
    firewall_type: str
    resource_type: str = ""
    resource_id: str = ""
    provider: str = ""
    region: str = ""
    status: str = "PLANNED"
    enabled: bool = True
    default_policy: str = "DENY"
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
            "firewall_id": self.firewall_id,
            "name": self.name,
            "firewall_type": self.firewall_type,
            "resource_type": self.resource_type,
            "resource_id": self.resource_id,
            "provider": self.provider,
            "region": self.region,
            "status": self.status,
            "enabled": self.enabled,
            "default_policy": self.default_policy,
            "description": self.description,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
