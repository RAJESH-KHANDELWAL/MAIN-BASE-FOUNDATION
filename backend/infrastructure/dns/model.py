"""DNS models for MAIN BASE FOUNDATION."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class DNSRecord:
    record_id: str
    zone_id: str
    record_type: str
    name: str
    content: str
    ttl: int = 300
    priority: int | None = None
    enabled: bool = True
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def to_dict(self) -> dict:
        return {
            "record_id": self.record_id,
            "zone_id": self.zone_id,
            "record_type": self.record_type,
            "name": self.name,
            "content": self.content,
            "ttl": self.ttl,
            "priority": self.priority,
            "enabled": self.enabled,
            "created_at": self.created_at,
        }


@dataclass
class DNSZone:
    zone_id: str
    domain: str
    status: str = "ACTIVE"
    nameservers: list[str] = field(default_factory=list)
    records: list[DNSRecord] = field(default_factory=list)
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    updated_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def to_dict(self) -> dict:
        return {
            "zone_id": self.zone_id,
            "domain": self.domain,
            "status": self.status,
            "nameservers": self.nameservers,
            "records": [
                record.to_dict()
                for record in self.records
            ],
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
