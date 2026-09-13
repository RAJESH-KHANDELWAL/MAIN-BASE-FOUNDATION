"""Object storage infrastructure service."""

from __future__ import annotations

from datetime import datetime, timezone

from backend.database.controller import DatabaseController

from .model import ObjectStorageInfo


class ObjectStorageService:
    def __init__(self):
        self.database = DatabaseController()
        self.initialize()

    def initialize(self) -> None:
        self.database.execute(
            """
            CREATE TABLE IF NOT EXISTS object_storage (
                storage_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                storage_type TEXT NOT NULL,
                bucket_name TEXT DEFAULT '',
                region TEXT DEFAULT '',
                provider TEXT DEFAULT '',
                endpoint TEXT DEFAULT '',
                capacity_gb REAL DEFAULT 0,
                used_gb REAL DEFAULT 0,
                status TEXT DEFAULT 'PLANNED',
                public_access INTEGER DEFAULT 0,
                encryption_enabled INTEGER DEFAULT 1,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )

    def create(
        self,
        name: str,
        storage_type: str,
        bucket_name: str = "",
        region: str = "",
        provider: str = "",
        endpoint: str = "",
        capacity_gb: float = 0,
        used_gb: float = 0,
        status: str = "PLANNED",
        public_access: bool = False,
        encryption_enabled: bool = True,
    ) -> ObjectStorageInfo:

        timestamp = datetime.now(timezone.utc).isoformat()

        existing = self.database.fetchone(
            """
            SELECT storage_id
            FROM object_storage
            WHERE bucket_name = ?
              AND bucket_name != ''
            """,
            (bucket_name,),
        )

        if existing:
            raise ValueError("Object storage bucket already exists")

        row = self.database.fetchone(
            """
            SELECT COUNT(*) AS total
            FROM object_storage
            """
        )

        number = int(row["total"]) + 1 if row else 1
        storage_id = f"OBJ-{number:06d}"

        self.database.execute(
            """
            INSERT INTO object_storage (
                storage_id,
                name,
                storage_type,
                bucket_name,
                region,
                provider,
                endpoint,
                capacity_gb,
                used_gb,
                status,
                public_access,
                encryption_enabled,
                created_at,
                updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                storage_id,
                name,
                storage_type,
                bucket_name,
                region,
                provider,
                endpoint,
                capacity_gb,
                used_gb,
                status,
                int(public_access),
                int(encryption_enabled),
                timestamp,
                timestamp,
            ),
        )

        return ObjectStorageInfo(
            storage_id=storage_id,
            name=name,
            storage_type=storage_type,
            bucket_name=bucket_name,
            region=region,
            provider=provider,
            endpoint=endpoint,
            capacity_gb=capacity_gb,
            used_gb=used_gb,
            status=status,
            public_access=public_access,
            encryption_enabled=encryption_enabled,
            created_at=timestamp,
            updated_at=timestamp,
        )

    def get(self, storage_id: str) -> ObjectStorageInfo | None:
        row = self.database.fetchone(
            """
            SELECT *
            FROM object_storage
            WHERE storage_id = ?
            """,
            (storage_id,),
        )

        if not row:
            return None

        data = dict(row)
        data["public_access"] = bool(data["public_access"])
        data["encryption_enabled"] = bool(
            data["encryption_enabled"]
        )

        return ObjectStorageInfo(**data)

    def list_all(self) -> list[ObjectStorageInfo]:
        rows = self.database.fetchall(
            """
            SELECT *
            FROM object_storage
            ORDER BY created_at DESC
            """
        )

        result = []

        for row in rows:
            data = dict(row)
            data["public_access"] = bool(data["public_access"])
            data["encryption_enabled"] = bool(
                data["encryption_enabled"]
            )

            result.append(
                ObjectStorageInfo(**data)
            )

        return result

    def update_status(
        self,
        storage_id: str,
        status: str,
    ) -> ObjectStorageInfo | None:

        timestamp = datetime.now(timezone.utc).isoformat()

        self.database.execute(
            """
            UPDATE object_storage
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
    ) -> ObjectStorageInfo | None:

        timestamp = datetime.now(timezone.utc).isoformat()

        self.database.execute(
            """
            UPDATE object_storage
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

    def update_access(
        self,
        storage_id: str,
        public_access: bool,
    ) -> ObjectStorageInfo | None:

        timestamp = datetime.now(timezone.utc).isoformat()

        self.database.execute(
            """
            UPDATE object_storage
            SET public_access = ?,
                updated_at = ?
            WHERE storage_id = ?
            """,
            (
                int(public_access),
                timestamp,
                storage_id,
            ),
        )

        return self.get(storage_id)

    def delete(self, storage_id: str) -> bool:
        row = self.database.fetchone(
            """
            SELECT storage_id
            FROM object_storage
            WHERE storage_id = ?
            """,
            (storage_id,),
        )

        if not row:
            return False

        self.database.execute(
            """
            DELETE FROM object_storage
            WHERE storage_id = ?
            """,
            (storage_id,),
        )

        return True
