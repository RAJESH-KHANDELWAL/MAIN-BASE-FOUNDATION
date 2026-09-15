from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class CreationUniverse:
    universe_id: str
    name: str
    description: str = ""
    source_type: str = "GAME"
    status: str = "DRAFT"
    created_at: str = field(default_factory=_now)
    updated_at: str = field(default_factory=_now)

    def to_dict(self):
        return {
            "universe_id": self.universe_id,
            "name": self.name,
            "description": self.description,
            "source_type": self.source_type,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


@dataclass
class UniverseCharacter:
    character_id: str
    universe_id: str
    name: str
    description: str = ""
    role: str = ""
    asset_reference: Optional[str] = None
    created_at: str = field(default_factory=_now)

    def to_dict(self):
        return {
            "character_id": self.character_id,
            "universe_id": self.universe_id,
            "name": self.name,
            "description": self.description,
            "role": self.role,
            "asset_reference": self.asset_reference,
            "created_at": self.created_at,
        }


@dataclass
class UniverseLocation:
    location_id: str
    universe_id: str
    name: str
    description: str = ""
    asset_reference: Optional[str] = None
    created_at: str = field(default_factory=_now)

    def to_dict(self):
        return {
            "location_id": self.location_id,
            "universe_id": self.universe_id,
            "name": self.name,
            "description": self.description,
            "asset_reference": self.asset_reference,
            "created_at": self.created_at,
        }


@dataclass
class UniverseStory:
    story_id: str
    universe_id: str
    title: str
    synopsis: str = ""
    story_data: str = ""
    created_at: str = field(default_factory=_now)

    def to_dict(self):
        return {
            "story_id": self.story_id,
            "universe_id": self.universe_id,
            "title": self.title,
            "synopsis": self.synopsis,
            "story_data": self.story_data,
            "created_at": self.created_at,
        }


@dataclass
class UniverseAsset:
    asset_id: str
    universe_id: str
    asset_type: str
    name: str
    source_reference: Optional[str] = None
    file_url: Optional[str] = None
    created_at: str = field(default_factory=_now)

    def to_dict(self):
        return {
            "asset_id": self.asset_id,
            "universe_id": self.universe_id,
            "asset_type": self.asset_type,
            "name": self.name,
            "source_reference": self.source_reference,
            "file_url": self.file_url,
            "created_at": self.created_at,
        }
