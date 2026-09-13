"""Infrastructure service layer."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional

from backend.database.controller import DatabaseController
from .model import InfrastructureInfo


class InfrastructureService:

    def __init__(self):
        self.database = DatabaseController()
        self.initialize()

    def initialize(self) -> None:
        self.database.execute(
            """
            CREATE TABLE IF NOT EXISTS infrastructure (
                infrastructure_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                infrastructure_type TEXT NOT NULL,
                provider TEXT DEFAULT '',
                region TEXT DEFAULT '',
                public_ipv4 TEXT DEFAULT '',
                public_ipv6 TEXT DEFAULT '',
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
        infrastructure_type: str,
        provider: str = "",
        region: str = "",
        public_ipv4: str = "",
        public_ipv6: str = "",
        description: str = "",
    ) -> InfrastructureInfo:

        existing = self.list_all()

        infrastructure_id = (
            f"INF-{len(existing) + 1:06d}"
        )

        now = datetime.now(timezone.utc).isoformat()

        item = InfrastructureInfo(
            infrastructure_id=infrastructure_id,
            name=name,
            infrastructure_type=infrastructure_type,
            provider=provider,
            region=region,
            public_ipv4=public_ipv4,
            public_ipv6=public_ipv6,
            status="PLANNED",
            description=description,
            created_at=now,
            updated_at=now,
        )

        self.database.execute(
            """
            INSERT INTO infrastructure (
                infrastructure_id,
                name,
                infrastructure_type,
                provider,
                region,
                public_ipv4,
                public_ipv6,
                status,
                description,
                created_at,
                updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                item.infrastructure_id,
                item.name,
                item.infrastructure_type,
                item.provider,
                item.region,
                item.public_ipv4,
                item.public_ipv6,
                item.status,
                item.description,
                item.created_at,
                item.updated_at,
            ),
        )

        return item

    def get(
        self,
        infrastructure_id: str,
    ) -> Optional[InfrastructureInfo]:

        row = self.database.fetchone(
            """
            SELECT *
            FROM infrastructure
            WHERE infrastructure_id = ?
            """,
            (infrastructure_id,),
        )

        if not row:
            return None

        return InfrastructureInfo(**dict(row))

    def list_all(self) -> list[InfrastructureInfo]:

        rows = self.database.fetchall(
            """
            SELECT *
            FROM infrastructure
            ORDER BY created_at DESC
            """
        )

        return [
            InfrastructureInfo(**dict(row))
            for row in rows
        ]

    def update_status(
        self,
        infrastructure_id: str,
        status: str,
    ) -> Optional[InfrastructureInfo]:

        now = datetime.now(timezone.utc).isoformat()

        self.database.execute(
            """
            UPDATE infrastructure
            SET status = ?, updated_at = ?
            WHERE infrastructure_id = ?
            """,
            (
                status,
                now,
                infrastructure_id,
            ),
        )

        return self.get(infrastructure_id)

    def delete(
        self,
        infrastructure_id: str,
    ) -> bool:

        self.database.execute(
            """
            DELETE FROM infrastructure
            WHERE infrastructure_id = ?
            """,
            (infrastructure_id,),
        )

        return self.get(infrastructure_id) is None
