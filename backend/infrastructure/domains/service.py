"""
MAIN BASE FOUNDATION
Infrastructure - Domain Service

Domain lifecycle and persistence service.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional

from backend.database.connection import get_connection


class DomainService:
    """Service layer for domain infrastructure management."""

    def __init__(self):
        self.initialize()

    def initialize(self) -> None:
        """Create the domains table if it does not exist."""

        conn = get_connection()

        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS infrastructure_domains (
                domain_id TEXT PRIMARY KEY,
                domain_name TEXT NOT NULL UNIQUE,

                registrar TEXT,
                registration_status TEXT NOT NULL DEFAULT 'PENDING',
                nameserver_status TEXT NOT NULL DEFAULT 'PENDING',
                dns_status TEXT NOT NULL DEFAULT 'PENDING',

                hosting_id TEXT,
                server_id TEXT,
                ip_address_id TEXT,
                ssl_id TEXT,

                auto_renew INTEGER NOT NULL DEFAULT 1,
                verified INTEGER NOT NULL DEFAULT 0,
                status TEXT NOT NULL DEFAULT 'PENDING',

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
    def _next_domain_id(conn) -> str:
        row = conn.execute(
            """
            SELECT domain_id
            FROM infrastructure_domains
            ORDER BY domain_id DESC
            LIMIT 1
            """
        ).fetchone()

        if not row:
            return "DOM-000001"

        last_id = row["domain_id"]
        number = int(last_id.split("-")[1]) + 1

        return f"DOM-{number:06d}"

    @staticmethod
    def _serialize_metadata(metadata: Optional[Dict[str, Any]]) -> str:
        import json

        return json.dumps(metadata or {})

    @staticmethod
    def _deserialize_metadata(value: Optional[str]) -> Dict[str, Any]:
        import json

        if not value:
            return {}

        try:
            return json.loads(value)
        except (TypeError, ValueError):
            return {}

    def create_domain(
        self,
        domain_name: str,
        registrar: Optional[str] = None,
        auto_renew: bool = True,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Create a new domain record."""

        domain_name = domain_name.strip().lower()

        if not domain_name:
            raise ValueError("domain_name is required")

        conn = get_connection()

        existing = conn.execute(
            """
            SELECT domain_id
            FROM infrastructure_domains
            WHERE domain_name = ?
            """,
            (domain_name,),
        ).fetchone()

        if existing:
            raise ValueError("Domain already exists")

        now = self._now()
        domain_id = self._next_domain_id(conn)

        conn.execute(
            """
            INSERT INTO infrastructure_domains (
                domain_id,
                domain_name,
                registrar,
                registration_status,
                nameserver_status,
                dns_status,
                hosting_id,
                server_id,
                ip_address_id,
                ssl_id,
                auto_renew,
                verified,
                status,
                metadata,
                created_at,
                updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                domain_id,
                domain_name,
                registrar,
                "PENDING",
                "PENDING",
                "PENDING",
                None,
                None,
                None,
                None,
                int(auto_renew),
                0,
                "PENDING",
                self._serialize_metadata(metadata),
                now,
                now,
            ),
        )

        conn.commit()

        return self.get_domain(domain_id)

    def get_domain(self, domain_id: str) -> Optional[Dict[str, Any]]:
        """Return a domain by ID."""

        conn = get_connection()

        row = conn.execute(
            """
            SELECT *
            FROM infrastructure_domains
            WHERE domain_id = ?
            """,
            (domain_id,),
        ).fetchone()

        if not row:
            return None

        return self._row_to_dict(row)

    def get_by_name(self, domain_name: str) -> Optional[Dict[str, Any]]:
        """Return a domain by domain name."""

        conn = get_connection()

        row = conn.execute(
            """
            SELECT *
            FROM infrastructure_domains
            WHERE domain_name = ?
            """,
            (domain_name.strip().lower(),),
        ).fetchone()

        if not row:
            return None

        return self._row_to_dict(row)

    def list_domains(self) -> List[Dict[str, Any]]:
        """Return all managed domains."""

        conn = get_connection()

        rows = conn.execute(
            """
            SELECT *
            FROM infrastructure_domains
            ORDER BY created_at DESC
            """
        ).fetchall()

        return [self._row_to_dict(row) for row in rows]

    def update_domain(
        self,
        domain_id: str,
        **fields: Any,
    ) -> Optional[Dict[str, Any]]:
        """Update permitted domain infrastructure fields."""

        allowed_fields = {
            "registrar",
            "registration_status",
            "nameserver_status",
            "dns_status",
            "hosting_id",
            "server_id",
            "ip_address_id",
            "ssl_id",
            "auto_renew",
            "verified",
            "status",
            "metadata",
        }

        updates = []

        values = []

        for field_name, value in fields.items():

            if field_name not in allowed_fields:
                continue

            if field_name == "metadata":
                value = self._serialize_metadata(value)

            if field_name in {"auto_renew", "verified"}:
                value = int(bool(value))

            updates.append(f"{field_name} = ?")
            values.append(value)

        if not updates:
            return self.get_domain(domain_id)

        updates.append("updated_at = ?")
        values.append(self._now())
        values.append(domain_id)

        conn = get_connection()

        conn.execute(
            f"""
            UPDATE infrastructure_domains
            SET {", ".join(updates)}
            WHERE domain_id = ?
            """,
            values,
        )

        conn.commit()

        return self.get_domain(domain_id)

    def delete_domain(self, domain_id: str) -> bool:
        """Delete a domain record."""

        conn = get_connection()

        cursor = conn.execute(
            """
            DELETE FROM infrastructure_domains
            WHERE domain_id = ?
            """,
            (domain_id,),
        )

        conn.commit()

        return cursor.rowcount > 0

    def exists(self, domain_id: str) -> bool:
        """Check whether a domain exists."""

        conn = get_connection()

        row = conn.execute(
            """
            SELECT 1
            FROM infrastructure_domains
            WHERE domain_id = ?
            LIMIT 1
            """,
            (domain_id,),
        ).fetchone()

        return row is not None

    def attach_hosting(
        self,
        domain_id: str,
        hosting_id: str,
    ) -> Optional[Dict[str, Any]]:
        """Attach a hosting resource to a domain."""

        return self.update_domain(
            domain_id,
            hosting_id=hosting_id,
            status="HOSTING_CONNECTED",
        )

    def attach_server(
        self,
        domain_id: str,
        server_id: str,
    ) -> Optional[Dict[str, Any]]:
        """Attach a server resource to a domain."""

        return self.update_domain(
            domain_id,
            server_id=server_id,
        )

    def attach_ip(
        self,
        domain_id: str,
        ip_address_id: str,
    ) -> Optional[Dict[str, Any]]:
        """Attach an IPAM resource to a domain."""

        return self.update_domain(
            domain_id,
            ip_address_id=ip_address_id,
        )

    def attach_ssl(
        self,
        domain_id: str,
        ssl_id: str,
    ) -> Optional[Dict[str, Any]]:
        """Attach an SSL resource to a domain."""

        return self.update_domain(
            domain_id,
            ssl_id=ssl_id,
            status="SSL_ACTIVE",
        )

    def update_dns_status(
        self,
        domain_id: str,
        status: str,
    ) -> Optional[Dict[str, Any]]:
        """Update DNS lifecycle status."""

        return self.update_domain(
            domain_id,
            dns_status=status,
        )

    def update_nameserver_status(
        self,
        domain_id: str,
        status: str,
    ) -> Optional[Dict[str, Any]]:
        """Update nameserver lifecycle status."""

        return self.update_domain(
            domain_id,
            nameserver_status=status,
        )

    @classmethod
    def _row_to_dict(cls, row) -> Dict[str, Any]:
        return {
            "domain_id": row["domain_id"],
            "domain_name": row["domain_name"],
            "registrar": row["registrar"],
            "registration_status": row["registration_status"],
            "nameserver_status": row["nameserver_status"],
            "dns_status": row["dns_status"],
            "hosting_id": row["hosting_id"],
            "server_id": row["server_id"],
            "ip_address_id": row["ip_address_id"],
            "ssl_id": row["ssl_id"],
            "auto_renew": bool(row["auto_renew"]),
            "verified": bool(row["verified"]),
            "status": row["status"],
            "metadata": cls._deserialize_metadata(row["metadata"]),
            "created_at": row["created_at"],
            "updated_at": row["updated_at"],
        }
