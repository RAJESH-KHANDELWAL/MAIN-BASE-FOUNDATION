from typing import Dict, List, Optional

from .model import (
    CreationUniverse,
    UniverseCharacter,
    UniverseLocation,
    UniverseStory,
    UniverseAsset,
)


class CreationUniverseService:

    def __init__(self):
        self._universes: Dict[str, CreationUniverse] = {}
        self._characters: Dict[str, UniverseCharacter] = {}
        self._locations: Dict[str, UniverseLocation] = {}
        self._stories: Dict[str, UniverseStory] = {}
        self._assets: Dict[str, UniverseAsset] = {}

    # -------------------------
    # UNIVERSE
    # -------------------------

    def create_universe(self, universe: CreationUniverse):
        self._universes[universe.universe_id] = universe
        return universe

    def get_universe(self, universe_id: str):
        return self._universes.get(universe_id)

    def list_universes(self):
        return list(self._universes.values())

    # -------------------------
    # CHARACTERS
    # -------------------------

    def create_character(self, character: UniverseCharacter):
        self._characters[character.character_id] = character
        return character

    def get_character(self, character_id: str):
        return self._characters.get(character_id)

    def list_characters(self, universe_id: Optional[str] = None):
        values = list(self._characters.values())

        if universe_id:
            values = [
                item for item in values
                if item.universe_id == universe_id
            ]

        return values

    # -------------------------
    # LOCATIONS
    # -------------------------

    def create_location(self, location: UniverseLocation):
        self._locations[location.location_id] = location
        return location

    def get_location(self, location_id: str):
        return self._locations.get(location_id)

    def list_locations(self, universe_id: Optional[str] = None):
        values = list(self._locations.values())

        if universe_id:
            values = [
                item for item in values
                if item.universe_id == universe_id
            ]

        return values

    # -------------------------
    # STORIES
    # -------------------------

    def create_story(self, story: UniverseStory):
        self._stories[story.story_id] = story
        return story

    def get_story(self, story_id: str):
        return self._stories.get(story_id)

    def list_stories(self, universe_id: Optional[str] = None):
        values = list(self._stories.values())

        if universe_id:
            values = [
                item for item in values
                if item.universe_id == universe_id
            ]

        return values

    # -------------------------
    # ASSETS
    # -------------------------

    def create_asset(self, asset: UniverseAsset):
        self._assets[asset.asset_id] = asset
        return asset

    def get_asset(self, asset_id: str):
        return self._assets.get(asset_id)

    def list_assets(self, universe_id: Optional[str] = None):
        values = list(self._assets.values())

        if universe_id:
            values = [
                item for item in values
                if item.universe_id == universe_id
            ]

        return values

    # -------------------------
    # STATUS
    # -------------------------

    def status(self):
        return {
            "status": "READY",
            "universes": len(self._universes),
            "characters": len(self._characters),
            "locations": len(self._locations),
            "stories": len(self._stories),
            "assets": len(self._assets),
        }
