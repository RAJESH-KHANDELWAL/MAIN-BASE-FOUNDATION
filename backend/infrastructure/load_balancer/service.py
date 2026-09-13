"""Load balancer infrastructure service."""

from __future__ import annotations

from datetime import datetime, timezone

from backend.database.controller import DatabaseController

from .model import LoadBalancerInfo


class LoadBalancerService:
    def __init__(self):
        self.database = DatabaseController()
        self.initialize()

    def initialize(self) -> None:
        self.database.execute(
            """
            CREATE TABLE IF NOT EXISTS load_balancers (
                load_balancer_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                load_balancer_type TEXT NOT NULL,
                domain TEXT DEFAULT '',
                network_id TEXT DEFAULT '',
                provider TEXT DEFAULT '',
                region TEXT DEFAULT '',
                algorithm TEXT DEFAULT 'ROUND_ROBIN',
                status TEXT DEFAULT 'PLANNED',
                enabled INTEGER DEFAULT 1,
                health_check_enabled INTEGER DEFAULT 1,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )

    def create(
        self,
        name: str,
        load_balancer_type: str,
        domain: str = "",
        network_id: str = "",
        provider: str = "",
        region: str = "",
        algorithm: str = "ROUND_ROBIN",
        status: str = "PLANNED",
        enabled: bool = True,
        health_check_enabled: bool = True,
    ) -> LoadBalancerInfo:

        timestamp = datetime.now(timezone.utc).isoformat()

        row = self.database.fetchone(
            """
            SELECT COUNT(*) AS total
            FROM load_balancers
            """
        )

        number = int(row["total"]) + 1 if row else 1
        load_balancer_id = f"LB-{number:06d}"

        self.database.execute(
            """
            INSERT INTO load_balancers (
                load_balancer_id,
                name,
                load_balancer_type,
                domain,
                network_id,
                provider,
                region,
                algorithm,
                status,
                enabled,
                health_check_enabled,
                created_at,
                updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                load_balancer_id,
                name,
                load_balancer_type,
                domain,
                network_id,
                provider,
                region,
                algorithm,
                status,
                int(enabled),
                int(health_check_enabled),
                timestamp,
                timestamp,
            ),
        )

        return LoadBalancerInfo(
            load_balancer_id=load_balancer_id,
            name=name,
            load_balancer_type=load_balancer_type,
            domain=domain,
            network_id=network_id,
            provider=provider,
            region=region,
            algorithm=algorithm,
            status=status,
            enabled=enabled,
            health_check_enabled=health_check_enabled,
            created_at=timestamp,
            updated_at=timestamp,
        )

    def get(
        self,
        load_balancer_id: str,
    ) -> LoadBalancerInfo | None:

        row = self.database.fetchone(
            """
            SELECT *
            FROM load_balancers
            WHERE load_balancer_id = ?
            """,
            (load_balancer_id,),
        )

        if not row:
            return None

        data = dict(row)
        data["enabled"] = bool(data["enabled"])
        data["health_check_enabled"] = bool(
            data["health_check_enabled"]
        )

        return LoadBalancerInfo(**data)

    def list_all(self) -> list[LoadBalancerInfo]:
        rows = self.database.fetchall(
            """
            SELECT *
            FROM load_balancers
            ORDER BY created_at DESC
            """
        )

        result = []

        for row in rows:
            data = dict(row)
            data["enabled"] = bool(data["enabled"])
            data["health_check_enabled"] = bool(
                data["health_check_enabled"]
            )

            result.append(
                LoadBalancerInfo(**data)
            )

        return result

    def update_status(
        self,
        load_balancer_id: str,
        status: str,
    ) -> LoadBalancerInfo | None:

        timestamp = datetime.now(timezone.utc).isoformat()

        self.database.execute(
            """
            UPDATE load_balancers
            SET status = ?,
                updated_at = ?
            WHERE load_balancer_id = ?
            """,
            (
                status,
                timestamp,
                load_balancer_id,
            ),
        )

        return self.get(load_balancer_id)

    def update_enabled(
        self,
        load_balancer_id: str,
        enabled: bool,
    ) -> LoadBalancerInfo | None:

        timestamp = datetime.now(timezone.utc).isoformat()

        self.database.execute(
            """
            UPDATE load_balancers
            SET enabled = ?,
                updated_at = ?
            WHERE load_balancer_id = ?
            """,
            (
                int(enabled),
                timestamp,
                load_balancer_id,
            ),
        )

        return self.get(load_balancer_id)

    def update_health_check(
        self,
        load_balancer_id: str,
        health_check_enabled: bool,
    ) -> LoadBalancerInfo | None:

        timestamp = datetime.now(timezone.utc).isoformat()

        self.database.execute(
            """
            UPDATE load_balancers
            SET health_check_enabled = ?,
                updated_at = ?
            WHERE load_balancer_id = ?
            """,
            (
                int(health_check_enabled),
                timestamp,
                load_balancer_id,
            ),
        )

        return self.get(load_balancer_id)

    def delete(self, load_balancer_id: str) -> bool:
        row = self.database.fetchone(
            """
            SELECT load_balancer_id
            FROM load_balancers
            WHERE load_balancer_id = ?
            """,
            (load_balancer_id,),
        )

        if not row:
            return False

        self.database.execute(
            """
            DELETE FROM load_balancers
            WHERE load_balancer_id = ?
            """,
            (load_balancer_id,),
        )

        return True
