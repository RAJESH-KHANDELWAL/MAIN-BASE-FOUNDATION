"""
MAIN BASE FOUNDATION
Infrastructure - Network Controller

Controller layer for network infrastructure management.
"""

from typing import Any, Dict, List, Optional

from backend.infrastructure.network.service import NetworkService


class NetworkController:
    """
    Public controller facade for the NetworkService.
    """

    def __init__(self):
        self.service = NetworkService()

    def create(
        self,
        name: str,
        network_type: str = "PUBLIC",
        provider: Optional[str] = None,
        region: Optional[str] = None,
        datacenter: Optional[str] = None,
        cidr: Optional[str] = None,
        gateway: Optional[str] = None,
        subnet_mask: Optional[str] = None,
        dns_primary: Optional[str] = None,
        dns_secondary: Optional[str] = None,
        vlan_id: Optional[int] = None,
        status: str = "ACTIVE",
        verified: bool = False,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:

        result = self.service.create(
            name=name,
            network_type=network_type,
            provider=provider,
            region=region,
            datacenter=datacenter,
            cidr=cidr,
            gateway=gateway,
            subnet_mask=subnet_mask,
            dns_primary=dns_primary,
            dns_secondary=dns_secondary,
            vlan_id=vlan_id,
            status=status,
            verified=verified,
            metadata=metadata,
        )

        return result.to_dict()

    def get(
        self,
        network_id: str,
    ) -> Optional[Dict[str, Any]]:

        result = self.service.get(network_id)

        if not result:
            return None

        return result.to_dict()

    def get_by_name(
        self,
        name: str,
    ) -> Optional[Dict[str, Any]]:

        result = self.service.get_by_name(name)

        if not result:
            return None

        return result.to_dict()

    def list(
        self,
        status: Optional[str] = None,
        network_type: Optional[str] = None,
    ) -> List[Dict[str, Any]]:

        results = self.service.list(
            status=status,
            network_type=network_type,
        )

        return [
            result.to_dict()
            for result in results
        ]

    def list_by_type(
        self,
        network_type: str,
    ) -> List[Dict[str, Any]]:

        results = self.service.list_by_type(
            network_type
        )

        return [
            result.to_dict()
            for result in results
        ]

    def exists(
        self,
        network_id: str,
    ) -> bool:

        return self.service.exists(network_id)

    def update(
        self,
        network_id: str,
        **updates,
    ) -> Optional[Dict[str, Any]]:

        result = self.service.update(
            network_id,
            **updates,
        )

        if not result:
            return None

        return result.to_dict()

    def delete(
        self,
        network_id: str,
    ) -> bool:

        return self.service.delete(network_id)

    def set_active(
        self,
        network_id: str,
    ) -> Optional[Dict[str, Any]]:

        result = self.service.set_active(
            network_id
        )

        if not result:
            return None

        return result.to_dict()

    def set_maintenance(
        self,
        network_id: str,
    ) -> Optional[Dict[str, Any]]:

        result = self.service.set_maintenance(
            network_id
        )

        if not result:
            return None

        return result.to_dict()

    def suspend(
        self,
        network_id: str,
    ) -> Optional[Dict[str, Any]]:

        result = self.service.suspend(
            network_id
        )

        if not result:
            return None

        return result.to_dict()

    def set_offline(
        self,
        network_id: str,
    ) -> Optional[Dict[str, Any]]:

        result = self.service.set_offline(
            network_id
        )

        if not result:
            return None

        return result.to_dict()
