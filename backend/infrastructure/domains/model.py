"""
MAIN BASE FOUNDATION
Infrastructure - Domain Models

Virtual Temple style domain foundation.
A domain is kept independent from any specific personal website.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, Optional


@dataclass
class DomainInfo:
    """
    Represents a domain managed by the infrastructure control plane.
    """

    domain_id: str
    domain_name: str

    registrar: Optional[str] = None
    registration_status: str = "PENDING"
    nameserver_status: str = "PENDING"
    dns_status: str = "PENDING"

    hosting_id: Optional[str] = None
    server_id: Optional[str] = None
    ip_address_id: Optional[str] = None
    ssl_id: Optional[str] = None

    auto_renew: bool = True
    verified: bool = False
    status: str = "PENDING"

    metadata: Dict[str, Any] = field(default_factory=dict)

    created_at: str = field(
        default_factory=lambda: datetime.utcnow().isoformat()
    )
    updated_at: str = field(
        default_factory=lambda: datetime.utcnow().isoformat()
    )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "domain_id": self.domain_id,
            "domain_name": self.domain_name,
            "registrar": self.registrar,
            "registration_status": self.registration_status,
            "nameserver_status": self.nameserver_status,
            "dns_status": self.dns_status,
            "hosting_id": self.hosting_id,
            "server_id": self.server_id,
            "ip_address_id": self.ip_address_id,
            "ssl_id": self.ssl_id,
            "auto_renew": self.auto_renew,
            "verified": self.verified,
            "status": self.status,
            "metadata": self.metadata,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
