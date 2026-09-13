"""IP Address Management controller."""

from .service import IPAddressService


class IPAddressController:
    def __init__(self):
        self.service = IPAddressService()

    def create(self, **kwargs) -> dict:
        ip = self.service.create(**kwargs)
        return ip.to_dict()

    def get(self, ip_id: str) -> dict | None:
        ip = self.service.get(ip_id)

        if not ip:
            return None

        return ip.to_dict()

    def get_by_address(self, address: str) -> dict | None:
        ip = self.service.get_by_address(address)

        if not ip:
            return None

        return ip.to_dict()

    def list(self) -> list[dict]:
        return [
            ip.to_dict()
            for ip in self.service.list_all()
        ]

    def update_status(
        self,
        ip_id: str,
        status: str,
    ) -> dict | None:

        ip = self.service.update_status(
            ip_id,
            status,
        )

        if not ip:
            return None

        return ip.to_dict()

    def update_allocation(
        self,
        ip_id: str,
        allocation_type: str,
        server_id: str = "",
    ) -> dict | None:

        ip = self.service.update_allocation(
            ip_id,
            allocation_type,
            server_id,
        )

        if not ip:
            return None

        return ip.to_dict()

    def delete(self, ip_id: str) -> bool:
        return self.service.delete(ip_id)
