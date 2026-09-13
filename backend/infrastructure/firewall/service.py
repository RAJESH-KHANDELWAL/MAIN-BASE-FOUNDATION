"""Firewall infrastructure service."""

from __future__ import annotations

from datetime import datetime, timezone

from backend.database.controller import DatabaseController

from .model import FirewallInfo


class FirewallService:
    def __init__(self):
        self.database = DatabaseController()
        self.initialize()

    def initialize(self) -> None:
        self.database.execute(
            """
            CREATE TABLE IF NOT EXISTS firewalls (
                firewall_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                firewall_type TEXT NOT NULL,
                resource_type TEXT DEFAULT '',
                resource_id TEXT DEFAULT '',
                provider TEXT DEFAULT '',
                region TEXT DEFAULT '',
                status TEXT DEFAULT 'PLANNED',
                enabled INTEGER DEFAULT 1,
                default_policy TEXT DEFAULT 'DENY',
                description TEXT DEFAULT '',
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )

    def create(
        self,
        name: str,
        firewall_type: str,
        resource_type: str = "",
        resource_id: str = "",
        provider: str = "",
        region: str = "",
        status: str = "PLANNED",
        enabled: bool = True,
        default_policy: str = "DENY",
        description: str = "",
    ) -> FirewallInfo:

        timestamp = datetime.now(timezone.utc).isoformat()

        row = self.database.fetchone(
            """
            SELECT COUNT(*) AS total
            FROM firewalls
            """
        )

        number = int(row["total"]) + 1 if row else 1
        firewall_id = f"FW-{number:06d}"

        self.database.execute(
            """
            INSERT INTO firewalls (
                firewall_id,
                name,
                firewall_type,
                resource_type,
                resource_id,
                provider,
                region,
                status,
                enabled,
                default_policy,
                description,
                created_at,
                updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                firewall_id,
                name,
                firewall_type,
                resource_type,
                resource_id,
                provider,
                region,
                status,
                int(enabled),
                default_policy,
                description,
                timestamp,
                timestamp,
            ),
        )

        return FirewallInfo(
            firewall_id=firewall_id,
            name=name,
            firewall_type=firewall_type,
            resource_type=resource_type,
            resource_id=resource_id,
            provider=provider,
            region=region,
            status=status,
            enabled=enabled,
            default_policy=default_policy,
            description=description,
            created_at=timestamp,
            updated_at=timestamp,
        )

    def get(self, firewall_id: str) -> FirewallInfo | None:
        row = self.database.fetchone(
            """
            SELECT *
            FROM firewalls
            WHERE firewall_id = ?
            """,
            (firewall_id,),
        )

        if not row:
            return None

        data = dict(row)
        data["enabled"] = bool(data["enabled"])

        return FirewallInfo(**data)

    def list_all(self) -> list[FirewallInfo]:
        rows = self.database.fetchall(
            """
            SELECT *
            FROM firewalls
            ORDER BY created_at DESC
            """
        )

        result = []

        for row in rows:
            data = dict(row)
            data["enabled"] = bool(data["enabled"])

            result.append(
                FirewallInfo(**data)
            )

        return result

    def update_status(
        self,
        firewall_id: str,
        status: str,
    ) -> FirewallInfo | None:

        timestamp = datetime.now(timezone.utc).isoformat()

        self.database.execute(
            """
            UPDATE firewalls
            SET status = ?,
                updated_at = ?
            WHERE firewall_id = ?
            """,
            (
                status,
                timestamp,
                firewall_id,
            ),
        )

        return self.get(firewall_id)

    def update_enabled(
        self,
        firewall_id: str,
        enabled: bool,
    ) -> FirewallInfo | None:

        timestamp = datetime.now(timezone.utc).isoformat()

        self.database.execute(
            """
            UPDATE firewalls
            SET enabled = ?,
                updated_at = ?
            WHERE firewall_id = ?
            """,
            (
                int(enabled),
                timestamp,
                firewall_id,
            ),
        )

        return self.get(firewall_id)

    def delete(self, firewall_id: str) -> bool:
        row = self.database.fetchone(
            """
            SELECT firewall_id
            FROM firewalls
            WHERE firewall_id = ?
            """,
            (firewall_id,),
        )

        if not row:
            return False

        self.database.execute(
            """
            DELETE FROM firewalls
            WHERE firewall_id = ?
            """,
            (firewall_id,),
        )

        return True
