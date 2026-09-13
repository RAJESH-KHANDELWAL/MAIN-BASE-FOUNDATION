"""Email infrastructure models."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass
class EmailServiceInfo:
    email_id: str
    name: str
    email_type: str
    domain: str = ""
    provider: str = ""
    smtp_host: str = ""
    smtp_port: int = 0
    status: str = "PLANNED"
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
            "email_id": self.email_id,
            "name": self.name,
            "email_type": self.email_type,
            "domain": self.domain,
            "provider": self.provider,
            "smtp_host": self.smtp_host,
            "smtp_port": self.smtp_port,
            "status": self.status,
            "ssl_enabled": self.ssl_enabled,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
