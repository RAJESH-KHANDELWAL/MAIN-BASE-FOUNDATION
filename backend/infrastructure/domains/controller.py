"""
MAIN BASE FOUNDATION
Infrastructure - Domain Controller

Control-plane facade for domain management.
"""

from typing import Any, Dict, List, Optional

from .service import DomainService


class DomainController:
    """Controller for domain infrastructure operations."""

    def __init__(self):
        self.service = DomainService()

    def create(
        self,
        domain_name: str,
        registrar: Optional[str] = None,
        auto_renew: bool = True,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        return self.service.create_domain(
            domain_name=domain_name,
            registrar=registrar,
            auto_renew=auto_renew,
            metadata=metadata,
        )

    def get(self, domain_id: str) -> Optional[Dict[str, Any]]:
        return self.service.get_domain(domain_id)

    def get_by_name(
        self,
        domain_name: str,
    ) -> Optional[Dict[str, Any]]:
        return self.service.get_by_name(domain_name)

    def list(self) -> List[Dict[str, Any]]:
        return self.service.list_domains()

    def update(
        self,
        domain_id: str,
        **fields: Any,
    ) -> Optional[Dict[str, Any]]:
        return self.service.update_domain(
            domain_id,
            **fields,
        )

    def delete(self, domain_id: str) -> bool:
        return self.service.delete_domain(domain_id)

    def exists(self, domain_id: str) -> bool:
        return self.service.exists(domain_id)

    def attach_hosting(
        self,
        domain_id: str,
        hosting_id: str,
    ) -> Optional[Dict[str, Any]]:
        return self.service.attach_hosting(
            domain_id,
            hosting_id,
        )

    def attach_server(
        self,
        domain_id: str,
        server_id: str,
    ) -> Optional[Dict[str, Any]]:
        return self.service.attach_server(
            domain_id,
            server_id,
        )

    def attach_ip(
        self,
        domain_id: str,
        ip_address_id: str,
    ) -> Optional[Dict[str, Any]]:
        return self.service.attach_ip(
            domain_id,
            ip_address_id,
        )

    def attach_ssl(
        self,
        domain_id: str,
        ssl_id: str,
    ) -> Optional[Dict[str, Any]]:
        return self.service.attach_ssl(
            domain_id,
            ssl_id,
        )

    def update_dns_status(
        self,
        domain_id: str,
        status: str,
    ) -> Optional[Dict[str, Any]]:
        return self.service.update_dns_status(
            domain_id,
            status,
        )

    def update_nameserver_status(
        self,
        domain_id: str,
        status: str,
    ) -> Optional[Dict[str, Any]]:
        return self.service.update_nameserver_status(
            domain_id,
            status,
        )
