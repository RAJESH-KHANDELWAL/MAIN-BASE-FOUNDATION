"""Backup infrastructure controller."""

from .service import BackupService


class BackupController:
    def __init__(self):
        self.service = BackupService()

    def create(self, **kwargs) -> dict:
        backup = self.service.create(**kwargs)
        return backup.to_dict()

    def get(self, backup_id: str) -> dict | None:
        backup = self.service.get(backup_id)

        if not backup:
            return None

        return backup.to_dict()

    def list(self) -> list[dict]:
        return [
            backup.to_dict()
            for backup in self.service.list_all()
        ]

    def update_status(
        self,
        backup_id: str,
        status: str,
    ) -> dict | None:

        backup = self.service.update_status(
            backup_id,
            status,
        )

        if not backup:
            return None

        return backup.to_dict()

    def update_size(
        self,
        backup_id: str,
        size_gb: float,
    ) -> dict | None:

        backup = self.service.update_size(
            backup_id,
            size_gb,
        )

        if not backup:
            return None

        return backup.to_dict()

    def delete(self, backup_id: str) -> bool:
        return self.service.delete(backup_id)
