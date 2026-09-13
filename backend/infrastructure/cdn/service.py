"""CDN infrastructure service."""

from __future__ import annotations

from datetime import datetime, timezone

from backend.database.controller import DatabaseController

from .model import CDNInfo


class CDNService:
    def __init__(self):
        self.database = DatabaseController()
        self.initialize()

    def initialize(self) -> None:
        self.database.execute(
            """
            CREATE TABLE IF NOT EXISTS cdn (
                cdn_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                domain TEXT NOT NULL,
                origin_server_id TEXT DEFAULT '',
                provider TEXT DEFAULT '',
                region TEXT DEFAULT '',
                status TEXT DEFAULT 'PLANNED',
                cache_enabled INTEGER DEFAULT 1,
                ssl_enabled INTEGER DEFAULT 1,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )

    def create(
        self,
        name: str,
        domain: str,
        origin_server_id: str = "",
        provider: str = "",
        region: str = "",
        status: str = "PLANNED",
        cache_enabled: bool = True,
        ssl_enabled: bool = True,
    ) -> CDNInfo:

        timestamp = datetime.now(timezone.utc).isoformat()

        row = self.database.fetchone(
            """
            SELECT COUNT(*) AS total
            FROM cdn
            """
        )

        number = int(row["total"]) + 1 if row else 1
        cdn_id = f"CDN-{number:06d}"

        self.database.execute(
            """
            INSERT INTO cdn (
                cdn_id,
                name,
                domain,
                origin_server_id,
                provider,
                region,
                status,
                cache_enabled,
                ssl_enabled,
                created_at,
                updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                cdn_id,
                name,
                domain,
                origin_server_id,
                provider,
                region,
                status,
                int(cache_enabled),
                int(ssl_enabled),
                timestamp,
                timestamp,
            ),
        )

        return CDNInfo(
            cdn_id=cdn_id,
            name=name,
            domain=domain,
            origin_server_id=origin_server_id,
            provider=provider,
            region=region,
            status=status,
            cache_enabled=cache_enabled,
            ssl_enabled=ssl_enabled,
            created_at=timestamp,
            updated_at=timestamp,
        )

    def get(self, cdn_id: str) -> CDNInfo | None:
        row = self.database.fetchone(
            """
            SELECT *
            FROM cdn
            WHERE cdn_id = ?
            """,
            (cdn_id,),
        )

        if not row:
            return None

        data = dict(row)
        data["cache_enabled"] = bool(data["cache_enabled"])
        data["ssl_enabled"] = bool(data["ssl_enabled"])

        return CDNInfo(**data)

    def list_all(self) -> list[CDNInfo]:
        rows = self.database.fetchall(
            """
            SELECT *
            FROM cdn
            ORDER BY created_at DESC
            """
        )

        result = []

        for row in rows:
            data = dict(row)
            data["cache_enabled"] = bool(data["cache_enabled"])
            data["ssl_enabled"] = bool(data["ssl_enabled"])

            result.append(CDNInfo(**data))

        return result

    def update_status(
        self,
        cdn_id: str,
        status: str,
    ) -> CDNInfo | None:

        timestamp = datetime.now(timezone.utc).isoformat()

        self.database.execute(
            """
            UPDATE cdn
            SET status = ?,
                updated_at = ?
            WHERE cdn_id = ?
            """,
            (
                status,
                timestamp,
                cdn_id,
            ),
        )

        return self.get(cdn_id)

    def update_cache(
        self,
        cdn_id: str,
        cache_enabled: bool,
    ) -> CDNInfo | None:

        timestamp = datetime.now(timezone.utc).isoformat()

        self.database.execute(
            """
            UPDATE cdn
            SET cache_enabled = ?,
                updated_at = ?
            WHERE cdn_id = ?
            """,
            (
                int(cache_enabled),
                timestamp,
                cdn_id,
            ),
        )

        return self.get(cdn_id)

    def update_ssl(
        self,
        cdn_id: str,
        ssl_enabled: bool,
    ) -> CDNInfo | None:

        timestamp = datetime.now(timezone.utc).isoformat()

        self.database.execute(
            """
            UPDATE cdn
            SET ssl_enabled = ?,
                updated_at = ?
            WHERE cdn_id = ?
            """,
            (
                int(ssl_enabled),
                timestamp,
                cdn_id,
            ),
        )

        return self.get(cdn_id)

    def delete(self, cdn_id: str) -> bool:
        row = self.database.fetchone(
            """
            SELECT cdn_id
            FROM cdn
            WHERE cdn_id = ?
            """,
            (cdn_id,),
        )

        if not row:
            return False

        self.database.execute(
            """
            DELETE FROM cdn
            WHERE cdn_id = ?
            """,
            (cdn_id,),
        )

        return True
