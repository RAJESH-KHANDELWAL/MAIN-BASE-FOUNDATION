"""Hosting infrastructure service."""

from __future__ import annotations

from datetime import datetime, timezone

from backend.database.controller import DatabaseController

from .model import HostingInfo


class HostingService:
    def __init__(self):
        self.database = DatabaseController()
        self.initialize()

    def initialize(self) -> None:
        self.database.execute(
            """
            CREATE TABLE IF NOT EXISTS hosting (
                hosting_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                hosting_type TEXT NOT NULL,
                server_id TEXT DEFAULT '',
                domain TEXT DEFAULT '',
                provider TEXT DEFAULT '',
                plan TEXT DEFAULT '',
                storage_gb REAL DEFAULT 0,
                bandwidth_gb REAL DEFAULT 0,
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
        hosting_type: str,
        server_id: str = "",
        domain: str = "",
        provider: str = "",
        plan: str = "",
        storage_gb: float = 0,
        bandwidth_gb: float = 0,
        status: str = "PLANNED",
        description: str = "",
    ) -> HostingInfo:

        timestamp = datetime.now(timezone.utc).isoformat()

        row = self.database.fetchone(
            """
            SELECT COUNT(*) AS total
            FROM hosting
            """
        )

        number = int(row["total"]) + 1 if row else 1
        hosting_id = f"HOST-{number:06d}"

        self.database.execute(
            """
            INSERT INTO hosting (
                hosting_id,
                name,
                hosting_type,
                server_id,
                domain,
                provider,
                plan,
                storage_gb,
                bandwidth_gb,
                status,
                description,
                created_at,
                updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                hosting_id,
                name,
                hosting_type,
                server_id,
                domain,
                provider,
                plan,
                storage_gb,
                bandwidth_gb,
                status,
                description,
                timestamp,
                timestamp,
            ),
        )

        return HostingInfo(
            hosting_id=hosting_id,
            name=name,
            hosting_type=hosting_type,
            server_id=server_id,
            domain=domain,
            provider=provider,
            plan=plan,
            storage_gb=storage_gb,
            bandwidth_gb=bandwidth_gb,
            status=status,
            description=description,
            created_at=timestamp,
            updated_at=timestamp,
        )

    def get(self, hosting_id: str) -> HostingInfo | None:
        row = self.database.fetchone(
            """
            SELECT *
            FROM hosting
            WHERE hosting_id = ?
            """,
            (hosting_id,),
        )

        if not row:
            return None

        return HostingInfo(**dict(row))

    def list_all(self) -> list[HostingInfo]:
        rows = self.database.fetchall(
            """
            SELECT *
            FROM hosting
            ORDER BY created_at DESC
            """
        )

        return [
            HostingInfo(**dict(row))
            for row in rows
        ]

    def update_status(
        self,
        hosting_id: str,
        status: str,
    ) -> HostingInfo | None:

        timestamp = datetime.now(timezone.utc).isoformat()

        self.database.execute(
            """
            UPDATE hosting
            SET status = ?,
                updated_at = ?
            WHERE hosting_id = ?
            """,
            (
                status,
                timestamp,
                hosting_id,
            ),
        )

        return self.get(hosting_id)

    def delete(self, hosting_id: str) -> bool:
        row = self.database.fetchone(
            """
            SELECT hosting_id
            FROM hosting
            WHERE hosting_id = ?
            """,
            (hosting_id,),
        )

        if not row:
            return False

        self.database.execute(
            """
            DELETE FROM hosting
            WHERE hosting_id = ?
            """,
            (hosting_id,),
        )

        return True
