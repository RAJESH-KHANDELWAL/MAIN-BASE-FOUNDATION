"""
MAIN BASE FOUNDATION
Infrastructure - Hosting Controller

Control-plane facade for hosting management.
"""

from typing import Any, Dict, List, Optional

from .service import HostingService


class HostingController:
    """Controller for hosting infrastructure operations."""

    def __init__(self):
        self.service = HostingService()

    def create(
        self,
        hosting_type: str,
        plan_name: Optional[str] = None,
        domain_id: Optional[str] = None,
        server_id: Optional[str] = None,
        ip_address_id: Optional[str] = None,
        control_panel: Optional[str] = None,
        operating_system: Optional[str] = None,
        storage_id: Optional[str] = None,
        ssl_id: Optional[str] = None,
        root_access: bool = False,
        dedicated_ip: bool = False,
        cpu_cores: Optional[int] = None,
        memory_gb: Optional[float] = None,
        storage_gb: Optional[float] = None,
        bandwidth_gb: Optional[float] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        return self.service.create_hosting(
            hosting_type=hosting_type,
            plan_name=plan_name,
            domain_id=domain_id,
            server_id=server_id,
            ip_address_id=ip_address_id,
            control_panel=control_panel,
            operating_system=operating_system,
            storage_id=storage_id,
            ssl_id=ssl_id,
            root_access=root_access,
            dedicated_ip=dedicated_ip,
            cpu_cores=cpu_cores,
            memory_gb=memory_gb,
            storage_gb=storage_gb,
            bandwidth_gb=bandwidth_gb,
            metadata=metadata,
        )

    def get(
        self,
        hosting_id: str,
    ) -> Optional[Dict[str, Any]]:
        return self.service.get_hosting(hosting_id)

    def list(self) -> List[Dict[str, Any]]:
        return self.service.list_hosting()

    def list_by_type(
        self,
        hosting_type: str,
    ) -> List[Dict[str, Any]]:
        return self.service.list_by_type(hosting_type)

    def update(
        self,
        hosting_id: str,
        **fields: Any,
    ) -> Optional[Dict[str, Any]]:
        return self.service.update_hosting(
            hosting_id,
            **fields,
        )

    def delete(
        self,
        hosting_id: str,
    ) -> bool:
        return self.service.delete_hosting(hosting_id)

    def exists(
        self,
        hosting_id: str,
    ) -> bool:
        return self.service.exists(hosting_id)

    def attach_domain(
        self,
        hosting_id: str,
        domain_id: str,
    ) -> Optional[Dict[str, Any]]:
        return self.service.attach_domain(
            hosting_id,
            domain_id,
        )

    def attach_server(
        self,
        hosting_id: str,
        server_id: str,
    ) -> Optional[Dict[str, Any]]:
        return self.service.attach_server(
            hosting_id,
            server_id,
        )

    def attach_ip(
        self,
        hosting_id: str,
        ip_address_id: str,
    ) -> Optional[Dict[str, Any]]:
        return self.service.attach_ip(
            hosting_id,
            ip_address_id,
        )

    def attach_storage(
        self,
        hosting_id: str,
        storage_id: str,
    ) -> Optional[Dict[str, Any]]:
        return self.service.attach_storage(
            hosting_id,
            storage_id,
        )

    def attach_ssl(
        self,
        hosting_id: str,
        ssl_id: str,
    ) -> Optional[Dict[str, Any]]:
        return self.service.attach_ssl(
            hosting_id,
            ssl_id,
        )

    def set_active(
        self,
        hosting_id: str,
    ) -> Optional[Dict[str, Any]]:
        return self.service.set_active(hosting_id)

    def suspend(
        self,
        hosting_id: str,
    ) -> Optional[Dict[str, Any]]:
        return self.service.suspend(hosting_id)
