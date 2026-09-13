"""Network infrastructure models."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass
class NetworkInfo:
    network_id: str
    name: str
    network_type: str
    server_id: str = ""
    provider: str = ""
    region: str = ""
    public_ipv4: str = ""
    public_ipv6: str = ""
    subnet: str = ""
    gateway: str = ""
    bandwidth_mbps: float = 0
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
            "network_id": self.network_id,
            "name": self.name,
            "network_type": self.network_type,
            "server_id": self.server_id,
            "provider": self.provider,
            "region": self.region,
            "public_ipv4": self.public_ipv4,
            "public_ipv6": self.public_ipv6,
            "subnet": self.subnet,
            "gateway": self.gateway,
            "bandwidth_mbps": self.bandwidth_mbps,
            "status": self.status,
            "description": self.description,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
