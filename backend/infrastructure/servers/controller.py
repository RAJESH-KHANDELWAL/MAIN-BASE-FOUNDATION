"""
MAIN BASE FOUNDATION
Infrastructure - Server Controller

Control-plane facade for server management.
"""

from typing import Any, Dict, List, Optional

from .service import ServerService


class ServerController:
    """Controller for server infrastructure operations."""

    def __init__(self):
        self.service = ServerService()

    def create(
        self,
        server_type: str,
        name: Optional[str] = None,
        provider: Optional[str] = None,
        location: Optional[str] = None,
        region: Optional[str] = None,
        datacenter: Optional[str] = None,
        ip_address_id: Optional[str] = None,
        operating_system: Optional[str] = None,
        control_panel: Optional[str] = None,
        cpu_cores: Optional[int] = None,
        memory_gb: Optional[float] = None,
        storage_gb: Optional[float] = None,
        bandwidth_gb: Optional[float] = None,
        virtualization: Optional[str] = None,
        root_access: bool = False,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        return self.service.create_server(
            server_type=server_type,
            name=name,
            provider=provider,
            location=location,
            region=region,
            datacenter=datacenter,
            ip_address_id=ip_address_id,
            operating_system=operating_system,
            control_panel=control_panel,
            cpu_cores=cpu_cores,
            memory_gb=memory_gb,
            storage_gb=storage_gb,
            bandwidth_gb=bandwidth_gb,
            virtualization=virtualization,
            root_access=root_access,
            metadata=metadata,
        )

    def get(
        self,
        server_id: str,
    ) -> Optional[Dict[str, Any]]:
        return self.service.get_server(server_id)

    def list(self) -> List[Dict[str, Any]]:
        return self.service.list_servers()

    def list_by_type(
        self,
        server_type: str,
    ) -> List[Dict[str, Any]]:
        return self.service.list_by_type(server_type)

    def update(
        self,
        server_id: str,
        **fields: Any,
    ) -> Optional[Dict[str, Any]]:
        return self.service.update_server(
            server_id,
            **fields,
        )

    def delete(
        self,
        server_id: str,
    ) -> bool:
        return self.service.delete_server(server_id)

    def exists(
        self,
        server_id: str,
    ) -> bool:
        return self.service.exists(server_id)

    def attach_ip(
        self,
        server_id: str,
        ip_address_id: str,
    ) -> Optional[Dict[str, Any]]:
        return self.service.attach_ip(
            server_id,
            ip_address_id,
        )

    def set_active(
        self,
        server_id: str,
    ) -> Optional[Dict[str, Any]]:
        return self.service.set_active(server_id)

    def set_maintenance(
        self,
        server_id: str,
    ) -> Optional[Dict[str, Any]]:
        return self.service.set_maintenance(server_id)

    def suspend(
        self,
        server_id: str,
    ) -> Optional[Dict[str, Any]]:
        return self.service.suspend(server_id)
