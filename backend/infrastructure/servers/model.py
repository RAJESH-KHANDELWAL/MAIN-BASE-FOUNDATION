"""
MAIN BASE FOUNDATION
Infrastructure - Server Models

Virtual Temple style server foundation.
A server is an infrastructure resource that can host
one or more hosting resources.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, Optional


@dataclass
class ServerInfo:
    """
    Represents a physical, virtual, or dedicated server
    managed by the infrastructure control plane.
    """

    server_id: str
    server_type: str

    name: Optional[str] = None
    provider: Optional[str] = None
    location: Optional[str] = None
    region: Optional[str] = None
    datacenter: Optional[str] = None

    ip_address_id: Optional[str] = None

    operating_system: Optional[str] = None
    control_panel: Optional[str] = None

    cpu_cores: Optional[int] = None
    memory_gb: Optional[float] = None
    storage_gb: Optional[float] = None
    bandwidth_gb: Optional[float] = None

    virtualization: Optional[str] = None

    status: str = "PROVISIONING"
    verified: bool = False

    root_access: bool = False

    metadata: Dict[str, Any] = field(default_factory=dict)

    created_at: str = field(
        default_factory=lambda: datetime.utcnow().isoformat()
    )

    updated_at: str = field(
        default_factory=lambda: datetime.utcnow().isoformat()
    )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "server_id": self.server_id,
            "server_type": self.server_type,
            "name": self.name,
            "provider": self.provider,
            "location": self.location,
            "region": self.region,
            "datacenter": self.datacenter,
            "ip_address_id": self.ip_address_id,
            "operating_system": self.operating_system,
            "control_panel": self.control_panel,
            "cpu_cores": self.cpu_cores,
            "memory_gb": self.memory_gb,
            "storage_gb": self.storage_gb,
            "bandwidth_gb": self.bandwidth_gb,
            "virtualization": self.virtualization,
            "status": self.status,
            "verified": self.verified,
            "root_access": self.root_access,
            "metadata": self.metadata,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
