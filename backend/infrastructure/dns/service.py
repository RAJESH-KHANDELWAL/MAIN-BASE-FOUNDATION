"""
MAIN BASE FOUNDATION
Infrastructure - DNS Service

DNS zone and record lifecycle management.
"""

import datetime
import json
from typing import Any, Dict, List, Optional

from backend.database.connection import get_connection
from backend.infrastructure.dns.model import DNSRecordInfo, DNSZoneInfo


class DNSService:
    """
    Manages DNS zones and DNS records inside the
    infrastructure control plane.

    This service manages DNS configuration records.
    Actual authoritative DNS execution will be connected
    to the real DNS infrastructure later.
    """

    ALLOWED_ZONE_TYPES = {
        "PRIMARY",
        "SECONDARY",
    }

    ALLOWED_RECORD_TYPES = {
        "A",
        "AAAA",
        "CNAME",
        "MX",
        "TXT",
        "NS",
        "SRV",
        "CAA",
    }

    ALLOWED_STATUS = {
        "ACTIVE",
        "PENDING",
        "SUSPENDED",
        "DISABLED",
    }

    ALLOWED_DNS_STATUS = {
        "PENDING",
        "PROPAGATING",
        "ACTIVE",
        "FAILED",
    }

    TABLE_ZONE = "infrastructure_dns_zones"
    TABLE_RECORD = "infrastructure_dns_records"

    def __init__(self):
        self.initialize()

    def initialize(self) -> None:
        connection = get_connection()

        connection.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {self.TABLE_ZONE} (
                zone_id TEXT PRIMARY KEY,
                domain_name TEXT NOT NULL UNIQUE,

                zone_type TEXT NOT NULL,

                primary_nameserver TEXT,
                secondary_nameserver TEXT,

                nameserver_status TEXT NOT NULL,
                dns_status TEXT NOT NULL,

                status TEXT NOT NULL,
                verified INTEGER NOT NULL DEFAULT 0,

                metadata TEXT,

                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )

        connection.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {self.TABLE_RECORD} (
                record_id TEXT PRIMARY KEY,
                domain_name TEXT NOT NULL,

                record_type TEXT NOT NULL,
                record_name TEXT NOT NULL,
                record_value TEXT NOT NULL,

                ttl INTEGER NOT NULL DEFAULT 3600,
                priority INTEGER,

                status TEXT NOT NULL,
                verified INTEGER NOT NULL DEFAULT 0,

                metadata TEXT,

                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )

        connection.commit()

    def _next_zone_id(self) -> str:
        connection = get_connection()

        row = connection.execute(
            f"""
            SELECT zone_id
            FROM {self.TABLE_ZONE}
            ORDER BY rowid DESC
            LIMIT 1
            """
        ).fetchone()

        if not row:
            return "ZONE-000001"

        number = int(
            row["zone_id"].split("-")[-1]
        )

        return f"ZONE-{number + 1:06d}"

    def _next_record_id(self) -> str:
        connection = get_connection()

        row = connection.execute(
            f"""
            SELECT record_id
            FROM {self.TABLE_RECORD}
            ORDER BY rowid DESC
            LIMIT 1
            """
        ).fetchone()

        if not row:
            return "DNS-000001"

        number = int(
            row["record_id"].split("-")[-1]
        )

        return f"DNS-{number + 1:06d}"

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

    def _zone_to_model(self, row) -> DNSZoneInfo:
        return DNSZoneInfo(
            zone_id=row["zone_id"],
            domain_name=row["domain_name"],
            zone_type=row["zone_type"],
            primary_nameserver=row["primary_nameserver"],
            secondary_nameserver=row["secondary_nameserver"],
            nameserver_status=row["nameserver_status"],
            dns_status=row["dns_status"],
            status=row["status"],
            verified=bool(row["verified"]),
            metadata=self._deserialize_metadata(
                row["metadata"]
            ),
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )

    def _record_to_model(self, row) -> DNSRecordInfo:
        return DNSRecordInfo(
            record_id=row["record_id"],
            domain_name=row["domain_name"],
            record_type=row["record_type"],
            record_name=row["record_name"],
            record_value=row["record_value"],
            ttl=row["ttl"],
            priority=row["priority"],
            status=row["status"],
            verified=bool(row["verified"]),
            metadata=self._deserialize_metadata(
                row["metadata"]
            ),
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )

    # ---------------------------------------------------------
    # ZONES
    # ---------------------------------------------------------

    def create_zone(
        self,
        domain_name: str,
        zone_type: str = "PRIMARY",
        primary_nameserver: Optional[str] = None,
        secondary_nameserver: Optional[str] = None,
        nameserver_status: str = "PENDING",
        dns_status: str = "PENDING",
        status: str = "ACTIVE",
        verified: bool = False,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> DNSZoneInfo:

        if not domain_name:
            raise ValueError("Domain name is required")

        if zone_type not in self.ALLOWED_ZONE_TYPES:
            raise ValueError(
                f"Unsupported DNS zone type: {zone_type}"
            )

        if status not in self.ALLOWED_STATUS:
            raise ValueError(
                f"Unsupported DNS status: {status}"
            )

        if dns_status not in self.ALLOWED_DNS_STATUS:
            raise ValueError(
                f"Unsupported DNS lifecycle status: "
                f"{dns_status}"
            )

        zone_id = self._next_zone_id()
        now = datetime.datetime.utcnow().isoformat()

        connection = get_connection()

        connection.execute(
            f"""
            INSERT INTO {self.TABLE_ZONE} (
                zone_id,
                domain_name,
                zone_type,
                primary_nameserver,
                secondary_nameserver,
                nameserver_status,
                dns_status,
                status,
                verified,
                metadata,
                created_at,
                updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                zone_id,
                domain_name,
                zone_type,
                primary_nameserver,
                secondary_nameserver,
                nameserver_status,
                dns_status,
                status,
                int(verified),
                self._serialize_metadata(metadata),
                now,
                now,
            ),
        )

        connection.commit()

        return self.get_zone(zone_id)

    def get_zone(
        self,
        zone_id: str,
    ) -> Optional[DNSZoneInfo]:

        connection = get_connection()

        row = connection.execute(
            f"""
            SELECT *
            FROM {self.TABLE_ZONE}
            WHERE zone_id = ?
            """,
            (zone_id,),
        ).fetchone()

        if not row:
            return None

        return self._zone_to_model(row)

    def get_zone_by_domain(
        self,
        domain_name: str,
    ) -> Optional[DNSZoneInfo]:

        connection = get_connection()

        row = connection.execute(
            f"""
            SELECT *
            FROM {self.TABLE_ZONE}
            WHERE domain_name = ?
            """,
            (domain_name,),
        ).fetchone()

        if not row:
            return None

        return self._zone_to_model(row)

    def list_zones(
        self,
        status: Optional[str] = None,
    ) -> List[DNSZoneInfo]:

        connection = get_connection()

        if status:
            rows = connection.execute(
                f"""
                SELECT *
                FROM {self.TABLE_ZONE}
                WHERE status = ?
                ORDER BY rowid ASC
                """,
                (status,),
            ).fetchall()
        else:
            rows = connection.execute(
                f"""
                SELECT *
                FROM {self.TABLE_ZONE}
                ORDER BY rowid ASC
                """
            ).fetchall()

        return [
            self._zone_to_model(row)
            for row in rows
        ]

    def update_zone(
        self,
        zone_id: str,
        **updates,
    ) -> Optional[DNSZoneInfo]:

        current = self.get_zone(zone_id)

        if not current:
            return None

        allowed_fields = {
            "primary_nameserver",
            "secondary_nameserver",
            "nameserver_status",
            "dns_status",
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

        if "status" in updates:
            if updates["status"] not in self.ALLOWED_STATUS:
                raise ValueError(
                    f"Unsupported DNS status: "
                    f"{updates['status']}"
                )

        if "dns_status" in updates:
            if updates["dns_status"] not in self.ALLOWED_DNS_STATUS:
                raise ValueError(
                    f"Unsupported DNS lifecycle status: "
                    f"{updates['dns_status']}"
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
        values.append(zone_id)

        connection = get_connection()

        connection.execute(
            f"""
            UPDATE {self.TABLE_ZONE}
            SET {set_clause}
            WHERE zone_id = ?
            """,
            values,
        )

        connection.commit()

        return self.get_zone(zone_id)

    def delete_zone(
        self,
        zone_id: str,
    ) -> bool:

        connection = get_connection()

        cursor = connection.execute(
            f"""
            DELETE FROM {self.TABLE_ZONE}
            WHERE zone_id = ?
            """,
            (zone_id,),
        )

        connection.commit()

        return cursor.rowcount > 0

    # ---------------------------------------------------------
    # DNS RECORDS
    # ---------------------------------------------------------

    def create_record(
        self,
        domain_name: str,
        record_type: str,
        record_name: str,
        record_value: str,
        ttl: int = 3600,
        priority: Optional[int] = None,
        status: str = "ACTIVE",
        verified: bool = False,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> DNSRecordInfo:

        if not domain_name:
            raise ValueError("Domain name is required")

        if record_type not in self.ALLOWED_RECORD_TYPES:
            raise ValueError(
                f"Unsupported DNS record type: "
                f"{record_type}"
            )

        if not record_name:
            raise ValueError("Record name is required")

        if not record_value:
            raise ValueError("Record value is required")

        if ttl < 0:
            raise ValueError("TTL cannot be negative")

        if status not in self.ALLOWED_STATUS:
            raise ValueError(
                f"Unsupported DNS status: {status}"
            )

        record_id = self._next_record_id()
        now = datetime.datetime.utcnow().isoformat()

        connection = get_connection()

        connection.execute(
            f"""
            INSERT INTO {self.TABLE_RECORD} (
                record_id,
                domain_name,
                record_type,
                record_name,
                record_value,
                ttl,
                priority,
                status,
                verified,
                metadata,
                created_at,
                updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                record_id,
                domain_name,
                record_type,
                record_name,
                record_value,
                ttl,
                priority,
                status,
                int(verified),
                self._serialize_metadata(metadata),
                now,
                now,
            ),
        )

        connection.commit()

        return self.get_record(record_id)

    def get_record(
        self,
        record_id: str,
    ) -> Optional[DNSRecordInfo]:

        connection = get_connection()

        row = connection.execute(
            f"""
            SELECT *
            FROM {self.TABLE_RECORD}
            WHERE record_id = ?
            """,
            (record_id,),
        ).fetchone()

        if not row:
            return None

        return self._record_to_model(row)

    def list_records(
        self,
        domain_name: Optional[str] = None,
        record_type: Optional[str] = None,
    ) -> List[DNSRecordInfo]:

        connection = get_connection()

        conditions = []
        values = []

        if domain_name:
            conditions.append("domain_name = ?")
            values.append(domain_name)

        if record_type:
            conditions.append("record_type = ?")
            values.append(record_type)

        where_clause = ""

        if conditions:
            where_clause = (
                "WHERE " + " AND ".join(conditions)
            )

        rows = connection.execute(
            f"""
            SELECT *
            FROM {self.TABLE_RECORD}
            {where_clause}
            ORDER BY rowid ASC
            """,
            tuple(values),
        ).fetchall()

        return [
            self._record_to_model(row)
            for row in rows
        ]

    def update_record(
        self,
        record_id: str,
        **updates,
    ) -> Optional[DNSRecordInfo]:

        current = self.get_record(record_id)

        if not current:
            return None

        allowed_fields = {
            "record_name",
            "record_value",
            "ttl",
            "priority",
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

        if "ttl" in updates:
            if updates["ttl"] < 0:
                raise ValueError(
                    "TTL cannot be negative"
                )

        if "status" in updates:
            if updates["status"] not in self.ALLOWED_STATUS:
                raise ValueError(
                    f"Unsupported DNS status: "
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
        values.append(record_id)

        connection = get_connection()

        connection.execute(
            f"""
            UPDATE {self.TABLE_RECORD}
            SET {set_clause}
            WHERE record_id = ?
            """,
            values,
        )

        connection.commit()

        return self.get_record(record_id)

    def delete_record(
        self,
        record_id: str,
    ) -> bool:

        connection = get_connection()

        cursor = connection.execute(
            f"""
            DELETE FROM {self.TABLE_RECORD}
            WHERE record_id = ?
            """,
            (record_id,),
        )

        connection.commit()

        return cursor.rowcount > 0

    # ---------------------------------------------------------
    # DNS STATE OPERATIONS
    # ---------------------------------------------------------

    def activate_zone(
        self,
        zone_id: str,
    ) -> Optional[DNSZoneInfo]:

        return self.update_zone(
            zone_id,
            dns_status="ACTIVE",
            nameserver_status="ACTIVE",
            status="ACTIVE",
        )

    def set_zone_propagating(
        self,
        zone_id: str,
    ) -> Optional[DNSZoneInfo]:

        return self.update_zone(
            zone_id,
            dns_status="PROPAGATING",
        )

    def suspend_zone(
        self,
        zone_id: str,
    ) -> Optional[DNSZoneInfo]:

        return self.update_zone(
            zone_id,
            status="SUSPENDED",
        )

    def verify_zone(
        self,
        zone_id: str,
    ) -> Optional[DNSZoneInfo]:

        return self.update_zone(
            zone_id,
            verified=True,
        )

    def verify_record(
        self,
        record_id: str,
    ) -> Optional[DNSRecordInfo]:

        return self.update_record(
            record_id,
            verified=True,
        )
