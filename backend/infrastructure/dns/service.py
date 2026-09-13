"""DNS service layer."""

from __future__ import annotations

from datetime import datetime, timezone

from backend.database.controller import DatabaseController

from .model import DNSRecord, DNSZone


class DNSService:

    def __init__(self):
        self.database = DatabaseController()
        self.initialize()

    def initialize(self) -> None:

        self.database.execute(
            """
            CREATE TABLE IF NOT EXISTS dns_zones (
                zone_id TEXT PRIMARY KEY,
                domain TEXT NOT NULL UNIQUE,
                status TEXT DEFAULT 'ACTIVE',
                nameservers TEXT DEFAULT '',
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )

        self.database.execute(
            """
            CREATE TABLE IF NOT EXISTS dns_records (
                record_id TEXT PRIMARY KEY,
                zone_id TEXT NOT NULL,
                record_type TEXT NOT NULL,
                name TEXT NOT NULL,
                content TEXT NOT NULL,
                ttl INTEGER DEFAULT 300,
                priority INTEGER,
                enabled INTEGER DEFAULT 1,
                created_at TEXT NOT NULL,
                FOREIGN KEY(zone_id)
                    REFERENCES dns_zones(zone_id)
                    ON DELETE CASCADE
            )
            """
        )

    def create_zone(
        self,
        domain: str,
        nameservers: list[str] | None = None,
    ) -> DNSZone:

        existing = self.database.fetchone(
            """
            SELECT zone_id
            FROM dns_zones
            WHERE domain = ?
            """,
            (domain,),
        )

        if existing:
            raise ValueError(
                f"DNS zone already exists: {domain}"
            )

        count = self.database.fetchone(
            """
            SELECT COUNT(*) AS total
            FROM dns_zones
            """
        )

        zone_number = int(count["total"]) + 1

        zone_id = f"DNS-ZONE-{zone_number:06d}"

        now = datetime.now(timezone.utc).isoformat()

        zone = DNSZone(
            zone_id=zone_id,
            domain=domain,
            nameservers=nameservers or [],
            created_at=now,
            updated_at=now,
        )

        self.database.execute(
            """
            INSERT INTO dns_zones (
                zone_id,
                domain,
                status,
                nameservers,
                created_at,
                updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                zone.zone_id,
                zone.domain,
                zone.status,
                ",".join(zone.nameservers),
                zone.created_at,
                zone.updated_at,
            ),
        )

        return zone

    def get_zone(
        self,
        zone_id: str,
    ) -> DNSZone | None:

        row = self.database.fetchone(
            """
            SELECT *
            FROM dns_zones
            WHERE zone_id = ?
            """,
            (zone_id,),
        )

        if not row:
            return None

        record_rows = self.database.fetchall(
            """
            SELECT *
            FROM dns_records
            WHERE zone_id = ?
            ORDER BY created_at ASC
            """,
            (zone_id,),
        )

        records = [
            DNSRecord(
                record_id=item["record_id"],
                zone_id=item["zone_id"],
                record_type=item["record_type"],
                name=item["name"],
                content=item["content"],
                ttl=item["ttl"],
                priority=item["priority"],
                enabled=bool(item["enabled"]),
                created_at=item["created_at"],
            )
            for item in record_rows
        ]

        nameservers = [
            item
            for item in (row["nameservers"] or "").split(",")
            if item
        ]

        return DNSZone(
            zone_id=row["zone_id"],
            domain=row["domain"],
            status=row["status"],
            nameservers=nameservers,
            records=records,
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )

    def list_zones(self) -> list[DNSZone]:

        rows = self.database.fetchall(
            """
            SELECT zone_id
            FROM dns_zones
            ORDER BY created_at DESC
            """
        )

        zones = []

        for row in rows:
            zone = self.get_zone(row["zone_id"])

            if zone:
                zones.append(zone)

        return zones

    def add_record(
        self,
        zone_id: str,
        record_type: str,
        name: str,
        content: str,
        ttl: int = 300,
        priority: int | None = None,
    ) -> DNSRecord:

        zone = self.get_zone(zone_id)

        if not zone:
            raise ValueError(
                f"DNS zone not found: {zone_id}"
            )

        count = self.database.fetchone(
            """
            SELECT COUNT(*) AS total
            FROM dns_records
            """
        )

        record_number = int(count["total"]) + 1

        record_id = f"DNS-RECORD-{record_number:06d}"

        now = datetime.now(timezone.utc).isoformat()

        record = DNSRecord(
            record_id=record_id,
            zone_id=zone_id,
            record_type=record_type.upper(),
            name=name,
            content=content,
            ttl=ttl,
            priority=priority,
            created_at=now,
        )

        self.database.execute(
            """
            INSERT INTO dns_records (
                record_id,
                zone_id,
                record_type,
                name,
                content,
                ttl,
                priority,
                enabled,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                record.record_id,
                record.zone_id,
                record.record_type,
                record.name,
                record.content,
                record.ttl,
                record.priority,
                1,
                record.created_at,
            ),
        )

        self.database.execute(
            """
            UPDATE dns_zones
            SET updated_at = ?
            WHERE zone_id = ?
            """,
            (now, zone_id),
        )

        return record

    def delete_record(
        self,
        record_id: str,
    ) -> bool:

        self.database.execute(
            """
            DELETE FROM dns_records
            WHERE record_id = ?
            """,
            (record_id,),
        )

        return True
