"""
MAIN BASE FOUNDATION
Infrastructure - IPAM Service

Virtual Temple style IP address management foundation.
"""

from __future__ import annotations

import datetime
import json
from typing import Any, Dict, List, Optional

from backend.database.service import DatabaseService
from backend.infrastructure.ipam.model import IPAddressInfo


class IPAMService:
    """Manage IP address inventory through DatabaseService."""

    ALLOWED_ADDRESS_FAMILIES = {
        "IPv4",
        "IPv6",
    }

    ALLOWED_ALLOCATION_TYPES = {
        "DEDICATED",
        "SHARED",
        "RESERVED",
    }

    ALLOWED_STATUS = {
        "AVAILABLE",
        "ALLOCATED",
        "RESERVED",
        "ACTIVE",
        "SUSPENDED",
        "RELEASED",
    }

    TABLE_NAME = "infrastructure_ip_addresses"

    def __init__(
        self,
        database_service: Optional[DatabaseService] = None,
    ) -> None:
        self.database = (
            database_service
            or DatabaseService()
        )

        self.initialize()

    def initialize(self) -> None:
        """Initialize the IPAM table."""

        self.database.initialize()

        self.database.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {self.TABLE_NAME} (
                ip_address_id TEXT PRIMARY KEY,
                ip_address TEXT NOT NULL UNIQUE,
                address_family TEXT NOT NULL,
                allocation_type TEXT NOT NULL,
                provider TEXT,
                server_id TEXT,
                hosting_id TEXT,
                domain_id TEXT,
                network_id TEXT,
                gateway TEXT,
                subnet_mask TEXT,
                reverse_dns TEXT,
                status TEXT NOT NULL,
                verified INTEGER NOT NULL DEFAULT 0,
                metadata TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )

    def _next_id(self) -> str:
        row = self.database.fetchone(
            f"""
            SELECT ip_address_id
            FROM {self.TABLE_NAME}
            ORDER BY rowid DESC
            LIMIT 1
            """
        )

        if not row:
            return "IP-000001"

        number = int(
            row["ip_address_id"].split("-")[-1]
        )

        return f"IP-{number + 1:06d}"

    @staticmethod
    def _serialize_metadata(
        metadata: Optional[Dict[str, Any]],
    ) -> str:
        return json.dumps(metadata or {})

    @staticmethod
    def _deserialize_metadata(
        value: Optional[str],
    ) -> Dict[str, Any]:

        if not value:
            return {}

        try:
            return json.loads(value)
        except (TypeError, ValueError):
            return {}

    def _to_model(self, row) -> IPAddressInfo:
        return IPAddressInfo(
            ip_address_id=row["ip_address_id"],
            ip_address=row["ip_address"],
            address_family=row["address_family"],
            allocation_type=row["allocation_type"],
            provider=row["provider"],
            server_id=row["server_id"],
            hosting_id=row["hosting_id"],
            domain_id=row["domain_id"],
            network_id=row["network_id"],
            gateway=row["gateway"],
            subnet_mask=row["subnet_mask"],
            reverse_dns=row["reverse_dns"],
            status=row["status"],
            verified=bool(row["verified"]),
            metadata=self._deserialize_metadata(
                row["metadata"]
            ),
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )

    # ---------------------------------------------------------
    # CREATE
    # ---------------------------------------------------------

    def create(
        self,
        ip_address: str,
        address_family: str = "IPv4",
        allocation_type: str = "DEDICATED",
        provider: Optional[str] = None,
        server_id: Optional[str] = None,
        hosting_id: Optional[str] = None,
        domain_id: Optional[str] = None,
        network_id: Optional[str] = None,
        gateway: Optional[str] = None,
        subnet_mask: Optional[str] = None,
        reverse_dns: Optional[str] = None,
        status: str = "AVAILABLE",
        verified: bool = False,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> IPAddressInfo:

        if not ip_address:
            raise ValueError("IP address is required")

        if address_family not in self.ALLOWED_ADDRESS_FAMILIES:
            raise ValueError(
                f"Unsupported address family: "
                f"{address_family}"
            )

        if allocation_type not in self.ALLOWED_ALLOCATION_TYPES:
            raise ValueError(
                f"Unsupported allocation type: "
                f"{allocation_type}"
            )

        if status not in self.ALLOWED_STATUS:
            raise ValueError(
                f"Unsupported IP status: {status}"
            )

        ip_address_id = self._next_id()
        now = datetime.datetime.utcnow().isoformat()

        self.database.execute(
            f"""
            INSERT INTO {self.TABLE_NAME} (
                ip_address_id,
                ip_address,
                address_family,
                allocation_type,
                provider,
                server_id,
                hosting_id,
                domain_id,
                network_id,
                gateway,
                subnet_mask,
                reverse_dns,
                status,
                verified,
                metadata,
                created_at,
                updated_at
            )
            VALUES (
                ?, ?, ?, ?, ?, ?, ?, ?, ?,
                ?, ?, ?, ?, ?, ?, ?, ?
            )
            """,
            (
                ip_address_id,
                ip_address,
                address_family,
                allocation_type,
                provider,
                server_id,
                hosting_id,
                domain_id,
                network_id,
                gateway,
                subnet_mask,
                reverse_dns,
                status,
                int(verified),
                self._serialize_metadata(metadata),
                now,
                now,
            ),
        )

        return self.get(ip_address_id)

    # ---------------------------------------------------------
    # READ
    # ---------------------------------------------------------

    def get(
        self,
        ip_address_id: str,
    ) -> Optional[IPAddressInfo]:

        row = self.database.fetchone(
            f"""
            SELECT *
            FROM {self.TABLE_NAME}
            WHERE ip_address_id = ?
            """,
            (ip_address_id,),
        )

        if not row:
            return None

        return self._to_model(row)

    def get_by_address(
        self,
        ip_address: str,
    ) -> Optional[IPAddressInfo]:

        row = self.database.fetchone(
            f"""
            SELECT *
            FROM {self.TABLE_NAME}
            WHERE ip_address = ?
            """,
            (ip_address,),
        )

        if not row:
            return None

        return self._to_model(row)

    def list(
        self,
        status: Optional[str] = None,
    ) -> List[IPAddressInfo]:

        if status:
            rows = self.database.fetchall(
                f"""
                SELECT *
                FROM {self.TABLE_NAME}
                WHERE status = ?
                ORDER BY rowid ASC
                """,
                (status,),
            )
        else:
            rows = self.database.fetchall(
                f"""
                SELECT *
                FROM {self.TABLE_NAME}
                ORDER BY rowid ASC
                """
            )

        return [
            self._to_model(row)
            for row in rows
        ]

    def exists(
        self,
        ip_address: str,
    ) -> bool:

        row = self.database.fetchone(
            f"""
            SELECT ip_address_id
            FROM {self.TABLE_NAME}
            WHERE ip_address = ?
            """,
            (ip_address,),
        )

        return row is not None

    # ---------------------------------------------------------
    # UPDATE
    # ---------------------------------------------------------

    def update(
        self,
        ip_address_id: str,
        **updates,
    ) -> Optional[IPAddressInfo]:

        current = self.get(ip_address_id)

        if not current:
            return None

        allowed_fields = {
            "ip_address",
            "address_family",
            "allocation_type",
            "provider",
            "server_id",
            "hosting_id",
            "domain_id",
            "network_id",
            "gateway",
            "subnet_mask",
            "reverse_dns",
            "status",
            "verified",
            "metadata",
        }

        updates = {
            key: value
            for key, value in updates.items()
            if key in allowed_fields
        }

        if not updates:
            return current

        if "address_family" in updates:
            if (
                updates["address_family"]
                not in self.ALLOWED_ADDRESS_FAMILIES
            ):
                raise ValueError(
                    "Unsupported address family: "
                    f"{updates['address_family']}"
                )

        if "allocation_type" in updates:
            if (
                updates["allocation_type"]
                not in self.ALLOWED_ALLOCATION_TYPES
            ):
                raise ValueError(
                    "Unsupported allocation type: "
                    f"{updates['allocation_type']}"
                )

        if "status" in updates:
            if updates["status"] not in self.ALLOWED_STATUS:
                raise ValueError(
                    f"Unsupported IP status: "
                    f"{updates['status']}"
                )

        if "metadata" in updates:
            updates["metadata"] = self._serialize_metadata(
                updates["metadata"]
            )

        if "verified" in updates:
            updates["verified"] = int(
                updates["verified"]
            )

        updates["updated_at"] = (
            datetime.datetime.utcnow().isoformat()
        )

        set_clause = ", ".join(
            f"{field} = ?"
            for field in updates
        )

        values = list(updates.values())
        values.append(ip_address_id)

        self.database.execute(
            f"""
            UPDATE {self.TABLE_NAME}
            SET {set_clause}
            WHERE ip_address_id = ?
            """,
            values,
        )

        return self.get(ip_address_id)

    # ---------------------------------------------------------
    # DELETE
    # ---------------------------------------------------------

    def delete(
        self,
        ip_address_id: str,
    ) -> bool:

        affected = self.database.execute(
            f"""
            DELETE FROM {self.TABLE_NAME}
            WHERE ip_address_id = ?
            """,
            (ip_address_id,),
        )

        return affected > 0

    # ---------------------------------------------------------
    # ATTACHMENTS
    # ---------------------------------------------------------

    def attach_server(
        self,
        ip_address_id: str,
        server_id: str,
    ) -> Optional[IPAddressInfo]:

        return self.update(
            ip_address_id,
            server_id=server_id,
            status="ALLOCATED",
        )

    def attach_hosting(
        self,
        ip_address_id: str,
        hosting_id: str,
    ) -> Optional[IPAddressInfo]:

        return self.update(
            ip_address_id,
            hosting_id=hosting_id,
            status="ALLOCATED",
        )

    def attach_domain(
        self,
        ip_address_id: str,
        domain_id: str,
    ) -> Optional[IPAddressInfo]:

        return self.update(
            ip_address_id,
            domain_id=domain_id,
            status="ALLOCATED",
        )

    # ---------------------------------------------------------
    # STATE OPERATIONS
    # ---------------------------------------------------------

    def set_active(
        self,
        ip_address_id: str,
    ) -> Optional[IPAddressInfo]:

        return self.update(
            ip_address_id,
            status="ACTIVE",
        )

    def reserve(
        self,
        ip_address_id: str,
    ) -> Optional[IPAddressInfo]:

        return self.update(
            ip_address_id,
            status="RESERVED",
        )

    def release(
        self,
        ip_address_id: str,
    ) -> Optional[IPAddressInfo]:

        return self.update(
            ip_address_id,
            status="RELEASED",
        )


__all__ = [
    "IPAMService",
]
