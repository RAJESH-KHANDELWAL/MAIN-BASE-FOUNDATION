"""CDN infrastructure models."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass
class CDNInfo:
    cdn_id: str
    name: str
    domain: str
    origin_server_id: str = ""
    provider: str = ""
    region: str = ""
    status: str = "PLANNED"
    cache_enabled: bool = True
    ssl_enabled: bool = True
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
            "cdn_id": self.cdn_id,
            "name": self.name,
            "domain": self.domain,
            "origin_server_id": self.origin_server_id,
            "provider": self.provider,
            "region": self.region,
            "status": self.status,
            "cache_enabled": self.cache_enabled,
            "ssl_enabled": self.ssl_enabled,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
