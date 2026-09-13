"""Monitoring infrastructure service."""

from __future__ import annotations

from datetime import datetime, timezone

from backend.database.controller import DatabaseController

from .model import MonitoringInfo


class MonitoringService:
    def __init__(self):
        self.database = DatabaseController()
        self.initialize()

    def initialize(self) -> None:
        self.database.execute(
            """
            CREATE TABLE IF NOT EXISTS monitoring (
                monitoring_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                resource_type TEXT NOT NULL,
                resource_id TEXT DEFAULT '',
                endpoint TEXT DEFAULT '',
                check_type TEXT DEFAULT 'HEALTH',
                interval_seconds INTEGER DEFAULT 60,
                status TEXT DEFAULT 'PLANNED',
                last_check_at TEXT DEFAULT '',
                last_status TEXT DEFAULT '',
                description TEXT DEFAULT '',
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )

    def create(
        self,
        name: str,
        resource_type: str,
        resource_id: str = "",
        endpoint: str = "",
        check_type: str = "HEALTH",
        interval_seconds: int = 60,
        status: str = "PLANNED",
        description: str = "",
    ) -> MonitoringInfo:

        timestamp = datetime.now(timezone.utc).isoformat()

        row = self.database.fetchone(
            """
            SELECT COUNT(*) AS total
            FROM monitoring
            """
        )

        number = int(row["total"]) + 1 if row else 1
        monitoring_id = f"MON-{number:06d}"

        self.database.execute(
            """
            INSERT INTO monitoring (
                monitoring_id,
                name,
                resource_type,
                resource_id,
                endpoint,
                check_type,
                interval_seconds,
                status,
                last_check_at,
                last_status,
                description,
                created_at,
                updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                monitoring_id,
                name,
                resource_type,
                resource_id,
                endpoint,
                check_type,
                interval_seconds,
                status,
                "",
                "",
                description,
                timestamp,
                timestamp,
            ),
        )

        return MonitoringInfo(
            monitoring_id=monitoring_id,
            name=name,
            resource_type=resource_type,
            resource_id=resource_id,
            endpoint=endpoint,
            check_type=check_type,
            interval_seconds=interval_seconds,
            status=status,
            last_check_at="",
            last_status="",
            description=description,
            created_at=timestamp,
            updated_at=timestamp,
        )

    def get(self, monitoring_id: str) -> MonitoringInfo | None:
        row = self.database.fetchone(
            """
            SELECT *
            FROM monitoring
            WHERE monitoring_id = ?
            """,
            (monitoring_id,),
        )

        if not row:
            return None

        return MonitoringInfo(**dict(row))

    def list_all(self) -> list[MonitoringInfo]:
        rows = self.database.fetchall(
            """
            SELECT *
            FROM monitoring
            ORDER BY created_at DESC
            """
        )

        return [
            MonitoringInfo(**dict(row))
            for row in rows
        ]

    def update_status(
        self,
        monitoring_id: str,
        status: str,
    ) -> MonitoringInfo | None:

        timestamp = datetime.now(timezone.utc).isoformat()

        self.database.execute(
            """
            UPDATE monitoring
            SET status = ?,
                updated_at = ?
            WHERE monitoring_id = ?
            """,
            (
                status,
                timestamp,
                monitoring_id,
            ),
        )

        return self.get(monitoring_id)

    def record_check(
        self,
        monitoring_id: str,
        check_status: str,
    ) -> MonitoringInfo | None:

        timestamp = datetime.now(timezone.utc).isoformat()

        self.database.execute(
            """
            UPDATE monitoring
            SET last_check_at = ?,
                last_status = ?,
                updated_at = ?
            WHERE monitoring_id = ?
            """,
            (
                timestamp,
                check_status,
                timestamp,
                monitoring_id,
            ),
        )

        return self.get(monitoring_id)

    def delete(self, monitoring_id: str) -> bool:
        row = self.database.fetchone(
            """
            SELECT monitoring_id
            FROM monitoring
            WHERE monitoring_id = ?
            """,
            (monitoring_id,),
        )

        if not row:
            return False

        self.database.execute(
            """
            DELETE FROM monitoring
            WHERE monitoring_id = ?
            """,
            (monitoring_id,),
        )

        return True
