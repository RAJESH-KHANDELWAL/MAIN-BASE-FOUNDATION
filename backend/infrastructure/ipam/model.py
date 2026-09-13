"""
MAIN BASE FOUNDATION
Infrastructure - IPAM Models

Virtual Temple style IP address management foundation.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, Optional


@dataclass
class IPAddressInfo:
    """
    Represents an IP address managed by the infrastructure
    control plane.

    IPAM = Internet Protocol Address Management.
    """

    ip_address_id: str
    ip_address: str

    address_family: str = "IPv4"
    allocation_type: str = "DEDICATED"
    provider: Optional[str] = None

    server_id: Optional[str] = None
    hosting_id: Optional[str] = None
    domain_id: Optional[str] = None

    network_id: Optional[str] = None
    gateway: Optional[str] = None
    subnet_mask: Optional[str] = None

    reverse_dns: Optional[str] = None

    status: str = "AVAILABLE"
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
            "ip_address_id": self.ip_address_id,
            "ip_address": self.ip_address,
            "address_family": self.address_family,
            "allocation_type": self.allocation_type,
            "provider": self.provider,
            "server_id": self.server_id,
            "hosting_id": self.hosting_id,
            "domain_id": self.domain_id,
            "network_id": self.network_id,
            "gateway": self.gateway,
            "subnet_mask": self.subnet_mask,
            "reverse_dns": self.reverse_dns,
            "status": self.status,
            "verified": self.verified,
            "metadata": self.metadata,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
