"""
MAIN BASE FOUNDATION
Infrastructure - Network Models

Virtual Temple style network foundation.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, Optional


@dataclass
class NetworkInfo:
    """
    Represents a network managed by the infrastructure
    control plane.
    """

    network_id: str
    name: str

    network_type: str = "PUBLIC"
    provider: Optional[str] = None

    region: Optional[str] = None
    datacenter: Optional[str] = None

    cidr: Optional[str] = None
    gateway: Optional[str] = None
    subnet_mask: Optional[str] = None

    dns_primary: Optional[str] = None
    dns_secondary: Optional[str] = None

    vlan_id: Optional[int] = None

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
            "network_id": self.network_id,
            "name": self.name,
            "network_type": self.network_type,
            "provider": self.provider,
            "region": self.region,
            "datacenter": self.datacenter,
            "cidr": self.cidr,
            "gateway": self.gateway,
            "subnet_mask": self.subnet_mask,
            "dns_primary": self.dns_primary,
            "dns_secondary": self.dns_secondary,
            "vlan_id": self.vlan_id,
            "status": self.status,
            "verified": self.verified,
            "metadata": self.metadata,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
