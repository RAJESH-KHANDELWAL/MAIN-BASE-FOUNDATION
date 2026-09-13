"""IP Address Management service."""

from __future__ import annotations

from datetime import datetime, timezone

from backend.database.controller import DatabaseController

from .model import IPAddressInfo


class IPAddressService:
    def __init__(self):
        self.database = DatabaseController()
        self.initialize()

    def initialize(self) -> None:
        self.database.execute(
            """
            CREATE TABLE IF NOT EXISTS ip_addresses (
                ip_id TEXT PRIMARY KEY,
                address TEXT NOT NULL UNIQUE,
                address_family TEXT NOT NULL,
                ip_type TEXT DEFAULT 'PUBLIC',
                network_id TEXT DEFAULT '',
                server_id TEXT DEFAULT '',
                provider TEXT DEFAULT '',
                region TEXT DEFAULT '',
                status TEXT DEFAULT 'PLANNED',
                allocation_type TEXT DEFAULT 'DYNAMIC',
                description TEXT DEFAULT '',
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )

    def create(
        self,
        address: str,
        address_family: str,
        ip_type: str = "PUBLIC",
        network_id: str = "",
        server_id: str = "",
        provider: str = "",
        region: str = "",
        status: str = "PLANNED",
        allocation_type: str = "DYNAMIC",
        description: str = "",
    ) -> IPAddressInfo:

        timestamp = datetime.now(timezone.utc).isoformat()

        existing = self.database.fetchone(
            """
            SELECT ip_id
            FROM ip_addresses
            WHERE address = ?
            """,
            (address,),
        )

        if existing:
            raise ValueError("IP address already exists")

        row = self.database.fetchone(
            """
            SELECT COUNT(*) AS total
            FROM ip_addresses
            """
        )

        number = int(row["total"]) + 1 if row else 1
        ip_id = f"IP-{number:06d}"

        self.database.execute(
            """
            INSERT INTO ip_addresses (
                ip_id,
                address,
                address_family,
                ip_type,
                network_id,
                server_id,
                provider,
                region,
                status,
                allocation_type,
                description,
                created_at,
                updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                ip_id,
                address,
                address_family,
                ip_type,
                network_id,
                server_id,
                provider,
                region,
                status,
                allocation_type,
                description,
                timestamp,
                timestamp,
            ),
        )

        return IPAddressInfo(
            ip_id=ip_id,
            address=address,
            address_family=address_family,
            ip_type=ip_type,
            network_id=network_id,
            server_id=server_id,
            provider=provider,
            region=region,
            status=status,
            allocation_type=allocation_type,
            description=description,
            created_at=timestamp,
            updated_at=timestamp,
        )

    def get(self, ip_id: str) -> IPAddressInfo | None:
        row = self.database.fetchone(
            """
            SELECT *
            FROM ip_addresses
            WHERE ip_id = ?
            """,
            (ip_id,),
        )

        if not row:
            return None

        return IPAddressInfo(**dict(row))

    def get_by_address(
        self,
        address: str,
    ) -> IPAddressInfo | None:

        row = self.database.fetchone(
            """
            SELECT *
            FROM ip_addresses
            WHERE address = ?
            """,
            (address,),
        )

        if not row:
            return None

        return IPAddressInfo(**dict(row))

    def list_all(self) -> list[IPAddressInfo]:
        rows = self.database.fetchall(
            """
            SELECT *
            FROM ip_addresses
            ORDER BY created_at DESC
            """
        )

        return [
            IPAddressInfo(**dict(row))
            for row in rows
        ]

    def update_status(
        self,
        ip_id: str,
        status: str,
    ) -> IPAddressInfo | None:

        timestamp = datetime.now(timezone.utc).isoformat()

        self.database.execute(
            """
            UPDATE ip_addresses
            SET status = ?,
                updated_at = ?
            WHERE ip_id = ?
            """,
            (
                status,
                timestamp,
                ip_id,
            ),
        )

        return self.get(ip_id)

    def update_allocation(
        self,
        ip_id: str,
        allocation_type: str,
        server_id: str = "",
    ) -> IPAddressInfo | None:

        timestamp = datetime.now(timezone.utc).isoformat()

        self.database.execute(
            """
            UPDATE ip_addresses
            SET allocation_type = ?,
                server_id = ?,
                updated_at = ?
            WHERE ip_id = ?
            """,
            (
                allocation_type,
                server_id,
                timestamp,
                ip_id,
            ),
        )

        return self.get(ip_id)

    def delete(self, ip_id: str) -> bool:
        row = self.database.fetchone(
            """
            SELECT ip_id
            FROM ip_addresses
            WHERE ip_id = ?
            """,
            (ip_id,),
        )

        if not row:
            return False

        self.database.execute(
            """
            DELETE FROM ip_addresses
            WHERE ip_id = ?
            """,
            (ip_id,),
        )

        return True
