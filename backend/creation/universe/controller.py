from typing import Optional

from .model import (
    CreationUniverse,
    UniverseCharacter,
    UniverseLocation,
    UniverseStory,
    UniverseAsset,
)
from .service import CreationUniverseService


class CreationUniverseController:

    def __init__(self):
        self.service = CreationUniverseService()

    def create_universe(self, data: CreationUniverse):
        return data.to_dict() if self.service.create_universe(data) else None

    def get_universe(self, universe_id: str):
        item = self.service.get_universe(universe_id)
        return item.to_dict() if item else None

    def list_universes(self):
        return [item.to_dict() for item in self.service.list_universes()]

    def create_character(self, data: UniverseCharacter):
        return data.to_dict() if self.service.create_character(data) else None

    def list_characters(self, universe_id: Optional[str] = None):
        return [
            item.to_dict()
            for item in self.service.list_characters(universe_id)
        ]

    def create_location(self, data: UniverseLocation):
        return data.to_dict() if self.service.create_location(data) else None

    def list_locations(self, universe_id: Optional[str] = None):
        return [
            item.to_dict()
            for item in self.service.list_locations(universe_id)
        ]

    def create_story(self, data: UniverseStory):
        return data.to_dict() if self.service.create_story(data) else None

    def list_stories(self, universe_id: Optional[str] = None):
        return [
            item.to_dict()
            for item in self.service.list_stories(universe_id)
        ]

    def create_asset(self, data: UniverseAsset):
        return data.to_dict() if self.service.create_asset(data) else None

    def list_assets(self, universe_id: Optional[str] = None):
        return [
            item.to_dict()
            for item in self.service.list_assets(universe_id)
        ]

    def status(self):
        return self.service.status()
