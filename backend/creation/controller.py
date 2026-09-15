from typing import Optional

from .model import CreationStatus, CreationType
from .service import CreationService


class CreationController:

    def __init__(self):
        self.service = CreationService()

    def create(
        self,
        creation_type: CreationType,
        title: str,
        description: str = "",
        owner_id: Optional[str] = None,
        project_id: Optional[str] = None,
    ):
        return self.service.create(
            creation_type=creation_type,
            title=title,
            description=description,
            owner_id=owner_id,
            project_id=project_id,
        ).to_dict()

    def get(self, creation_id: str):
        creation = self.service.get(creation_id)
        return creation.to_dict() if creation else None

    def list(self):
        return [
            creation.to_dict()
            for creation in self.service.list()
        ]

    def update_status(
        self,
        creation_id: str,
        status: CreationStatus,
    ):
        creation = self.service.update_status(
            creation_id,
            status,
        )

        return creation.to_dict() if creation else None

    def delete(self, creation_id: str):
        return self.service.delete(creation_id)
