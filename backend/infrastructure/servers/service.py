"""
MAIN BASE FOUNDATION
Infrastructure - Server Service

Server inventory and lifecycle service.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional
import json

from backend.database.connection import get_connection


class ServerService:
    """Service layer for server infrastructure."""

    ALLOWED_SERVER_TYPES = {
        "PHYSICAL",
        "VIRTUAL",
        "DEDICATED",
    }

    ALLOWED_STATUS = {
        "PROVISIONING",
        "ACTIVE",
        "MAINTENANCE",
        "SUSPENDED",
        "OFFLINE",
        "TERMINATED",
    }

    def __init__(self):
        self.initialize()

    def initialize(self) -> None:
        """Create the server inventory table."""

        conn = get_connection()

        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS infrastructure_servers (
                server_id TEXT PRIMARY KEY,
                server_type TEXT NOT NULL,

                name TEXT,
                provider TEXT,
                location TEXT,
                region TEXT,
                datacenter TEXT,

                ip_address_id TEXT,

                operating_system TEXT,
                control_panel TEXT,

                cpu_cores INTEGER,
                memory_gb REAL,
                storage_gb REAL,
                bandwidth_gb REAL,

                virtualization TEXT,

                status TEXT NOT NULL DEFAULT 'PROVISIONING',
                verified INTEGER NOT NULL DEFAULT 0,
                root_access INTEGER NOT NULL DEFAULT 0,

                metadata TEXT,

                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )

        conn.commit()

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

    @staticmethod
    def _next_server_id(conn) -> str:
        row = conn.execute(
            """
            SELECT server_id
            FROM infrastructure_servers
            ORDER BY server_id DESC
            LIMIT 1
            """
        ).fetchone()

        if not row:
            return "SRV-000001"

        number = int(row["server_id"].split("-")[1]) + 1

        return f"SRV-{number:06d}"

    def create_server(
        self,
        server_type: str,
        name: Optional[str] = None,
        provider: Optional[str] = None,
        location: Optional[str] = None,
        region: Optional[str] = None,
        datacenter: Optional[str] = None,
        ip_address_id: Optional[str] = None,
        operating_system: Optional[str] = None,
        control_panel: Optional[str] = None,
        cpu_cores: Optional[int] = None,
        memory_gb: Optional[float] = None,
        storage_gb: Optional[float] = None,
        bandwidth_gb: Optional[float] = None,
        virtualization: Optional[str] = None,
        root_access: bool = False,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Create a server inventory record."""

        server_type = server_type.strip().upper()

        if server_type not in self.ALLOWED_SERVER_TYPES:
            raise ValueError(
                "Invalid server_type. "
                "Use PHYSICAL, VIRTUAL, or DEDICATED."
            )

        conn = get_connection()

        server_id = self._next_server_id(conn)
        now = self._now()

        conn.execute(
            """
            INSERT INTO infrastructure_servers (
                server_id,
                server_type,
                name,
                provider,
                location,
                region,
                datacenter,
                ip_address_id,
                operating_system,
                control_panel,
                cpu_cores,
                memory_gb,
                storage_gb,
                bandwidth_gb,
                virtualization,
                status,
                verified,
                root_access,
                metadata,
                created_at,
                updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                server_id,
                server_type,
                name,
                provider,
                location,
                region,
                datacenter,
                ip_address_id,
                operating_system,
                control_panel,
                cpu_cores,
                memory_gb,
                storage_gb,
                bandwidth_gb,
                virtualization,
                "PROVISIONING",
                0,
                int(root_access),
                self._serialize_metadata(metadata),
                now,
                now,
            ),
        )

        conn.commit()

        return self.get_server(server_id)

    def get_server(
        self,
        server_id: str,
    ) -> Optional[Dict[str, Any]]:
        """Get a server by ID."""

        conn = get_connection()

        row = conn.execute(
            """
            SELECT *
            FROM infrastructure_servers
            WHERE server_id = ?
            """,
            (server_id,),
        ).fetchone()

        if not row:
            return None

        return self._row_to_dict(row)

    def list_servers(self) -> List[Dict[str, Any]]:
        """List all servers."""

        conn = get_connection()

        rows = conn.execute(
            """
            SELECT *
            FROM infrastructure_servers
            ORDER BY created_at DESC
            """
        ).fetchall()

        return [self._row_to_dict(row) for row in rows]

    def list_by_type(
        self,
        server_type: str,
    ) -> List[Dict[str, Any]]:
        """List servers by type."""

        server_type = server_type.strip().upper()

        if server_type not in self.ALLOWED_SERVER_TYPES:
            raise ValueError("Invalid server_type")

        conn = get_connection()

        rows = conn.execute(
            """
            SELECT *
            FROM infrastructure_servers
            WHERE server_type = ?
            ORDER BY created_at DESC
            """,
            (server_type,),
        ).fetchall()

        return [self._row_to_dict(row) for row in rows]

    def update_server(
        self,
        server_id: str,
        **fields: Any,
    ) -> Optional[Dict[str, Any]]:
        """Update permitted server fields."""

        allowed_fields = {
            "server_type",
            "name",
            "provider",
            "location",
            "region",
            "datacenter",
            "ip_address_id",
            "operating_system",
            "control_panel",
            "cpu_cores",
            "memory_gb",
            "storage_gb",
            "bandwidth_gb",
            "virtualization",
            "status",
            "verified",
            "root_access",
            "metadata",
        }

        updates = []
        values = []

        for field_name, value in fields.items():

            if field_name not in allowed_fields:
                continue

            if field_name == "server_type":
                value = str(value).strip().upper()

                if value not in self.ALLOWED_SERVER_TYPES:
                    raise ValueError("Invalid server_type")

            if field_name == "status":
                value = str(value).strip().upper()

                if value not in self.ALLOWED_STATUS:
                    raise ValueError("Invalid server status")

            if field_name in {
                "verified",
                "root_access",
            }:
                value = int(bool(value))

            if field_name == "metadata":
                value = self._serialize_metadata(value)

            updates.append(f"{field_name} = ?")
            values.append(value)

        if not updates:
            return self.get_server(server_id)

        updates.append("updated_at = ?")
        values.append(self._now())
        values.append(server_id)

        conn = get_connection()

        conn.execute(
            f"""
            UPDATE infrastructure_servers
            SET {", ".join(updates)}
            WHERE server_id = ?
            """,
            values,
        )

        conn.commit()

        return self.get_server(server_id)

    def attach_ip(
        self,
        server_id: str,
        ip_address_id: str,
    ) -> Optional[Dict[str, Any]]:
        """Attach an IPAM resource to a server."""

        return self.update_server(
            server_id,
            ip_address_id=ip_address_id,
        )

    def set_active(
        self,
        server_id: str,
    ) -> Optional[Dict[str, Any]]:
        """Mark a server as active."""

        return self.update_server(
            server_id,
            status="ACTIVE",
        )

    def set_maintenance(
        self,
        server_id: str,
    ) -> Optional[Dict[str, Any]]:
        """Put a server into maintenance."""

        return self.update_server(
            server_id,
            status="MAINTENANCE",
        )

    def suspend(
        self,
        server_id: str,
    ) -> Optional[Dict[str, Any]]:
        """Suspend a server."""

        return self.update_server(
            server_id,
            status="SUSPENDED",
        )

    def delete_server(
        self,
        server_id: str,
    ) -> bool:
        """Delete a server inventory record."""

        conn = get_connection()

        cursor = conn.execute(
            """
            DELETE FROM infrastructure_servers
            WHERE server_id = ?
            """,
            (server_id,),
        )

        conn.commit()

        return cursor.rowcount > 0

    def exists(
        self,
        server_id: str,
    ) -> bool:
        """Check whether a server exists."""

        conn = get_connection()

        row = conn.execute(
            """
            SELECT 1
            FROM infrastructure_servers
            WHERE server_id = ?
            LIMIT 1
            """,
            (server_id,),
        ).fetchone()

        return row is not None

    @classmethod
    def _row_to_dict(cls, row) -> Dict[str, Any]:
        return {
            "server_id": row["server_id"],
            "server_type": row["server_type"],
            "name": row["name"],
            "provider": row["provider"],
            "location": row["location"],
            "region": row["region"],
            "datacenter": row["datacenter"],
            "ip_address_id": row["ip_address_id"],
            "operating_system": row["operating_system"],
            "control_panel": row["control_panel"],
            "cpu_cores": row["cpu_cores"],
            "memory_gb": row["memory_gb"],
            "storage_gb": row["storage_gb"],
            "bandwidth_gb": row["bandwidth_gb"],
            "virtualization": row["virtualization"],
            "status": row["status"],
            "verified": bool(row["verified"]),
            "root_access": bool(row["root_access"]),
            "metadata": cls._deserialize_metadata(row["metadata"]),
            "created_at": row["created_at"],
            "updated_at": row["updated_at"],
        }
