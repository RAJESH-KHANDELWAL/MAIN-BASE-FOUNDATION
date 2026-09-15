from .model import ProductionStage
from .service import ProductionService


class ProductionController:

    def __init__(self):
        self.service = ProductionService()

    def create_production(
        self,
        creation_id,
        title,
        production_type,
    ):
        return self.service.create_production(
            creation_id,
            title,
            production_type,
        ).to_dict()

    def get_production(self, production_id):
        item = self.service.get_production(production_id)
        return item.to_dict() if item else None

    def list_productions(self):
        return [
            item.to_dict()
            for item in self.service.list_productions()
        ]

    def set_stage(self, production_id, stage):
        item = self.service.set_stage(
            production_id,
            ProductionStage(stage),
        )
        return item.to_dict() if item else None

    def set_script(self, production_id, script):
        item = self.service.set_script(
            production_id,
            script,
        )
        return item.to_dict() if item else None

    def add_scene(
        self,
        production_id,
        title,
        description="",
    ):
        item = self.service.add_scene(
            production_id,
            title,
            description,
        )
        return item.to_dict() if item else None

    def add_asset(
        self,
        production_id,
        asset_type,
        name,
        source_url=None,
        metadata=None,
    ):
        item = self.service.add_asset(
            production_id,
            asset_type,
            name,
            source_url,
            metadata,
        )
        return item.to_dict() if item else None
