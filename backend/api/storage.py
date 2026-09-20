"""MAIN BASE FOUNDATION — CENTRAL AI STORAGE API."""

from typing import Any, Dict, Optional

from backend.engines.storage import StorageEngine


class StorageAPI:
    """API facade for the Central AI Storage Engine."""

    def __init__(self):
        self.engine = StorageEngine()

    # ---------------------------------------------------------
    # ENGINE
    # ---------------------------------------------------------

    def status(self) -> dict:
        return self.engine.status()

    def health(self) -> dict:
        return self.engine.health()

    def configuration(self) -> dict:
        return self.engine.configuration()

    def connect(self) -> dict:
        return self.engine.connect()

    def disconnect(self) -> dict:
        return self.engine.disconnect()

    # ---------------------------------------------------------
    # ASSETS
    # ---------------------------------------------------------

    def register_asset(
        self,
        owner_id: str,
        area_id: str,
        title: str,
        asset_type: str = "FILE",
        workspace_id: Optional[str] = None,
        mime_type: Optional[str] = None,
        storage_key: Optional[str] = None,
        file_url: Optional[str] = None,
        content_class: Optional[str] = None,
        metadata: str = "",
    ) -> Dict[str, Any]:

        return self.engine.register_asset(
            owner_id=owner_id,
            area_id=area_id,
            title=title,
            asset_type=asset_type,
            workspace_id=workspace_id,
            mime_type=mime_type,
            storage_key=storage_key,
            file_url=file_url,
            content_class=content_class,
            metadata=metadata,
        )

    def get_asset(
        self,
        asset_id: str,
    ) -> Optional[Dict[str, Any]]:

        return self.engine.get_asset(asset_id)

    # ---------------------------------------------------------
    # PERMISSIONS
    # ---------------------------------------------------------

    def grant_access(
        self,
        asset_id: str,
        principal_id: str,
        action: str,
        granted_by: str,
    ) -> Dict[str, Any]:

        return self.engine.grant_access(
            asset_id=asset_id,
            principal_id=principal_id,
            action=action,
            granted_by=granted_by,
        )

    def revoke_access(
        self,
        asset_id: str,
        principal_id: str,
        action: str,
    ) -> bool:

        return self.engine.revoke_access(
            asset_id=asset_id,
            principal_id=principal_id,
            action=action,
        )

    def can_access(
        self,
        asset_id: str,
        principal_id: str,
        action: str,
    ) -> bool:

        return self.engine.can_access(
            asset_id=asset_id,
            principal_id=principal_id,
            action=action,
        )

    # ---------------------------------------------------------
    # ASSET OPERATIONS
    # ---------------------------------------------------------

    def move_asset(
        self,
        asset_id: str,
        target_area: str,
        actor_id: str,
    ) -> Dict[str, Any]:

        return self.engine.move_asset(
            asset_id=asset_id,
            target_area=target_area,
            actor_id=actor_id,
        )

    def set_lock(
        self,
        asset_id: str,
        locked: bool,
        actor_id: str,
    ) -> Dict[str, Any]:

        return self.engine.set_lock(
            asset_id=asset_id,
            locked=locked,
            actor_id=actor_id,
        )

    def delete_asset(
        self,
        asset_id: str,
        actor_id: str,
    ) -> Dict[str, Any]:

        return self.engine.delete_asset(
            asset_id=asset_id,
            actor_id=actor_id,
        )

    def restore_asset(
        self,
        asset_id: str,
        actor_id: str,
    ) -> Dict[str, Any]:

        return self.engine.restore_asset(
            asset_id=asset_id,
            actor_id=actor_id,
        )
