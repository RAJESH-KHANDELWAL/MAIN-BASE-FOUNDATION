"""Network infrastructure controller."""

from .service import NetworkService


class NetworkController:
    def __init__(self):
        self.service = NetworkService()

    def create(self, **kwargs) -> dict:
        network = self.service.create(**kwargs)
        return network.to_dict()

    def get(self, network_id: str) -> dict | None:
        network = self.service.get(network_id)

        if not network:
            return None

        return network.to_dict()

    def list(self) -> list[dict]:
        return [
            network.to_dict()
            for network in self.service.list_all()
        ]

    def update_status(
        self,
        network_id: str,
        status: str,
    ) -> dict | None:

        network = self.service.update_status(
            network_id,
            status,
        )

        if not network:
            return None

        return network.to_dict()

    def delete(self, network_id: str) -> bool:
        return self.service.delete(network_id)
