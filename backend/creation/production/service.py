from typing import Dict, List, Optional

from .model import (
    Production,
    ProductionAsset,
    ProductionScene,
    ProductionStage,
)


class ProductionService:

    def __init__(self):
        self._productions: Dict[str, Production] = {}
        self._assets: Dict[str, ProductionAsset] = {}
        self._scenes: Dict[str, ProductionScene] = {}

        self._production_counter = 0
        self._asset_counter = 0
        self._scene_counter = 0

    def _production_id(self):
        self._production_counter += 1
        return f"PRD-{self._production_counter:06d}"

    def _asset_id(self):
        self._asset_counter += 1
        return f"AST-{self._asset_counter:06d}"

    def _scene_id(self):
        self._scene_counter += 1
        return f"SCN-{self._scene_counter:06d}"

    def create_production(
        self,
        creation_id: str,
        title: str,
        production_type: str,
    ):
        production = Production(
            production_id=self._production_id(),
            creation_id=creation_id,
            title=title,
            production_type=production_type,
        )

        self._productions[production.production_id] = production
        return production

    def get_production(
        self,
        production_id: str,
    ) -> Optional[Production]:
        return self._productions.get(production_id)

    def list_productions(self) -> List[Production]:
        return list(self._productions.values())

    def set_stage(
        self,
        production_id: str,
        stage: ProductionStage,
    ):
        production = self.get_production(production_id)

        if production is None:
            return None

        production.stage = stage
        return production

    def set_script(
        self,
        production_id: str,
        script: str,
    ):
        production = self.get_production(production_id)

        if production is None:
            return None

        production.script = script
        production.stage = ProductionStage.SCRIPT

        return production

    def add_scene(
        self,
        production_id: str,
        title: str,
        description: str = "",
    ):
        production = self.get_production(production_id)

        if production is None:
            return None

        scene = ProductionScene(
            scene_id=self._scene_id(),
            scene_number=len(production.scenes) + 1,
            title=title,
            description=description,
        )

        self._scenes[scene.scene_id] = scene
        production.scenes.append(scene.scene_id)

        return scene

    def add_asset(
        self,
        production_id: str,
        asset_type: str,
        name: str,
        source_url: Optional[str] = None,
        metadata: Optional[dict] = None,
    ):
        production = self.get_production(production_id)

        if production is None:
            return None

        asset = ProductionAsset(
            asset_id=self._asset_id(),
            asset_type=asset_type,
            name=name,
            source_url=source_url,
            metadata=metadata or {},
        )

        self._assets[asset.asset_id] = asset
        production.assets.append(asset.asset_id)

        return asset

    def get_scene(self, scene_id: str):
        return self._scenes.get(scene_id)

    def get_asset(self, asset_id: str):
        return self._assets.get(asset_id)
