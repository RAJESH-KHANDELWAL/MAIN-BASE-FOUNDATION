"""IP Address Management models."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass
class IPAddressInfo:
    ip_id: str
    address: str
    address_family: str
    ip_type: str = "PUBLIC"
    network_id: str = ""
    server_id: str = ""
    provider: str = ""
    region: str = ""
    status: str = "PLANNED"
    allocation_type: str = "DYNAMIC"
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
            "ip_id": self.ip_id,
            "address": self.address,
            "address_family": self.address_family,
            "ip_type": self.ip_type,
            "network_id": self.network_id,
            "server_id": self.server_id,
            "provider": self.provider,
            "region": self.region,
            "status": self.status,
            "allocation_type": self.allocation_type,
            "description": self.description,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
