"""SSL/TLS infrastructure models."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass
class SSLInfo:
    ssl_id: str
    domain: str
    certificate_type: str = "TLS"
    issuer: str = ""
    certificate_status: str = "PLANNED"
    expires_at: str = ""
    auto_renew: bool = True
    server_id: str = ""
    provider: str = ""
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
            "ssl_id": self.ssl_id,
            "domain": self.domain,
            "certificate_type": self.certificate_type,
            "issuer": self.issuer,
            "certificate_status": self.certificate_status,
            "expires_at": self.expires_at,
            "auto_renew": self.auto_renew,
            "server_id": self.server_id,
            "provider": self.provider,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
