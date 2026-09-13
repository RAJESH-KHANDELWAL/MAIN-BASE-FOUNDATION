"""Container infrastructure models."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass
class ContainerInfo:
    container_id: str
    name: str
    image: str
    server_id: str = ""
    provider: str = ""
    region: str = ""
    ports: str = ""
    status: str = "PLANNED"
    replicas: int = 1
    restart_policy: str = "ALWAYS"
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
            "container_id": self.container_id,
            "name": self.name,
            "image": self.image,
            "server_id": self.server_id,
            "provider": self.provider,
            "region": self.region,
            "ports": self.ports,
            "status": self.status,
            "replicas": self.replicas,
            "restart_policy": self.restart_policy,
            "description": self.description,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
