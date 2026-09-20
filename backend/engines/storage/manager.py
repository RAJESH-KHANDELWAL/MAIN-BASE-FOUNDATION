"""MAIN BASE FOUNDATION — CENTRAL AI STORAGE ENGINE."""

from datetime import datetime, timezone
from typing import Any, Dict, Optional
from uuid import uuid4
import json

from backend.database.service import DatabaseService
from backend.engines.base import BaseEngine


class StorageEngine(BaseEngine):
    """
    CENTRAL AI STORAGE ENGINE

    MAIN-BASE-FOUNDATION ka central storage registry.

    Mukti Mahal, Business, Company, Project, Android,
    Web aur future modules isi central engine ko use kar sakte hain.

    Security model:

        AUTHENTICATED ACTOR
                ↓
        AI STORAGE ENGINE
                ↓
        OWNER / ACCESS CONTROL
                ↓
        AUDIT
    """

    ACTIONS = (
        "VIEW",
        "EDIT",
        "SHARE",
        "MOVE",
        "COPY",
        "DOWNLOAD",
        "DELETE",
        "RESTORE",
        "LOCK",
    )

    CONTENT_CLASSES = (
        "GENERAL",
        "DOCUMENT",
        "MEDIA_IMAGE",
        "MEDIA_VIDEO",
        "MEDIA_AUDIO",
        "ADULT_RESTRICTED",
        "PRIVATE_RESTRICTED",
        "CONFIDENTIAL",
    )

    def __init__(self):
        super().__init__("AI Storage Engine")

        self.database = DatabaseService()

        self.storage_status = "READY"
        self.storage_type = "ABSTRACT"
        self.connected = False

        self.initialize()

    # =========================================================
    # CORE
    # =========================================================

    @staticmethod
    def _now() -> str:
        return datetime.now(timezone.utc).isoformat()

    @staticmethod
    def _normalise_actor(actor_id: str) -> str:
        actor = str(actor_id or "").strip()

        if not actor:
            raise PermissionError(
                "Authenticated actor is required."
            )

        return actor

    @staticmethod
    def _normalise_content_class(
        content_class: Optional[str],
    ) -> Optional[str]:

        if content_class is None:
            return None

        value = str(content_class).strip().upper()

        if not value:
            return None

        if value not in StorageEngine.CONTENT_CLASSES:
            raise ValueError(
                f"Unsupported content class: {value}"
            )

        return value

    @staticmethod
    def _metadata_to_string(
        metadata: Any,
    ) -> str:

        if metadata is None:
            return ""

        if isinstance(metadata, str):
            return metadata

        return json.dumps(
            metadata,
            ensure_ascii=False,
            default=str,
        )

    def initialize(self) -> None:

        self.database.initialize()

        self.database.execute(
            """
            CREATE TABLE IF NOT EXISTS ai_store_assets (
                asset_id TEXT PRIMARY KEY,
                owner_id TEXT NOT NULL,
                workspace_id TEXT,
                area_id TEXT NOT NULL,
                title TEXT NOT NULL,
                asset_type TEXT NOT NULL,
                content_class TEXT NOT NULL DEFAULT 'GENERAL',
                mime_type TEXT,
                storage_key TEXT,
                file_url TEXT,
                metadata TEXT,
                locked INTEGER NOT NULL DEFAULT 0,
                deleted INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )

        self.database.execute(
            """
            CREATE TABLE IF NOT EXISTS ai_store_access (
                asset_id TEXT NOT NULL,
                principal_id TEXT NOT NULL,
                action TEXT NOT NULL,
                allowed INTEGER NOT NULL DEFAULT 1,
                granted_by TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                PRIMARY KEY (
                    asset_id,
                    principal_id,
                    action
                )
            )
            """
        )

        self.database.execute(
            """
            CREATE TABLE IF NOT EXISTS ai_store_links (
                asset_id TEXT NOT NULL,
                area_id TEXT NOT NULL,
                linked_by TEXT NOT NULL,
                created_at TEXT NOT NULL,
                PRIMARY KEY (
                    asset_id,
                    area_id
                )
            )
            """
        )

        self.database.execute(
            """
            CREATE TABLE IF NOT EXISTS ai_store_audit (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                asset_id TEXT NOT NULL,
                actor_id TEXT,
                action TEXT NOT NULL,
                source_area TEXT,
                target_area TEXT,
                created_at TEXT NOT NULL
            )
            """
        )

    # =========================================================
    # AI CLASSIFICATION
    # =========================================================

    @staticmethod
    def classify(
        mime_type: Optional[str],
        title: str,
        content_class: Optional[str] = None,
    ) -> str:

        supplied = StorageEngine._normalise_content_class(
            content_class
        )

        if supplied:
            return supplied

        mime = (mime_type or "").lower()
        name = (title or "").lower()

        if mime.startswith("image/"):
            return "MEDIA_IMAGE"

        if mime.startswith("video/"):
            return "MEDIA_VIDEO"

        if mime.startswith("audio/"):
            return "MEDIA_AUDIO"

        if (
            "pdf" in mime
            or name.endswith(
                (
                    ".pdf",
                    ".doc",
                    ".docx",
                    ".txt",
                    ".xls",
                    ".xlsx",
                    ".csv",
                )
            )
        ):
            return "DOCUMENT"

        return "GENERAL"

    # =========================================================
    # REGISTER ASSET
    # =========================================================

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
        metadata: Any = None,
    ) -> Dict[str, Any]:

        owner_id = self._normalise_actor(owner_id)

        if not area_id:
            raise ValueError(
                "Storage area is required."
            )

        if not title:
            raise ValueError(
                "Asset title is required."
            )

        asset_id = f"AST-{uuid4().hex.upper()}"

        now = self._now()

        classification = self.classify(
            mime_type,
            title,
            content_class,
        )

        metadata_text = self._metadata_to_string(
            metadata
        )

        self.database.execute(
            """
            INSERT INTO ai_store_assets (
                asset_id,
                owner_id,
                workspace_id,
                area_id,
                title,
                asset_type,
                content_class,
                mime_type,
                storage_key,
                file_url,
                metadata,
                created_at,
                updated_at
            )
            VALUES (
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
            )
            """,
            (
                asset_id,
                owner_id,
                workspace_id,
                area_id,
                title,
                asset_type.upper(),
                classification,
                mime_type,
                storage_key,
                file_url,
                metadata_text,
                now,
                now,
            ),
        )

        # OWNER = FULL CONTROL
        for action in self.ACTIONS:
            self.grant_access(
                asset_id=asset_id,
                principal_id=owner_id,
                action=action,
                granted_by=owner_id,
            )

        self.link_asset(
            asset_id=asset_id,
            area_id=area_id,
            actor_id=owner_id,
        )

        self._audit(
            asset_id=asset_id,
            actor_id=owner_id,
            action="CREATE",
            source_area=None,
            target_area=area_id,
        )

        return self.get_asset(asset_id)

    # =========================================================
    # GET ASSET
    # =========================================================

    def get_asset(
        self,
        asset_id: str,
        actor_id: Optional[str] = None,
        action: str = "VIEW",
    ) -> Optional[Dict[str, Any]]:

        asset = self.database.fetchone(
            """
            SELECT *
            FROM ai_store_assets
            WHERE asset_id = ?
            LIMIT 1
            """,
            (asset_id,),
        )

        if not asset:
            return None

        result = dict(asset)

        if actor_id is not None:
            actor_id = self._normalise_actor(actor_id)

            if not self.can_access(
                asset_id,
                actor_id,
                action,
            ):
                raise PermissionError(
                    f"{action.upper()} permission denied."
                )

            self._audit(
                asset_id=asset_id,
                actor_id=actor_id,
                action=action.upper(),
                source_area=result.get("area_id"),
                target_area=None,
            )

        return result

    # =========================================================
    # ACCESS CONTROL
    # =========================================================

    def grant_access(
        self,
        asset_id: str,
        principal_id: str,
        action: str,
        granted_by: str,
    ) -> Dict[str, Any]:

        principal_id = self._normalise_actor(
            principal_id
        )

        granted_by = self._normalise_actor(
            granted_by
        )

        action = action.upper()

        if action not in self.ACTIONS:
            raise ValueError(
                f"Unsupported storage action: {action}"
            )

        asset = self.get_asset(asset_id)

        if not asset:
            raise ValueError(
                "Asset not found."
            )

        # Only owner or already authorised SHARE actor
        # may grant access.
        if asset["owner_id"] != granted_by:

            if not self.can_access(
                asset_id,
                granted_by,
                "SHARE",
            ):
                raise PermissionError(
                    "SHARE permission denied."
                )

        now = self._now()

        existing = self.database.fetchone(
            """
            SELECT created_at
            FROM ai_store_access
            WHERE asset_id = ?
            AND principal_id = ?
            AND action = ?
            LIMIT 1
            """,
            (
                asset_id,
                principal_id,
                action,
            ),
        )

        created_at = (
            existing["created_at"]
            if existing
            else now
        )

        self.database.execute(
            """
            INSERT OR REPLACE INTO ai_store_access (
                asset_id,
                principal_id,
                action,
                allowed,
                granted_by,
                created_at,
                updated_at
            )
            VALUES (?, ?, ?, 1, ?, ?, ?)
            """,
            (
                asset_id,
                principal_id,
                action,
                granted_by,
                created_at,
                now,
            ),
        )

        self._audit(
            asset_id=asset_id,
            actor_id=granted_by,
            action="GRANT_" + action,
            source_area=None,
            target_area=None,
        )

        return {
            "asset_id": asset_id,
            "principal_id": principal_id,
            "action": action,
            "allowed": True,
            "granted_by": granted_by,
        }

    def revoke_access(
        self,
        asset_id: str,
        principal_id: str,
        action: str,
        actor_id: Optional[str] = None,
    ) -> bool:

        action = action.upper()

        asset = self.get_asset(asset_id)

        if not asset:
            raise ValueError(
                "Asset not found."
            )

        if actor_id is not None:

            actor_id = self._normalise_actor(
                actor_id
            )

            if asset["owner_id"] != actor_id:

                if not self.can_access(
                    asset_id,
                    actor_id,
                    "SHARE",
                ):
                    raise PermissionError(
                        "SHARE permission denied."
                    )

        self.database.execute(
            """
            UPDATE ai_store_access
            SET allowed = 0,
                updated_at = ?
            WHERE asset_id = ?
            AND principal_id = ?
            AND action = ?
            """,
            (
                self._now(),
                asset_id,
                principal_id,
                action,
            ),
        )

        return True

    def can_access(
        self,
        asset_id: str,
        principal_id: str,
        action: str,
    ) -> bool:

        principal_id = self._normalise_actor(
            principal_id
        )

        asset = self.get_asset(asset_id)

        if not asset:
            return False

        if int(asset["deleted"]) == 1:
            return False

        action = action.upper()

        if action not in self.ACTIONS:
            return False

        # OWNER ALWAYS HAS CONTROL
        if asset["owner_id"] == principal_id:
            return True

        row = self.database.fetchone(
            """
            SELECT allowed
            FROM ai_store_access
            WHERE asset_id = ?
            AND principal_id = ?
            AND action = ?
            LIMIT 1
            """,
            (
                asset_id,
                principal_id,
                action,
            ),
        )

        return bool(
            row
            and int(row["allowed"]) == 1
        )

    # =========================================================
    # CENTRAL LINKS
    # =========================================================

    def link_asset(
        self,
        asset_id: str,
        area_id: str,
        actor_id: str,
    ) -> None:

        actor_id = self._normalise_actor(
            actor_id
        )

        asset = self.get_asset(asset_id)

        if not asset:
            raise ValueError(
                "Asset not found."
            )

        if asset["owner_id"] != actor_id:

            if not self.can_access(
                asset_id,
                actor_id,
                "SHARE",
            ):
                raise PermissionError(
                    "SHARE permission denied."
                )

        self.database.execute(
            """
            INSERT OR IGNORE INTO ai_store_links (
                asset_id,
                area_id,
                linked_by,
                created_at
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                asset_id,
                area_id,
                actor_id,
                self._now(),
            ),
        )

    # =========================================================
    # MOVE
    # =========================================================

    def move_asset(
        self,
        asset_id: str,
        target_area: str,
        actor_id: str,
    ) -> Dict[str, Any]:

        actor_id = self._normalise_actor(
            actor_id
        )

        if not self.can_access(
            asset_id,
            actor_id,
            "MOVE",
        ):
            raise PermissionError(
                "MOVE permission denied."
            )

        asset = self.get_asset(asset_id)

        if not asset:
            raise ValueError(
                "Asset not found."
            )

        if int(asset["locked"]) == 1:
            raise PermissionError(
                "Asset is locked."
            )

        source_area = asset["area_id"]

        self.database.execute(
            """
            UPDATE ai_store_assets
            SET area_id = ?,
                updated_at = ?
            WHERE asset_id = ?
            """,
            (
                target_area,
                self._now(),
                asset_id,
            ),
        )

        self.link_asset(
            asset_id=asset_id,
            area_id=target_area,
            actor_id=actor_id,
        )

        self._audit(
            asset_id=asset_id,
            actor_id=actor_id,
            action="MOVE",
            source_area=source_area,
            target_area=target_area,
        )

        return self.get_asset(asset_id)

    # =========================================================
    # LOCK
    # =========================================================

    def set_lock(
        self,
        asset_id: str,
        locked: bool,
        actor_id: str,
    ) -> Dict[str, Any]:

        actor_id = self._normalise_actor(
            actor_id
        )

        if not self.can_access(
            asset_id,
            actor_id,
            "LOCK",
        ):
            raise PermissionError(
                "LOCK permission denied."
            )

        self.database.execute(
            """
            UPDATE ai_store_assets
            SET locked = ?,
                updated_at = ?
            WHERE asset_id = ?
            """,
            (
                int(locked),
                self._now(),
                asset_id,
            ),
        )

        self._audit(
            asset_id=asset_id,
            actor_id=actor_id,
            action="LOCK" if locked else "UNLOCK",
            source_area=None,
            target_area=None,
        )

        return self.get_asset(asset_id)

    # =========================================================
    # DELETE
    # =========================================================

    def delete_asset(
        self,
        asset_id: str,
        actor_id: str,
    ) -> Dict[str, Any]:

        actor_id = self._normalise_actor(
            actor_id
        )

        if not self.can_access(
            asset_id,
            actor_id,
            "DELETE",
        ):
            raise PermissionError(
                "DELETE permission denied."
            )

        asset = self.get_asset(asset_id)

        if not asset:
            raise ValueError(
                "Asset not found."
            )

        if int(asset["locked"]) == 1:
            raise PermissionError(
                "Asset is locked."
            )

        self.database.execute(
            """
            UPDATE ai_store_assets
            SET deleted = 1,
                updated_at = ?
            WHERE asset_id = ?
            """,
            (
                self._now(),
                asset_id,
            ),
        )

        self._audit(
            asset_id=asset_id,
            actor_id=actor_id,
            action="DELETE",
            source_area=asset["area_id"],
            target_area=None,
        )

        return self.get_asset(asset_id)

    # =========================================================
    # RESTORE
    # =========================================================

    def restore_asset(
        self,
        asset_id: str,
        actor_id: str,
    ) -> Dict[str, Any]:

        actor_id = self._normalise_actor(
            actor_id
        )

        asset = self.get_asset(asset_id)

        if not asset:
            raise ValueError(
                "Asset not found."
            )

        if asset["owner_id"] != actor_id:

            if not self.can_access(
                asset_id,
                actor_id,
                "RESTORE",
            ):
                raise PermissionError(
                    "RESTORE permission denied."
                )

        self.database.execute(
            """
            UPDATE ai_store_assets
            SET deleted = 0,
                updated_at = ?
            WHERE asset_id = ?
            """,
            (
                self._now(),
                asset_id,
            ),
        )

        self._audit(
            asset_id=asset_id,
            actor_id=actor_id,
            action="RESTORE",
            source_area=asset["area_id"],
            target_area=None,
        )

        return self.get_asset(asset_id)

    # =========================================================
    # AUDIT
    # =========================================================

    def _audit(
        self,
        asset_id: str,
        actor_id: Optional[str],
        action: str,
        source_area: Optional[str],
        target_area: Optional[str],
    ) -> None:

        self.database.execute(
            """
            INSERT INTO ai_store_audit (
                asset_id,
                actor_id,
                action,
                source_area,
                target_area,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                asset_id,
                actor_id,
                action,
                source_area,
                target_area,
                self._now(),
            ),
        )

    # =========================================================
    # STATUS
    # =========================================================

    def status(self) -> Dict[str, object]:

        row = self.database.fetchone(
            """
            SELECT COUNT(*) AS count
            FROM ai_store_assets
            WHERE deleted = 0
            """
        )

        return {
            "engine": "AI Storage Engine",
            "status": self.storage_status,
            "storage_type": self.storage_type,
            "connected": self.connected,
            "central_registry": True,
            "active_assets": (
                int(row["count"])
                if row
                else 0
            ),
            "shared_across_ecosystem": True,
        }

    def health(self) -> Dict[str, object]:

        return {
            "engine": "AI Storage Engine",
            "health": "HEALTHY",
            "database_registry": "READY",
            "permissions": "READY",
            "audit_log": "READY",
            "central_engine": True,
        }

    def connect(self) -> Dict[str, object]:

        self.connected = True
        self.storage_status = "CONNECTED"

        return self.status()

    def disconnect(self) -> Dict[str, object]:

        self.connected = False
        self.storage_status = "READY"

        return self.status()

    def configuration(self) -> Dict[str, object]:

        return {
            "engine": "AI Storage Engine",
            "storage_type": self.storage_type,
            "central_registry": True,
            "cross_area_access": True,
            "permission_actions": list(
                self.ACTIONS
            ),
            "content_classes": list(
                self.CONTENT_CLASSES
            ),
            "ai_classification": True,
            "audit_logging": True,
            "soft_delete": True,
            "asset_linking": True,
            "authenticated_actor_required": True,
            "owner_control": True,
            "restricted_content_classes": [
                "ADULT_RESTRICTED",
                "PRIVATE_RESTRICTED",
                "CONFIDENTIAL",
            ],
        }
