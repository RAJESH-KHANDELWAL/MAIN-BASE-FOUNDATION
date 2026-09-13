"""Server infrastructure models."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass
class ServerInfo:
    server_id: str
    name: str
    server_type: str
    provider: str = ""
    location: str = ""
    public_ipv4: str = ""
    public_ipv6: str = ""
    operating_system: str = ""
    cpu_cores: int = 0
    memory_gb: float = 0
    storage_gb: float = 0
    bandwidth_gb: float = 0
    status: str = "PLANNED"
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
            "server_id": self.server_id,
            "name": self.name,
            "server_type": self.server_type,
            "provider": self.provider,
            "location": self.location,
            "public_ipv4": self.public_ipv4,
            "public_ipv6": self.public_ipv6,
            "operating_system": self.operating_system,
            "cpu_cores": self.cpu_cores,
            "memory_gb": self.memory_gb,
            "storage_gb": self.storage_gb,
            "bandwidth_gb": self.bandwidth_gb,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
