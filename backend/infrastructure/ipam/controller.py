"""
MAIN BASE FOUNDATION
Infrastructure - IPAM Controller

Controller layer for IP Address Management.
"""

from typing import Any, Dict, List, Optional

from backend.infrastructure.ipam.service import IPAMService


class IPAMController:
    """
    Public controller facade for the IPAM service.
    """

    def __init__(self):
        self.service = IPAMService()

    def create(
        self,
        ip_address: str,
        address_family: str = "IPv4",
        allocation_type: str = "DEDICATED",
        provider: Optional[str] = None,
        network_id: Optional[str] = None,
        gateway: Optional[str] = None,
        subnet_mask: Optional[str] = None,
        reverse_dns: Optional[str] = None,
        status: str = "AVAILABLE",
        verified: bool = False,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:

        result = self.service.create(
            ip_address=ip_address,
            address_family=address_family,
            allocation_type=allocation_type,
            provider=provider,
            network_id=network_id,
            gateway=gateway,
            subnet_mask=subnet_mask,
            reverse_dns=reverse_dns,
            status=status,
            verified=verified,
            metadata=metadata,
        )

        return result.to_dict()

    def get(
        self,
        ip_address_id: str,
    ) -> Optional[Dict[str, Any]]:

        result = self.service.get(ip_address_id)

        if not result:
            return None

        return result.to_dict()

    def get_by_address(
        self,
        ip_address: str,
    ) -> Optional[Dict[str, Any]]:

        result = self.service.get_by_address(ip_address)

        if not result:
            return None

        return result.to_dict()

    def list(
        self,
        status: Optional[str] = None,
    ) -> List[Dict[str, Any]]:

        results = self.service.list(status=status)

        return [
            result.to_dict()
            for result in results
        ]

    def exists(
        self,
        ip_address_id: str,
    ) -> bool:

        return self.service.exists(ip_address_id)

    def update(
        self,
        ip_address_id: str,
        **updates,
    ) -> Optional[Dict[str, Any]]:

        result = self.service.update(
            ip_address_id,
            **updates,
        )

        if not result:
            return None

        return result.to_dict()

    def delete(
        self,
        ip_address_id: str,
    ) -> bool:

        return self.service.delete(ip_address_id)

    def attach_server(
        self,
        ip_address_id: str,
        server_id: str,
    ) -> Optional[Dict[str, Any]]:

        result = self.service.attach_server(
            ip_address_id,
            server_id,
        )

        if not result:
            return None

        return result.to_dict()

    def attach_hosting(
        self,
        ip_address_id: str,
        hosting_id: str,
    ) -> Optional[Dict[str, Any]]:

        result = self.service.attach_hosting(
            ip_address_id,
            hosting_id,
        )

        if not result:
            return None

        return result.to_dict()

    def attach_domain(
        self,
        ip_address_id: str,
        domain_id: str,
    ) -> Optional[Dict[str, Any]]:

        result = self.service.attach_domain(
            ip_address_id,
            domain_id,
        )

        if not result:
            return None

        return result.to_dict()

    def set_active(
        self,
        ip_address_id: str,
    ) -> Optional[Dict[str, Any]]:

        result = self.service.set_active(
            ip_address_id,
        )

        if not result:
            return None

        return result.to_dict()

    def reserve(
        self,
        ip_address_id: str,
    ) -> Optional[Dict[str, Any]]:

        result = self.service.reserve(
            ip_address_id,
        )

        if not result:
            return None

        return result.to_dict()

    def release(
        self,
        ip_address_id: str,
    ) -> Optional[Dict[str, Any]]:

        result = self.service.release(
            ip_address_id,
        )

        if not result:
            return None

        return result.to_dict()
