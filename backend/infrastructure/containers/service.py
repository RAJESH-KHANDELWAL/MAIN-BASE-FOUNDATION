"""Container infrastructure service."""

from __future__ import annotations

from datetime import datetime, timezone

from backend.database.controller import DatabaseController

from .model import ContainerInfo


class ContainerService:
    def __init__(self):
        self.database = DatabaseController()
        self.initialize()

    def initialize(self) -> None:
        self.database.execute(
            """
            CREATE TABLE IF NOT EXISTS containers (
                container_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                image TEXT NOT NULL,
                server_id TEXT DEFAULT '',
                provider TEXT DEFAULT '',
                region TEXT DEFAULT '',
                ports TEXT DEFAULT '',
                status TEXT DEFAULT 'PLANNED',
                replicas INTEGER DEFAULT 1,
                restart_policy TEXT DEFAULT 'ALWAYS',
                description TEXT DEFAULT '',
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )

    def create(
        self,
        name: str,
        image: str,
        server_id: str = "",
        provider: str = "",
        region: str = "",
        ports: str = "",
        status: str = "PLANNED",
        replicas: int = 1,
        restart_policy: str = "ALWAYS",
        description: str = "",
    ) -> ContainerInfo:

        timestamp = datetime.now(timezone.utc).isoformat()

        existing = self.database.fetchone(
            """
            SELECT container_id
            FROM containers
            WHERE name = ?
            """,
            (name,),
        )

        if existing:
            raise ValueError("Container name already exists")

        row = self.database.fetchone(
            """
            SELECT COUNT(*) AS total
            FROM containers
            """
        )

        number = int(row["total"]) + 1 if row else 1
        container_id = f"CTR-{number:06d}"

        self.database.execute(
            """
            INSERT INTO containers (
                container_id,
                name,
                image,
                server_id,
                provider,
                region,
                ports,
                status,
                replicas,
                restart_policy,
                description,
                created_at,
                updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                container_id,
                name,
                image,
                server_id,
                provider,
                region,
                ports,
                status,
                replicas,
                restart_policy,
                description,
                timestamp,
                timestamp,
            ),
        )

        return ContainerInfo(
            container_id=container_id,
            name=name,
            image=image,
            server_id=server_id,
            provider=provider,
            region=region,
            ports=ports,
            status=status,
            replicas=replicas,
            restart_policy=restart_policy,
            description=description,
            created_at=timestamp,
            updated_at=timestamp,
        )

    def get(self, container_id: str) -> ContainerInfo | None:
        row = self.database.fetchone(
            """
            SELECT *
            FROM containers
            WHERE container_id = ?
            """,
            (container_id,),
        )

        if not row:
            return None

        return ContainerInfo(**dict(row))

    def list_all(self) -> list[ContainerInfo]:
        rows = self.database.fetchall(
            """
            SELECT *
            FROM containers
            ORDER BY created_at DESC
            """
        )

        return [
            ContainerInfo(**dict(row))
            for row in rows
        ]

    def update_status(
        self,
        container_id: str,
        status: str,
    ) -> ContainerInfo | None:

        timestamp = datetime.now(timezone.utc).isoformat()

        self.database.execute(
            """
            UPDATE containers
            SET status = ?,
                updated_at = ?
            WHERE container_id = ?
            """,
            (
                status,
                timestamp,
                container_id,
            ),
        )

        return self.get(container_id)

    def update_replicas(
        self,
        container_id: str,
        replicas: int,
    ) -> ContainerInfo | None:

        timestamp = datetime.now(timezone.utc).isoformat()

        self.database.execute(
            """
            UPDATE containers
            SET replicas = ?,
                updated_at = ?
            WHERE container_id = ?
            """,
            (
                replicas,
                timestamp,
                container_id,
            ),
        )

        return self.get(container_id)

    def delete(self, container_id: str) -> bool:
        row = self.database.fetchone(
            """
            SELECT container_id
            FROM containers
            WHERE container_id = ?
            """,
            (container_id,),
        )

        if not row:
            return False

        self.database.execute(
            """
            DELETE FROM containers
            WHERE container_id = ?
            """,
            (container_id,),
        )

        return True
