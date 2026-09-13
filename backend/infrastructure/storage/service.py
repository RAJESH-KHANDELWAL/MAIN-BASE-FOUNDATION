"""Storage infrastructure service."""

from __future__ import annotations

from datetime import datetime, timezone

from backend.database.controller import DatabaseController

from .model import StorageInfo


class StorageService:
    def __init__(self):
        self.database = DatabaseController()
        self.initialize()

    def initialize(self) -> None:
        self.database.execute(
            """
            CREATE TABLE IF NOT EXISTS storage (
                storage_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                storage_type TEXT NOT NULL,
                server_id TEXT DEFAULT '',
                provider TEXT DEFAULT '',
                region TEXT DEFAULT '',
                capacity_gb REAL DEFAULT 0,
                used_gb REAL DEFAULT 0,
                status TEXT DEFAULT 'PLANNED',
                description TEXT DEFAULT '',
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )

    def create(
        self,
        name: str,
        storage_type: str,
        server_id: str = "",
        provider: str = "",
        region: str = "",
        capacity_gb: float = 0,
        used_gb: float = 0,
        status: str = "PLANNED",
        description: str = "",
    ) -> StorageInfo:

        timestamp = datetime.now(timezone.utc).isoformat()

        row = self.database.fetchone(
            """
            SELECT COUNT(*) AS total
            FROM storage
            """
        )

        number = int(row["total"]) + 1 if row else 1
        storage_id = f"STG-{number:06d}"

        self.database.execute(
            """
            INSERT INTO storage (
                storage_id,
                name,
                storage_type,
                server_id,
                provider,
                region,
                capacity_gb,
                used_gb,
                status,
                description,
                created_at,
                updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                storage_id,
                name,
                storage_type,
                server_id,
                provider,
                region,
                capacity_gb,
                used_gb,
                status,
                description,
                timestamp,
                timestamp,
            ),
        )

        return StorageInfo(
            storage_id=storage_id,
            name=name,
            storage_type=storage_type,
            server_id=server_id,
            provider=provider,
            region=region,
            capacity_gb=capacity_gb,
            used_gb=used_gb,
            status=status,
            description=description,
            created_at=timestamp,
            updated_at=timestamp,
        )

    def get(self, storage_id: str) -> StorageInfo | None:
        row = self.database.fetchone(
            """
            SELECT *
            FROM storage
            WHERE storage_id = ?
            """,
            (storage_id,),
        )

        if not row:
            return None

        return StorageInfo(**dict(row))

    def list_all(self) -> list[StorageInfo]:
        rows = self.database.fetchall(
            """
            SELECT *
            FROM storage
            ORDER BY created_at DESC
            """
        )

        return [
            StorageInfo(**dict(row))
            for row in rows
        ]

    def update_status(
        self,
        storage_id: str,
        status: str,
    ) -> StorageInfo | None:

        timestamp = datetime.now(timezone.utc).isoformat()

        self.database.execute(
            """
            UPDATE storage
            SET status = ?,
                updated_at = ?
            WHERE storage_id = ?
            """,
            (
                status,
                timestamp,
                storage_id,
            ),
        )

        return self.get(storage_id)

    def update_usage(
        self,
        storage_id: str,
        used_gb: float,
    ) -> StorageInfo | None:

        timestamp = datetime.now(timezone.utc).isoformat()

        self.database.execute(
            """
            UPDATE storage
            SET used_gb = ?,
                updated_at = ?
            WHERE storage_id = ?
            """,
            (
                used_gb,
                timestamp,
                storage_id,
            ),
        )

        return self.get(storage_id)

    def delete(self, storage_id: str) -> bool:
        row = self.database.fetchone(
            """
            SELECT storage_id
            FROM storage
            WHERE storage_id = ?
            """,
            (storage_id,),
        )

        if not row:
            return False

        self.database.execute(
            """
            DELETE FROM storage
            WHERE storage_id = ?
            """,
            (storage_id,),
        )

        return True
