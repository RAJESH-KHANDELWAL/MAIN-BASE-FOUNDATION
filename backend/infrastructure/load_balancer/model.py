"""Load balancer infrastructure models."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass
class LoadBalancerInfo:
    load_balancer_id: str
    name: str
    load_balancer_type: str
    domain: str = ""
    network_id: str = ""
    provider: str = ""
    region: str = ""
    algorithm: str = "ROUND_ROBIN"
    status: str = "PLANNED"
    enabled: bool = True
    health_check_enabled: bool = True
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
            "load_balancer_id": self.load_balancer_id,
            "name": self.name,
            "load_balancer_type": self.load_balancer_type,
            "domain": self.domain,
            "network_id": self.network_id,
            "provider": self.provider,
            "region": self.region,
            "algorithm": self.algorithm,
            "status": self.status,
            "enabled": self.enabled,
            "health_check_enabled": self.health_check_enabled,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
