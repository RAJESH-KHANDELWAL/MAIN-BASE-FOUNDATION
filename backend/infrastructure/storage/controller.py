"""Storage infrastructure controller."""

from .service import StorageService


class StorageController:
    def __init__(self):
        self.service = StorageService()

    def create(self, **kwargs) -> dict:
        storage = self.service.create(**kwargs)
        return storage.to_dict()

    def get(self, storage_id: str) -> dict | None:
        storage = self.service.get(storage_id)

        if not storage:
            return None

        return storage.to_dict()

    def list(self) -> list[dict]:
        return [
            storage.to_dict()
            for storage in self.service.list_all()
        ]

    def update_status(
        self,
        storage_id: str,
        status: str,
    ) -> dict | None:

        storage = self.service.update_status(
            storage_id,
            status,
        )

        if not storage:
            return None

        return storage.to_dict()

    def update_usage(
        self,
        storage_id: str,
        used_gb: float,
    ) -> dict | None:

        storage = self.service.update_usage(
            storage_id,
            used_gb,
        )

        if not storage:
            return None

        return storage.to_dict()

    def delete(self, storage_id: str) -> bool:
        return self.service.delete(storage_id)
