"""Backup infrastructure service."""

from __future__ import annotations

from datetime import datetime, timezone

from backend.database.controller import DatabaseController

from .model import BackupInfo


class BackupService:
    def __init__(self):
        self.database = DatabaseController()
        self.initialize()

    def initialize(self) -> None:
        self.database.execute(
            """
            CREATE TABLE IF NOT EXISTS backups (
                backup_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                backup_type TEXT NOT NULL,
                source_type TEXT DEFAULT '',
                source_id TEXT DEFAULT '',
                storage_id TEXT DEFAULT '',
                provider TEXT DEFAULT '',
                size_gb REAL DEFAULT 0,
                status TEXT DEFAULT 'PLANNED',
                retention_days INTEGER DEFAULT 30,
                encrypted INTEGER DEFAULT 1,
                description TEXT DEFAULT '',
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )

    def create(
        self,
        name: str,
        backup_type: str,
        source_type: str = "",
        source_id: str = "",
        storage_id: str = "",
        provider: str = "",
        size_gb: float = 0,
        status: str = "PLANNED",
        retention_days: int = 30,
        encrypted: bool = True,
        description: str = "",
    ) -> BackupInfo:

        timestamp = datetime.now(timezone.utc).isoformat()

        row = self.database.fetchone(
            """
            SELECT COUNT(*) AS total
            FROM backups
            """
        )

        number = int(row["total"]) + 1 if row else 1
        backup_id = f"BKP-{number:06d}"

        self.database.execute(
            """
            INSERT INTO backups (
                backup_id,
                name,
                backup_type,
                source_type,
                source_id,
                storage_id,
                provider,
                size_gb,
                status,
                retention_days,
                encrypted,
                description,
                created_at,
                updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                backup_id,
                name,
                backup_type,
                source_type,
                source_id,
                storage_id,
                provider,
                size_gb,
                status,
                retention_days,
                int(encrypted),
                description,
                timestamp,
                timestamp,
            ),
        )

        return BackupInfo(
            backup_id=backup_id,
            name=name,
            backup_type=backup_type,
            source_type=source_type,
            source_id=source_id,
            storage_id=storage_id,
            provider=provider,
            size_gb=size_gb,
            status=status,
            retention_days=retention_days,
            encrypted=encrypted,
            description=description,
            created_at=timestamp,
            updated_at=timestamp,
        )

    def get(self, backup_id: str) -> BackupInfo | None:
        row = self.database.fetchone(
            """
            SELECT *
            FROM backups
            WHERE backup_id = ?
            """,
            (backup_id,),
        )

        if not row:
            return None

        data = dict(row)
        data["encrypted"] = bool(data["encrypted"])

        return BackupInfo(**data)

    def list_all(self) -> list[BackupInfo]:
        rows = self.database.fetchall(
            """
            SELECT *
            FROM backups
            ORDER BY created_at DESC
            """
        )

        result = []

        for row in rows:
            data = dict(row)
            data["encrypted"] = bool(data["encrypted"])

            result.append(
                BackupInfo(**data)
            )

        return result

    def update_status(
        self,
        backup_id: str,
        status: str,
    ) -> BackupInfo | None:

        timestamp = datetime.now(timezone.utc).isoformat()

        self.database.execute(
            """
            UPDATE backups
            SET status = ?,
                updated_at = ?
            WHERE backup_id = ?
            """,
            (
                status,
                timestamp,
                backup_id,
            ),
        )

        return self.get(backup_id)

    def update_size(
        self,
        backup_id: str,
        size_gb: float,
    ) -> BackupInfo | None:

        timestamp = datetime.now(timezone.utc).isoformat()

        self.database.execute(
            """
            UPDATE backups
            SET size_gb = ?,
                updated_at = ?
            WHERE backup_id = ?
            """,
            (
                size_gb,
                timestamp,
                backup_id,
            ),
        )

        return self.get(backup_id)

    def delete(self, backup_id: str) -> bool:
        row = self.database.fetchone(
            """
            SELECT backup_id
            FROM backups
            WHERE backup_id = ?
            """,
            (backup_id,),
        )

        if not row:
            return False

        self.database.execute(
            """
            DELETE FROM backups
            WHERE backup_id = ?
            """,
            (backup_id,),
        )

        return True
