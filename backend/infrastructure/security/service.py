"""Security infrastructure service."""

from __future__ import annotations

from datetime import datetime, timezone

from backend.database.controller import DatabaseController

from .model import SecurityInfo


class SecurityService:
    def __init__(self):
        self.database = DatabaseController()
        self.initialize()

    def initialize(self) -> None:
        self.database.execute(
            """
            CREATE TABLE IF NOT EXISTS security (
                security_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                security_type TEXT NOT NULL,
                resource_type TEXT DEFAULT '',
                resource_id TEXT DEFAULT '',
                provider TEXT DEFAULT '',
                status TEXT DEFAULT 'PLANNED',
                enabled INTEGER DEFAULT 1,
                description TEXT DEFAULT '',
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )

    def create(
        self,
        name: str,
        security_type: str,
        resource_type: str = "",
        resource_id: str = "",
        provider: str = "",
        status: str = "PLANNED",
        enabled: bool = True,
        description: str = "",
    ) -> SecurityInfo:

        timestamp = datetime.now(timezone.utc).isoformat()

        row = self.database.fetchone(
            """
            SELECT COUNT(*) AS total
            FROM security
            """
        )

        number = int(row["total"]) + 1 if row else 1
        security_id = f"SEC-{number:06d}"

        self.database.execute(
            """
            INSERT INTO security (
                security_id,
                name,
                security_type,
                resource_type,
                resource_id,
                provider,
                status,
                enabled,
                description,
                created_at,
                updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                security_id,
                name,
                security_type,
                resource_type,
                resource_id,
                provider,
                status,
                int(enabled),
                description,
                timestamp,
                timestamp,
            ),
        )

        return SecurityInfo(
            security_id=security_id,
            name=name,
            security_type=security_type,
            resource_type=resource_type,
            resource_id=resource_id,
            provider=provider,
            status=status,
            enabled=enabled,
            description=description,
            created_at=timestamp,
            updated_at=timestamp,
        )

    def get(self, security_id: str) -> SecurityInfo | None:
        row = self.database.fetchone(
            """
            SELECT *
            FROM security
            WHERE security_id = ?
            """,
            (security_id,),
        )

        if not row:
            return None

        data = dict(row)
        data["enabled"] = bool(data["enabled"])

        return SecurityInfo(**data)

    def list_all(self) -> list[SecurityInfo]:
        rows = self.database.fetchall(
            """
            SELECT *
            FROM security
            ORDER BY created_at DESC
            """
        )

        result = []

        for row in rows:
            data = dict(row)
            data["enabled"] = bool(data["enabled"])

            result.append(
                SecurityInfo(**data)
            )

        return result

    def update_status(
        self,
        security_id: str,
        status: str,
    ) -> SecurityInfo | None:

        timestamp = datetime.now(timezone.utc).isoformat()

        self.database.execute(
            """
            UPDATE security
            SET status = ?,
                updated_at = ?
            WHERE security_id = ?
            """,
            (
                status,
                timestamp,
                security_id,
            ),
        )

        return self.get(security_id)

    def update_enabled(
        self,
        security_id: str,
        enabled: bool,
    ) -> SecurityInfo | None:

        timestamp = datetime.now(timezone.utc).isoformat()

        self.database.execute(
            """
            UPDATE security
            SET enabled = ?,
                updated_at = ?
            WHERE security_id = ?
            """,
            (
                int(enabled),
                timestamp,
                security_id,
            ),
        )

        return self.get(security_id)

    def delete(self, security_id: str) -> bool:
        row = self.database.fetchone(
            """
            SELECT security_id
            FROM security
            WHERE security_id = ?
            """,
            (security_id,),
        )

        if not row:
            return False

        self.database.execute(
            """
            DELETE FROM security
            WHERE security_id = ?
            """,
            (security_id,),
        )

        return True
