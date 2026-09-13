"""Container infrastructure controller."""

from .service import ContainerService


class ContainerController:
    def __init__(self):
        self.service = ContainerService()

    def create(self, **kwargs) -> dict:
        container = self.service.create(**kwargs)
        return container.to_dict()

    def get(self, container_id: str) -> dict | None:
        container = self.service.get(container_id)

        if not container:
            return None

        return container.to_dict()

    def list(self) -> list[dict]:
        return [
            container.to_dict()
            for container in self.service.list_all()
        ]

    def update_status(
        self,
        container_id: str,
        status: str,
    ) -> dict | None:

        container = self.service.update_status(
            container_id,
            status,
        )

        if not container:
            return None

        return container.to_dict()

    def update_replicas(
        self,
        container_id: str,
        replicas: int,
    ) -> dict | None:

        container = self.service.update_replicas(
            container_id,
            replicas,
        )

        if not container:
            return None

        return container.to_dict()

    def delete(self, container_id: str) -> bool:
        return self.service.delete(container_id)
