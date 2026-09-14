"""
MAIN BASE FOUNDATION
Infrastructure - Network Service

Network inventory and network lifecycle service.
"""

from __future__ import annotations

import datetime
import json
from typing import Any, Dict, List, Optional

from backend.database.service import DatabaseService
from backend.infrastructure.network.model import NetworkInfo


class NetworkService:
    """Manage network inventory through DatabaseService."""

    ALLOWED_NETWORK_TYPES = {
        "PUBLIC",
        "PRIVATE",
        "INTERNAL",
        "MANAGEMENT",
        "STORAGE",
    }

    ALLOWED_STATUS = {
        "ACTIVE",
        "PROVISIONING",
        "MAINTENANCE",
        "SUSPENDED",
        "OFFLINE",
        "TERMINATED",
    }

    TABLE_NAME = "infrastructure_networks"

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
        """Initialize the network table."""

        self.database.initialize()

        self.database.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {self.TABLE_NAME} (
                network_id TEXT PRIMARY KEY,
                name TEXT NOT NULL UNIQUE,
                network_type TEXT NOT NULL,
                provider TEXT,
                region TEXT,
                datacenter TEXT,
                cidr TEXT,
                gateway TEXT,
                subnet_mask TEXT,
                dns_primary TEXT,
                dns_secondary TEXT,
                vlan_id INTEGER,
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
            SELECT network_id
            FROM {self.TABLE_NAME}
            ORDER BY rowid DESC
            LIMIT 1
            """
        )

        if not row:
            return "NET-000001"

        number = int(
            row["network_id"].split("-")[-1]
        )

        return f"NET-{number + 1:06d}"

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

    def _to_model(self, row) -> NetworkInfo:
        return NetworkInfo(
            network_id=row["network_id"],
            name=row["name"],
            network_type=row["network_type"],
            provider=row["provider"],
            region=row["region"],
            datacenter=row["datacenter"],
            cidr=row["cidr"],
            gateway=row["gateway"],
            subnet_mask=row["subnet_mask"],
            dns_primary=row["dns_primary"],
            dns_secondary=row["dns_secondary"],
            vlan_id=row["vlan_id"],
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
        name: str,
        network_type: str = "PUBLIC",
        provider: Optional[str] = None,
        region: Optional[str] = None,
        datacenter: Optional[str] = None,
        cidr: Optional[str] = None,
        gateway: Optional[str] = None,
        subnet_mask: Optional[str] = None,
        dns_primary: Optional[str] = None,
        dns_secondary: Optional[str] = None,
        vlan_id: Optional[int] = None,
        status: str = "ACTIVE",
        verified: bool = False,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> NetworkInfo:

        if not name:
            raise ValueError("Network name is required")

        if network_type not in self.ALLOWED_NETWORK_TYPES:
            raise ValueError(
                f"Unsupported network type: "
                f"{network_type}"
            )

        if status not in self.ALLOWED_STATUS:
            raise ValueError(
                f"Unsupported network status: "
                f"{status}"
            )

        network_id = self._next_id()
        now = datetime.datetime.utcnow().isoformat()

        self.database.execute(
            f"""
            INSERT INTO {self.TABLE_NAME} (
                network_id,
                name,
                network_type,
                provider,
                region,
                datacenter,
                cidr,
                gateway,
                subnet_mask,
                dns_primary,
                dns_secondary,
                vlan_id,
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
                network_id,
                name,
                network_type,
                provider,
                region,
                datacenter,
                cidr,
                gateway,
                subnet_mask,
                dns_primary,
                dns_secondary,
                vlan_id,
                status,
                int(verified),
                self._serialize_metadata(metadata),
                now,
                now,
            ),
        )

        return self.get(network_id)

    # ---------------------------------------------------------
    # READ
    # ---------------------------------------------------------

    def get(
        self,
        network_id: str,
    ) -> Optional[NetworkInfo]:

        row = self.database.fetchone(
            f"""
            SELECT *
            FROM {self.TABLE_NAME}
            WHERE network_id = ?
            """,
            (network_id,),
        )

        if not row:
            return None

        return self._to_model(row)

    def get_by_name(
        self,
        name: str,
    ) -> Optional[NetworkInfo]:

        row = self.database.fetchone(
            f"""
            SELECT *
            FROM {self.TABLE_NAME}
            WHERE name = ?
            """,
            (name,),
        )

        if not row:
            return None

        return self._to_model(row)

    def list(
        self,
        status: Optional[str] = None,
        network_type: Optional[str] = None,
    ) -> List[NetworkInfo]:

        conditions = []
        values = []

        if status:
            if status not in self.ALLOWED_STATUS:
                raise ValueError(
                    f"Unsupported network status: "
                    f"{status}"
                )

            conditions.append("status = ?")
            values.append(status)

        if network_type:
            if network_type not in self.ALLOWED_NETWORK_TYPES:
                raise ValueError(
                    f"Unsupported network type: "
                    f"{network_type}"
                )

            conditions.append("network_type = ?")
            values.append(network_type)

        if conditions:
            where_clause = (
                "WHERE " + " AND ".join(conditions)
            )
        else:
            where_clause = ""

        rows = self.database.fetchall(
            f"""
            SELECT *
            FROM {self.TABLE_NAME}
            {where_clause}
            ORDER BY rowid ASC
            """,
            values,
        )

        return [
            self._to_model(row)
            for row in rows
        ]

    def list_by_type(
        self,
        network_type: str,
    ) -> List[NetworkInfo]:

        return self.list(
            network_type=network_type
        )

    def exists(
        self,
        name: str,
    ) -> bool:

        row = self.database.fetchone(
            f"""
            SELECT network_id
            FROM {self.TABLE_NAME}
            WHERE name = ?
            """,
            (name,),
        )

        return row is not None

    # ---------------------------------------------------------
    # UPDATE
    # ---------------------------------------------------------

    def update(
        self,
        network_id: str,
        **updates,
    ) -> Optional[NetworkInfo]:

        current = self.get(network_id)

        if not current:
            return None

        allowed_fields = {
            "name",
            "network_type",
            "provider",
            "region",
            "datacenter",
            "cidr",
            "gateway",
            "subnet_mask",
            "dns_primary",
            "dns_secondary",
            "vlan_id",
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

        if "network_type" in updates:
            if (
                updates["network_type"]
                not in self.ALLOWED_NETWORK_TYPES
            ):
                raise ValueError(
                    f"Unsupported network type: "
                    f"{updates['network_type']}"
                )

        if "status" in updates:
            if updates["status"] not in self.ALLOWED_STATUS:
                raise ValueError(
                    f"Unsupported network status: "
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
        values.append(network_id)

        self.database.execute(
            f"""
            UPDATE {self.TABLE_NAME}
            SET {set_clause}
            WHERE network_id = ?
            """,
            values,
        )

        return self.get(network_id)

    # ---------------------------------------------------------
    # DELETE
    # ---------------------------------------------------------

    def delete(
        self,
        network_id: str,
    ) -> bool:

        affected = self.database.execute(
            f"""
            DELETE FROM {self.TABLE_NAME}
            WHERE network_id = ?
            """,
            (network_id,),
        )

        return affected > 0

    # ---------------------------------------------------------
    # STATE OPERATIONS
    # ---------------------------------------------------------

    def set_active(
        self,
        network_id: str,
    ) -> Optional[NetworkInfo]:

        return self.update(
            network_id,
            status="ACTIVE",
        )

    def set_maintenance(
        self,
        network_id: str,
    ) -> Optional[NetworkInfo]:

        return self.update(
            network_id,
            status="MAINTENANCE",
        )

    def suspend(
        self,
        network_id: str,
    ) -> Optional[NetworkInfo]:

        return self.update(
            network_id,
            status="SUSPENDED",
        )

    def set_offline(
        self,
        network_id: str,
    ) -> Optional[NetworkInfo]:

        return self.update(
            network_id,
            status="OFFLINE",
        )


__all__ = [
    "NetworkService",
]
