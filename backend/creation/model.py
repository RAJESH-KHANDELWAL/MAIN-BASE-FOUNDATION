from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Optional


class CreationType(str, Enum):
    MOVIE = "MOVIE"
    VIDEO = "VIDEO"
    GAME = "GAME"
    PHOTO = "PHOTO"
    MUSIC = "MUSIC"
    DESIGN = "DESIGN"
    SOFTWARE = "SOFTWARE"
    OTHER = "OTHER"


class CreationStatus(str, Enum):
    DRAFT = "DRAFT"
    IN_PRODUCTION = "IN_PRODUCTION"
    COMPLETED = "COMPLETED"
    PUBLISHED = "PUBLISHED"
    ARCHIVED = "ARCHIVED"


@dataclass
class Creation:
    creation_id: str
    creation_type: CreationType
    title: str
    description: str = ""
    status: CreationStatus = CreationStatus.DRAFT
    owner_id: Optional[str] = None
    project_id: Optional[str] = None
    created_at: str = field(
        default_factory=lambda:
        datetime.now(timezone.utc).isoformat()
    )
    updated_at: str = field(
        default_factory=lambda:
        datetime.now(timezone.utc).isoformat()
    )

    def to_dict(self):
        return {
            "creation_id": self.creation_id,
            "creation_type": self.creation_type.value,
            "title": self.title,
            "description": self.description,
            "status": self.status.value,
            "owner_id": self.owner_id,
            "project_id": self.project_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
