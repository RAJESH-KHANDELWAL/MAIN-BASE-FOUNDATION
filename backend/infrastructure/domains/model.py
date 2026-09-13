"""Domain infrastructure models."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass
class DomainInfo:
    domain_id: str
    domain: str
    status: str = "PLANNED"
    registrar: str = ""
    dns_zone_id: str = ""
    nameservers: list[str] | None = None
    registration_date: str = ""
    expiry_date: str = ""
    auto_renew: bool = True
    verified: bool = False
    created_at: str = ""
    updated_at: str = ""

    def __post_init__(self):
        now = datetime.now(timezone.utc).isoformat()

        if self.nameservers is None:
            self.nameservers = []

        if not self.created_at:
            self.created_at = now

        if not self.updated_at:
            self.updated_at = now

    def to_dict(self) -> dict:
        return {
            "domain_id": self.domain_id,
            "domain": self.domain,
            "status": self.status,
            "registrar": self.registrar,
            "dns_zone_id": self.dns_zone_id,
            "nameservers": self.nameservers,
            "registration_date": self.registration_date,
            "expiry_date": self.expiry_date,
            "auto_renew": self.auto_renew,
            "verified": self.verified,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
