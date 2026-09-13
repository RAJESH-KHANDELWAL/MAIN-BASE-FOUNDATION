"""
MAIN BASE FOUNDATION
Infrastructure - Hosting Models

Virtual Temple style hosting resource foundation.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, Optional


@dataclass
class HostingInfo:
    """
    Represents a hosting resource managed by the
    MAIN BASE FOUNDATION infrastructure control plane.
    """

    hosting_id: str
    hosting_type: str

    plan_name: Optional[str] = None
    domain_id: Optional[str] = None
    server_id: Optional[str] = None
    ip_address_id: Optional[str] = None

    control_panel: Optional[str] = None
    operating_system: Optional[str] = None

    storage_id: Optional[str] = None
    ssl_id: Optional[str] = None

    resource_status: str = "PROVISIONING"
    status: str = "PENDING"

    root_access: bool = False
    dedicated_ip: bool = False

    cpu_cores: Optional[int] = None
    memory_gb: Optional[float] = None
    storage_gb: Optional[float] = None
    bandwidth_gb: Optional[float] = None

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
            "hosting_id": self.hosting_id,
            "hosting_type": self.hosting_type,
            "plan_name": self.plan_name,
            "domain_id": self.domain_id,
            "server_id": self.server_id,
            "ip_address_id": self.ip_address_id,
            "control_panel": self.control_panel,
            "operating_system": self.operating_system,
            "storage_id": self.storage_id,
            "ssl_id": self.ssl_id,
            "resource_status": self.resource_status,
            "status": self.status,
            "root_access": self.root_access,
            "dedicated_ip": self.dedicated_ip,
            "cpu_cores": self.cpu_cores,
            "memory_gb": self.memory_gb,
            "storage_gb": self.storage_gb,
            "bandwidth_gb": self.bandwidth_gb,
            "verified": self.verified,
            "metadata": self.metadata,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
