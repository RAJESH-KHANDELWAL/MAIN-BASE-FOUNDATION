from typing import Dict, List, Optional

from .model import Creation, CreationStatus, CreationType


class CreationService:

    def __init__(self):
        self._creations: Dict[str, Creation] = {}
        self._counter = 0

    def _next_id(self) -> str:
        self._counter += 1
        return f"CRT-{self._counter:06d}"

    def create(
        self,
        creation_type: CreationType,
        title: str,
        description: str = "",
        owner_id: Optional[str] = None,
        project_id: Optional[str] = None,
    ) -> Creation:

        creation = Creation(
            creation_id=self._next_id(),
            creation_type=creation_type,
            title=title,
            description=description,
            owner_id=owner_id,
            project_id=project_id,
        )

        self._creations[creation.creation_id] = creation
        return creation

    def get(self, creation_id: str) -> Optional[Creation]:
        return self._creations.get(creation_id)

    def list(self) -> List[Creation]:
        return list(self._creations.values())

    def update_status(
        self,
        creation_id: str,
        status: CreationStatus,
    ) -> Optional[Creation]:

        creation = self.get(creation_id)

        if creation is None:
            return None

        creation.status = status
        return creation

    def delete(self, creation_id: str) -> bool:
        return self._creations.pop(creation_id, None) is not None
