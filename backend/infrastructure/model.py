"""Infrastructure models for MAIN BASE FOUNDATION."""

from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass
class InfrastructureInfo:
    infrastructure_id: str
    name: str
    infrastructure_type: str
    provider: str = ""
    region: str = ""
    public_ipv4: str = ""
    public_ipv6: str = ""
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
            "infrastructure_id": self.infrastructure_id,
            "name": self.name,
            "infrastructure_type": self.infrastructure_type,
            "provider": self.provider,
            "region": self.region,
            "public_ipv4": self.public_ipv4,
            "public_ipv6": self.public_ipv6,
            "status": self.status,
            "description": self.description,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
