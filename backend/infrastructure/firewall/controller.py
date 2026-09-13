"""Firewall infrastructure controller."""

from .service import FirewallService


class FirewallController:
    def __init__(self):
        self.service = FirewallService()

    def create(self, **kwargs) -> dict:
        firewall = self.service.create(**kwargs)
        return firewall.to_dict()

    def get(self, firewall_id: str) -> dict | None:
        firewall = self.service.get(firewall_id)

        if not firewall:
            return None

        return firewall.to_dict()

    def list(self) -> list[dict]:
        return [
            firewall.to_dict()
            for firewall in self.service.list_all()
        ]

    def update_status(
        self,
        firewall_id: str,
        status: str,
    ) -> dict | None:

        firewall = self.service.update_status(
            firewall_id,
            status,
        )

        if not firewall:
            return None

        return firewall.to_dict()

    def update_enabled(
        self,
        firewall_id: str,
        enabled: bool,
    ) -> dict | None:

        firewall = self.service.update_enabled(
            firewall_id,
            enabled,
        )

        if not firewall:
            return None

        return firewall.to_dict()

    def delete(self, firewall_id: str) -> bool:
        return self.service.delete(firewall_id)
