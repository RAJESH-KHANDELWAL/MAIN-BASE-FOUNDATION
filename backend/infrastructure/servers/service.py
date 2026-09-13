"""Server infrastructure service."""

from __future__ import annotations

from datetime import datetime, timezone

from backend.database.controller import DatabaseController

from .model import ServerInfo


class ServerService:

    def __init__(self):
        self.database = DatabaseController()
        self.initialize()

    def initialize(self) -> None:
        self.database.execute(
            """
            CREATE TABLE IF NOT EXISTS servers (
                server_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                server_type TEXT NOT NULL,
                provider TEXT DEFAULT '',
                location TEXT DEFAULT '',
                public_ipv4 TEXT DEFAULT '',
                public_ipv6 TEXT DEFAULT '',
                operating_system TEXT DEFAULT '',
                cpu_cores INTEGER DEFAULT 0,
                memory_gb REAL DEFAULT 0,
                storage_gb REAL DEFAULT 0,
                bandwidth_gb REAL DEFAULT 0,
                status TEXT DEFAULT 'PLANNED',
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )

    def create(
        self,
        name: str,
        server_type: str,
        provider: str = "",
        location: str = "",
        public_ipv4: str = "",
        public_ipv6: str = "",
        operating_system: str = "",
        cpu_cores: int = 0,
        memory_gb: float = 0,
        storage_gb: float = 0,
        bandwidth_gb: float = 0,
    ) -> ServerInfo:

        count = self.database.fetchone(
            "SELECT COUNT(*) AS total FROM servers"
        )

        server_number = int(count["total"]) + 1
        server_id = f"SRV-{server_number:06d}"

        now = datetime.now(timezone.utc).isoformat()

        server = ServerInfo(
            server_id=server_id,
            name=name,
            server_type=server_type,
            provider=provider,
            location=location,
            public_ipv4=public_ipv4,
            public_ipv6=public_ipv6,
            operating_system=operating_system,
            cpu_cores=cpu_cores,
            memory_gb=memory_gb,
            storage_gb=storage_gb,
            bandwidth_gb=bandwidth_gb,
            status="PLANNED",
            created_at=now,
            updated_at=now,
        )

        self.database.execute(
            """
            INSERT INTO servers (
                server_id,
                name,
                server_type,
                provider,
                location,
                public_ipv4,
                public_ipv6,
                operating_system,
                cpu_cores,
                memory_gb,
                storage_gb,
                bandwidth_gb,
                status,
                created_at,
                updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                server.server_id,
                server.name,
                server.server_type,
                server.provider,
                server.location,
                server.public_ipv4,
                server.public_ipv6,
                server.operating_system,
                server.cpu_cores,
                server.memory_gb,
                server.storage_gb,
                server.bandwidth_gb,
                server.status,
                server.created_at,
                server.updated_at,
            ),
        )

        return server

    def get(
        self,
        server_id: str,
    ) -> ServerInfo | None:

        row = self.database.fetchone(
            """
            SELECT *
            FROM servers
            WHERE server_id = ?
            """,
            (server_id,),
        )

        if not row:
            return None

        return ServerInfo(**dict(row))

    def list_all(self) -> list[ServerInfo]:

        rows = self.database.fetchall(
            """
            SELECT *
            FROM servers
            ORDER BY created_at DESC
            """
        )

        return [
            ServerInfo(**dict(row))
            for row in rows
        ]

    def update_status(
        self,
        server_id: str,
        status: str,
    ) -> ServerInfo | None:

        now = datetime.now(timezone.utc).isoformat()

        self.database.execute(
            """
            UPDATE servers
            SET status = ?, updated_at = ?
            WHERE server_id = ?
            """,
            (
                status,
                now,
                server_id,
            ),
        )

        return self.get(server_id)

    def delete(
        self,
        server_id: str,
    ) -> bool:

        self.database.execute(
            """
            DELETE FROM servers
            WHERE server_id = ?
            """,
            (server_id,),
        )

        return self.get(server_id) is None
