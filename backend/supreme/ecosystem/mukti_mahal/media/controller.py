"""
MUKTI MAHAL MEDIA CONTROLLER
"""

from typing import Optional

from .service import MuktiMahalMediaService


class MuktiMahalMediaController:

    def __init__(self):
        self.service = MuktiMahalMediaService()

    def create_asset(self, **kwargs):
        return self.service.create_asset(**kwargs)

    def get_asset(self, asset_id: str):
        return self.service.get_asset(asset_id)

    def list_assets(
        self,
        mahal_id: Optional[str] = None,
        project_id: Optional[str] = None,
        division_id: Optional[str] = None,
        asset_type: Optional[str] = None,
        status: Optional[str] = None,
    ):
        return self.service.list_assets(
            mahal_id=mahal_id,
            project_id=project_id,
            division_id=division_id,
            asset_type=asset_type,
            status=status,
        )

    def update_asset(self, asset_id: str, **kwargs):
        return self.service.update_asset(
            asset_id=asset_id,
            **kwargs,
        )

    def delete_asset(self, asset_id: str):
        return self.service.delete_asset(asset_id)

    def status(self):
        return self.service.status()
