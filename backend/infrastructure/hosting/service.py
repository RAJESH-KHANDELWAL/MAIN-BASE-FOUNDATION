"""
MAIN BASE FOUNDATION
Infrastructure - Hosting Service

Hosting resource lifecycle and persistence service.
"""

from __future__ import annotations

import json
from datetime import datetime
from typing import Any, Dict, List, Optional

from backend.database.service import DatabaseService


class HostingService:
    """Service layer for hosting infrastructure."""

    TABLE_NAME = "infrastructure_hosting"

    ALLOWED_HOSTING_TYPES = {
        "SHARED",
        "VIRTUAL_SERVER",
        "DEDICATED_SERVER",
    }

    ALLOWED_STATUS = {
        "PENDING",
        "PROVISIONING",
        "ACTIVE",
        "SUSPENDED",
        "MAINTENANCE",
        "TERMINATED",
    }

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
        """Create hosting infrastructure table."""

        self.database.initialize()

        self.database.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {self.TABLE_NAME} (
                hosting_id TEXT PRIMARY KEY,
                hosting_type TEXT NOT NULL,
                plan_name TEXT,
                domain_id TEXT,
                server_id TEXT,
                ip_address_id TEXT,
                control_panel TEXT,
                operating_system TEXT,
                storage_id TEXT,
                ssl_id TEXT,
                resource_status TEXT NOT NULL DEFAULT 'PROVISIONING',
                status TEXT NOT NULL DEFAULT 'PENDING',
                root_access INTEGER NOT NULL DEFAULT 0,
                dedicated_ip INTEGER NOT NULL DEFAULT 0,
                cpu_cores INTEGER,
                memory_gb REAL,
                storage_gb REAL,
                bandwidth_gb REAL,
                verified INTEGER NOT NULL DEFAULT 0,
                metadata TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )

    @staticmethod
    def _now() -> str:
        return datetime.utcnow().isoformat()

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

    def _next_hosting_id(self) -> str:
        row = self.database.fetchone(
            f"""
            SELECT hosting_id
            FROM {self.TABLE_NAME}
            ORDER BY rowid DESC
            LIMIT 1
            """
        )

        if not row:
            return "HOST-000001"

        number = int(
            row["hosting_id"].split("-")[1]
        ) + 1

        return f"HOST-{number:06d}"

    def create_hosting(
        self,
        hosting_type: str,
        plan_name: Optional[str] = None,
        domain_id: Optional[str] = None,
        server_id: Optional[str] = None,
        ip_address_id: Optional[str] = None,
        control_panel: Optional[str] = None,
        operating_system: Optional[str] = None,
        storage_id: Optional[str] = None,
        ssl_id: Optional[str] = None,
        root_access: bool = False,
        dedicated_ip: bool = False,
        cpu_cores: Optional[int] = None,
        memory_gb: Optional[float] = None,
        storage_gb: Optional[float] = None,
        bandwidth_gb: Optional[float] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Create a hosting resource."""

        hosting_type = hosting_type.strip().upper()

        if hosting_type not in self.ALLOWED_HOSTING_TYPES:
            raise ValueError(
                "Invalid hosting_type. "
                "Use SHARED, VIRTUAL_SERVER, or "
                "DEDICATED_SERVER."
            )

        hosting_id = self._next_hosting_id()
        now = self._now()

        self.database.execute(
            f"""
            INSERT INTO {self.TABLE_NAME} (
                hosting_id,
                hosting_type,
                plan_name,
                domain_id,
                server_id,
                ip_address_id,
                control_panel,
                operating_system,
                storage_id,
                ssl_id,
                resource_status,
                status,
                root_access,
                dedicated_ip,
                cpu_cores,
                memory_gb,
                storage_gb,
                bandwidth_gb,
                verified,
                metadata,
                created_at,
                updated_at
            )
            VALUES (
                ?, ?, ?, ?, ?, ?, ?, ?, ?,
                ?, ?, ?, ?, ?, ?, ?, ?, ?,
                ?, ?, ?, ?
            )
            """,
            (
                hosting_id,
                hosting_type,
                plan_name,
                domain_id,
                server_id,
                ip_address_id,
                control_panel,
                operating_system,
                storage_id,
                ssl_id,
                "PROVISIONING",
                "PENDING",
                int(root_access),
                int(dedicated_ip),
                cpu_cores,
                memory_gb,
                storage_gb,
                bandwidth_gb,
                0,
                self._serialize_metadata(metadata),
                now,
                now,
            ),
        )

        return self.get_hosting(hosting_id)

    def get_hosting(
        self,
        hosting_id: str,
    ) -> Optional[Dict[str, Any]]:
        """Get hosting resource by ID."""

        row = self.database.fetchone(
            f"""
            SELECT *
            FROM {self.TABLE_NAME}
            WHERE hosting_id = ?
            """,
            (hosting_id,),
        )

        if not row:
            return None

        return self._row_to_dict(row)

    def list_hosting(self) -> List[Dict[str, Any]]:
        """List all hosting resources."""

        rows = self.database.fetchall(
            f"""
            SELECT *
            FROM {self.TABLE_NAME}
            ORDER BY created_at DESC
            """
        )

        return [
            self._row_to_dict(row)
            for row in rows
        ]

    def list_by_type(
        self,
        hosting_type: str,
    ) -> List[Dict[str, Any]]:
        """List hosting resources by hosting type."""

        hosting_type = hosting_type.strip().upper()

        if hosting_type not in self.ALLOWED_HOSTING_TYPES:
            raise ValueError("Invalid hosting_type")

        rows = self.database.fetchall(
            f"""
            SELECT *
            FROM {self.TABLE_NAME}
            WHERE hosting_type = ?
            ORDER BY created_at DESC
            """,
            (hosting_type,),
        )

        return [
            self._row_to_dict(row)
            for row in rows
        ]

    def update_hosting(
        self,
        hosting_id: str,
        **fields: Any,
    ) -> Optional[Dict[str, Any]]:
        """Update permitted hosting fields."""

        allowed_fields = {
            "hosting_type",
            "plan_name",
            "domain_id",
            "server_id",
            "ip_address_id",
            "control_panel",
            "operating_system",
            "storage_id",
            "ssl_id",
            "resource_status",
            "status",
            "root_access",
            "dedicated_ip",
            "cpu_cores",
            "memory_gb",
            "storage_gb",
            "bandwidth_gb",
            "verified",
            "metadata",
        }

        updates = []
        values = []

        for field_name, value in fields.items():

            if field_name not in allowed_fields:
                continue

            if field_name == "hosting_type":
                value = str(value).strip().upper()

                if value not in self.ALLOWED_HOSTING_TYPES:
                    raise ValueError(
                        "Invalid hosting_type"
                    )

            if field_name == "status":
                value = str(value).strip().upper()

                if value not in self.ALLOWED_STATUS:
                    raise ValueError(
                        "Invalid hosting status"
                    )

            if field_name in {
                "root_access",
                "dedicated_ip",
                "verified",
            }:
                value = int(bool(value))

            if field_name == "metadata":
                value = self._serialize_metadata(value)

            updates.append(
                f"{field_name} = ?"
            )
            values.append(value)

        if not updates:
            return self.get_hosting(hosting_id)

        updates.append("updated_at = ?")
        values.append(self._now())
        values.append(hosting_id)

        self.database.execute(
            f"""
            UPDATE {self.TABLE_NAME}
            SET {", ".join(updates)}
            WHERE hosting_id = ?
            """,
            values,
        )

        return self.get_hosting(hosting_id)

    def attach_domain(
        self,
        hosting_id: str,
        domain_id: str,
    ) -> Optional[Dict[str, Any]]:
        """Attach a domain to hosting."""

        return self.update_hosting(
            hosting_id,
            domain_id=domain_id,
            status="ACTIVE",
        )

    def attach_server(
        self,
        hosting_id: str,
        server_id: str,
    ) -> Optional[Dict[str, Any]]:
        """Attach a server."""

        return self.update_hosting(
            hosting_id,
            server_id=server_id,
        )

    def attach_ip(
        self,
        hosting_id: str,
        ip_address_id: str,
    ) -> Optional[Dict[str, Any]]:
        """Attach an IPAM resource."""

        return self.update_hosting(
            hosting_id,
            ip_address_id=ip_address_id,
            dedicated_ip=True,
        )

    def attach_storage(
        self,
        hosting_id: str,
        storage_id: str,
    ) -> Optional[Dict[str, Any]]:
        """Attach storage."""

        return self.update_hosting(
            hosting_id,
            storage_id=storage_id,
        )

    def attach_ssl(
        self,
        hosting_id: str,
        ssl_id: str,
    ) -> Optional[Dict[str, Any]]:
        """Attach SSL."""

        return self.update_hosting(
            hosting_id,
            ssl_id=ssl_id,
        )

    def set_active(
        self,
        hosting_id: str,
    ) -> Optional[Dict[str, Any]]:
        """Mark hosting as active."""

        return self.update_hosting(
            hosting_id,
            resource_status="ACTIVE",
            status="ACTIVE",
        )

    def suspend(
        self,
        hosting_id: str,
    ) -> Optional[Dict[str, Any]]:
        """Suspend hosting."""

        return self.update_hosting(
            hosting_id,
            status="SUSPENDED",
        )

    def delete_hosting(
        self,
        hosting_id: str,
    ) -> bool:
        """Delete a hosting resource."""

        affected = self.database.execute(
            f"""
            DELETE FROM {self.TABLE_NAME}
            WHERE hosting_id = ?
            """,
            (hosting_id,),
        )

        return affected > 0

    def exists(
        self,
        hosting_id: str,
    ) -> bool:
        """Check whether hosting exists."""

        row = self.database.fetchone(
            f"""
            SELECT 1
            FROM {self.TABLE_NAME}
            WHERE hosting_id = ?
            LIMIT 1
            """,
            (hosting_id,),
        )

        return row is not None

    @classmethod
    def _row_to_dict(
        cls,
        row,
    ) -> Dict[str, Any]:
        return {
            "hosting_id": row["hosting_id"],
            "hosting_type": row["hosting_type"],
            "plan_name": row["plan_name"],
            "domain_id": row["domain_id"],
            "server_id": row["server_id"],
            "ip_address_id": row["ip_address_id"],
            "control_panel": row["control_panel"],
            "operating_system": row["operating_system"],
            "storage_id": row["storage_id"],
            "ssl_id": row["ssl_id"],
            "resource_status": row["resource_status"],
            "status": row["status"],
            "root_access": bool(row["root_access"]),
            "dedicated_ip": bool(row["dedicated_ip"]),
            "cpu_cores": row["cpu_cores"],
            "memory_gb": row["memory_gb"],
            "storage_gb": row["storage_gb"],
            "bandwidth_gb": row["bandwidth_gb"],
            "verified": bool(row["verified"]),
            "metadata": cls._deserialize_metadata(
                row["metadata"]
            ),
            "created_at": row["created_at"],
            "updated_at": row["updated_at"],
        }


__all__ = [
    "HostingService",
]
