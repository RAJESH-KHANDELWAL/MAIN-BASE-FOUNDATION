"""Network infrastructure service."""

from __future__ import annotations

from datetime import datetime, timezone

from backend.database.controller import DatabaseController

from .model import NetworkInfo


class NetworkService:
    def __init__(self):
        self.database = DatabaseController()
        self.initialize()

    def initialize(self) -> None:
        self.database.execute(
            """
            CREATE TABLE IF NOT EXISTS networks (
                network_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                network_type TEXT NOT NULL,
                server_id TEXT DEFAULT '',
                provider TEXT DEFAULT '',
                region TEXT DEFAULT '',
                public_ipv4 TEXT DEFAULT '',
                public_ipv6 TEXT DEFAULT '',
                subnet TEXT DEFAULT '',
                gateway TEXT DEFAULT '',
                bandwidth_mbps REAL DEFAULT 0,
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
        network_type: str,
        server_id: str = "",
        provider: str = "",
        region: str = "",
        public_ipv4: str = "",
        public_ipv6: str = "",
        subnet: str = "",
        gateway: str = "",
        bandwidth_mbps: float = 0,
        status: str = "PLANNED",
        description: str = "",
    ) -> NetworkInfo:

        timestamp = datetime.now(timezone.utc).isoformat()

        row = self.database.fetchone(
            """
            SELECT COUNT(*) AS total
            FROM networks
            """
        )

        number = int(row["total"]) + 1 if row else 1
        network_id = f"NET-{number:06d}"

        self.database.execute(
            """
            INSERT INTO networks (
                network_id,
                name,
                network_type,
                server_id,
                provider,
                region,
                public_ipv4,
                public_ipv6,
                subnet,
                gateway,
                bandwidth_mbps,
                status,
                description,
                created_at,
                updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                network_id,
                name,
                network_type,
                server_id,
                provider,
                region,
                public_ipv4,
                public_ipv6,
                subnet,
                gateway,
                bandwidth_mbps,
                status,
                description,
                timestamp,
                timestamp,
            ),
        )

        return NetworkInfo(
            network_id=network_id,
            name=name,
            network_type=network_type,
            server_id=server_id,
            provider=provider,
            region=region,
            public_ipv4=public_ipv4,
            public_ipv6=public_ipv6,
            subnet=subnet,
            gateway=gateway,
            bandwidth_mbps=bandwidth_mbps,
            status=status,
            description=description,
            created_at=timestamp,
            updated_at=timestamp,
        )

    def get(self, network_id: str) -> NetworkInfo | None:
        row = self.database.fetchone(
            """
            SELECT *
            FROM networks
            WHERE network_id = ?
            """,
            (network_id,),
        )

        if not row:
            return None

        return NetworkInfo(**dict(row))

    def list_all(self) -> list[NetworkInfo]:
        rows = self.database.fetchall(
            """
            SELECT *
            FROM networks
            ORDER BY created_at DESC
            """
        )

        return [
            NetworkInfo(**dict(row))
            for row in rows
        ]

    def update_status(
        self,
        network_id: str,
        status: str,
    ) -> NetworkInfo | None:

        timestamp = datetime.now(timezone.utc).isoformat()

        self.database.execute(
            """
            UPDATE networks
            SET status = ?,
                updated_at = ?
            WHERE network_id = ?
            """,
            (
                status,
                timestamp,
                network_id,
            ),
        )

        return self.get(network_id)

    def delete(self, network_id: str) -> bool:
        row = self.database.fetchone(
            """
            SELECT network_id
            FROM networks
            WHERE network_id = ?
            """,
            (network_id,),
        )

        if not row:
            return False

        self.database.execute(
            """
            DELETE FROM networks
            WHERE network_id = ?
            """,
            (network_id,),
        )

        return True
