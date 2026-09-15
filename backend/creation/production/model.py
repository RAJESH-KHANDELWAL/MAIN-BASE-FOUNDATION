from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import List, Optional


class ProductionStage(str, Enum):
    IDEA = "IDEA"
    SCRIPT = "SCRIPT"
    PRE_PRODUCTION = "PRE_PRODUCTION"
    PRODUCTION = "PRODUCTION"
    EDITING = "EDITING"
    AUDIO = "AUDIO"
    TESTING = "TESTING"
    FINAL = "FINAL"
    PUBLISHED = "PUBLISHED"


@dataclass
class ProductionAsset:
    asset_id: str
    asset_type: str
    name: str
    source_url: Optional[str] = None
    metadata: dict = field(default_factory=dict)

    def to_dict(self):
        return {
            "asset_id": self.asset_id,
            "asset_type": self.asset_type,
            "name": self.name,
            "source_url": self.source_url,
            "metadata": self.metadata,
        }


@dataclass
class ProductionScene:
    scene_id: str
    scene_number: int
    title: str
    description: str = ""
    assets: List[str] = field(default_factory=list)

    def to_dict(self):
        return {
            "scene_id": self.scene_id,
            "scene_number": self.scene_number,
            "title": self.title,
            "description": self.description,
            "assets": self.assets,
        }


@dataclass
class Production:
    production_id: str
    creation_id: str
    title: str
    production_type: str
    stage: ProductionStage = ProductionStage.IDEA
    script: str = ""
    scenes: List[str] = field(default_factory=list)
    assets: List[str] = field(default_factory=list)
    output_url: Optional[str] = None
    created_at: str = field(
        default_factory=lambda:
        datetime.now(timezone.utc).isoformat()
    )

    def to_dict(self):
        return {
            "production_id": self.production_id,
            "creation_id": self.creation_id,
            "title": self.title,
            "production_type": self.production_type,
            "stage": self.stage.value,
            "script": self.script,
            "scenes": self.scenes,
            "assets": self.assets,
            "output_url": self.output_url,
            "created_at": self.created_at,
        }
