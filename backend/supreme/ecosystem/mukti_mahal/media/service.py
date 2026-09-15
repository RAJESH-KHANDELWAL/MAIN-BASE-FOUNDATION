"""
MUKTI MAHAL MEDIA SERVICE

Persistent media asset registry.

This service stores metadata only.
Actual files are connected through file_url/storage_key.
"""

from datetime import datetime, timezone
from typing import Optional

from backend.database.service import DatabaseService

from .model import MuktiMahalMediaAsset


class MuktiMahalMediaService:

    def __init__(self):
        self.database = DatabaseService()
        self.initialize()

    # ---------------------------------------------------------
    # COMMON
    # ---------------------------------------------------------

    @staticmethod
    def _now() -> str:
        return datetime.now(timezone.utc).isoformat()

    def _generate_id(self) -> str:

        row = self.database.fetchone(
            """
            SELECT MAX(
                CAST(SUBSTR(asset_id, 6) AS INTEGER)
            ) AS max_number
            FROM mukti_mahal_media_assets
            """
        )

        max_number = 0

        if row and row["max_number"] is not None:
            max_number = int(row["max_number"])

        return f"MED-{max_number + 1:06d}"

    # ---------------------------------------------------------
    # DATABASE
    # ---------------------------------------------------------

    def initialize(self) -> None:

        self.database.initialize()

        self.database.execute(
            """
            CREATE TABLE IF NOT EXISTS mukti_mahal_media_assets (
                asset_id TEXT PRIMARY KEY,
                mahal_id TEXT NOT NULL,
                project_id TEXT,
                division_id TEXT,
                title TEXT NOT NULL,
                asset_type TEXT NOT NULL,
                description TEXT NOT NULL DEFAULT '',
                file_url TEXT,
                storage_key TEXT,
                mime_type TEXT,
                file_size INTEGER NOT NULL DEFAULT 0,
                status TEXT NOT NULL DEFAULT 'DRAFT',
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )

    # =========================================================
    # CREATE
    # =========================================================

    def create_asset(
        self,
        mahal_id: str,
        title: str,
        asset_type: str,
        project_id: Optional[str] = None,
        division_id: Optional[str] = None,
        description: str = "",
        file_url: Optional[str] = None,
        storage_key: Optional[str] = None,
        mime_type: Optional[str] = None,
        file_size: int = 0,
        status: str = "DRAFT",
    ) -> MuktiMahalMediaAsset:

        asset_id = self._generate_id()
        now = self._now()

        self.database.execute(
            """
            INSERT INTO mukti_mahal_media_assets (
                asset_id,
                mahal_id,
                project_id,
                division_id,
                title,
                asset_type,
                description,
                file_url,
                storage_key,
                mime_type,
                file_size,
                status,
                created_at,
                updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                asset_id,
                mahal_id,
                project_id,
                division_id,
                title,
                asset_type.upper(),
                description,
                file_url,
                storage_key,
                mime_type,
                int(file_size),
                status.upper(),
                now,
                now,
            ),
        )

        return self.get_asset(asset_id)

    # =========================================================
    # GET
    # =========================================================

    def get_asset(
        self,
        asset_id: str,
    ) -> Optional[MuktiMahalMediaAsset]:

        row = self.database.fetchone(
            """
            SELECT *
            FROM mukti_mahal_media_assets
            WHERE asset_id = ?
            """,
            (asset_id,),
        )

        if not row:
            return None

        return MuktiMahalMediaAsset(**dict(row))

    # =========================================================
    # LIST
    # =========================================================

    def list_assets(
        self,
        mahal_id: Optional[str] = None,
        project_id: Optional[str] = None,
        division_id: Optional[str] = None,
        asset_type: Optional[str] = None,
        status: Optional[str] = None,
    ):

        query = """
            SELECT *
            FROM mukti_mahal_media_assets
            WHERE 1 = 1
        """

        params = []

        if mahal_id:
            query += " AND mahal_id = ?"
            params.append(mahal_id)

        if project_id:
            query += " AND project_id = ?"
            params.append(project_id)

        if division_id:
            query += " AND division_id = ?"
            params.append(division_id)

        if asset_type:
            query += " AND asset_type = ?"
            params.append(asset_type.upper())

        if status:
            query += " AND status = ?"
            params.append(status.upper())

        query += " ORDER BY created_at ASC"

        rows = self.database.fetchall(
            query,
            tuple(params),
        )

        return [
            MuktiMahalMediaAsset(**dict(row))
            for row in rows
        ]

    # =========================================================
    # UPDATE
    # =========================================================

    def update_asset(
        self,
        asset_id: str,
        title: Optional[str] = None,
        asset_type: Optional[str] = None,
        description: Optional[str] = None,
        file_url: Optional[str] = None,
        storage_key: Optional[str] = None,
        mime_type: Optional[str] = None,
        file_size: Optional[int] = None,
        status: Optional[str] = None,
        project_id: Optional[str] = None,
        division_id: Optional[str] = None,
    ) -> Optional[MuktiMahalMediaAsset]:

        current = self.get_asset(asset_id)

        if not current:
            return None

        now = self._now()

        self.database.execute(
            """
            UPDATE mukti_mahal_media_assets
            SET
                project_id = ?,
                division_id = ?,
                title = ?,
                asset_type = ?,
                description = ?,
                file_url = ?,
                storage_key = ?,
                mime_type = ?,
                file_size = ?,
                status = ?,
                updated_at = ?
            WHERE asset_id = ?
            """,
            (
                project_id
                if project_id is not None
                else current.project_id,

                division_id
                if division_id is not None
                else current.division_id,

                title
                if title is not None
                else current.title,

                asset_type.upper()
                if asset_type is not None
                else current.asset_type,

                description
                if description is not None
                else current.description,

                file_url
                if file_url is not None
                else current.file_url,

                storage_key
                if storage_key is not None
                else current.storage_key,

                mime_type
                if mime_type is not None
                else current.mime_type,

                int(file_size)
                if file_size is not None
                else current.file_size,

                status.upper()
                if status is not None
                else current.status,

                now,
                asset_id,
            ),
        )

        return self.get_asset(asset_id)

    # =========================================================
    # DELETE
    # =========================================================

    def delete_asset(
        self,
        asset_id: str,
    ) -> bool:

        current = self.get_asset(asset_id)

        if not current:
            return False

        self.database.execute(
            """
            DELETE FROM mukti_mahal_media_assets
            WHERE asset_id = ?
            """,
            (asset_id,),
        )

        return True

    # =========================================================
    # STATUS
    # =========================================================

    def status(self):

        row = self.database.fetchone(
            """
            SELECT COUNT(*) AS count
            FROM mukti_mahal_media_assets
            """
        )

        count = int(row["count"]) if row else 0

        return {
            "system": "MUKTI MAHAL MEDIA",
            "status": "LIVE",
            "asset_registry": "READY",
            "total_assets": count,
            "asset_types": [
                "PHOTO",
                "VIDEO",
                "MOVIE",
                "GAME",
                "AUDIO",
                "DESIGN",
                "SOFTWARE",
                "OTHER",
            ],
        }
