"""
MAIN BASE FOUNDATION
Infrastructure - DNS Models

Virtual Temple style DNS foundation.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, Optional


@dataclass
class DNSRecordInfo:
    """
    Represents a DNS record managed by the infrastructure
    control plane.
    """

    record_id: str
    domain_name: str

    record_type: str
    record_name: str
    record_value: str

    ttl: int = 3600
    priority: Optional[int] = None

    status: str = "ACTIVE"
    verified: bool = False

    metadata: Dict[str, Any] = field(default_factory=dict)

    created_at: str = field(
        default_factory=lambda: datetime.utcnow().isoformat()
    )
    updated_at: str = field(
        default_factory=lambda: datetime.utcnow().isoformat()
    )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "record_id": self.record_id,
            "domain_name": self.domain_name,
            "record_type": self.record_type,
            "record_name": self.record_name,
            "record_value": self.record_value,
            "ttl": self.ttl,
            "priority": self.priority,
            "status": self.status,
            "verified": self.verified,
            "metadata": self.metadata,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


@dataclass
class DNSZoneInfo:
    """
    Represents an authoritative DNS zone.
    """

    zone_id: str
    domain_name: str

    zone_type: str = "PRIMARY"

    primary_nameserver: Optional[str] = None
    secondary_nameserver: Optional[str] = None

    nameserver_status: str = "PENDING"
    dns_status: str = "PENDING"

    status: str = "ACTIVE"
    verified: bool = False

    metadata: Dict[str, Any] = field(default_factory=dict)

    created_at: str = field(
        default_factory=lambda: datetime.utcnow().isoformat()
    )
    updated_at: str = field(
        default_factory=lambda: datetime.utcnow().isoformat()
    )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "zone_id": self.zone_id,
            "domain_name": self.domain_name,
            "zone_type": self.zone_type,
            "primary_nameserver": self.primary_nameserver,
            "secondary_nameserver": self.secondary_nameserver,
            "nameserver_status": self.nameserver_status,
            "dns_status": self.dns_status,
            "status": self.status,
            "verified": self.verified,
            "metadata": self.metadata,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
