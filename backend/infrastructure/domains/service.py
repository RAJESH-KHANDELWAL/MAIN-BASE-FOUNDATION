"""Domain infrastructure service."""

from __future__ import annotations

import json
from datetime import datetime, timezone

from backend.database.controller import DatabaseController

from .model import DomainInfo


class DomainService:
    def __init__(self):
        self.database = DatabaseController()
        self.initialize()

    def initialize(self) -> None:
        self.database.execute(
            """
            CREATE TABLE IF NOT EXISTS domains (
                domain_id TEXT PRIMARY KEY,
                domain TEXT NOT NULL UNIQUE,
                status TEXT DEFAULT 'PLANNED',
                registrar TEXT DEFAULT '',
                dns_zone_id TEXT DEFAULT '',
                nameservers TEXT DEFAULT '[]',
                registration_date TEXT DEFAULT '',
                expiry_date TEXT DEFAULT '',
                auto_renew INTEGER DEFAULT 1,
                verified INTEGER DEFAULT 0,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )

    def create(
        self,
        domain: str,
        status: str = "PLANNED",
        registrar: str = "",
        dns_zone_id: str = "",
        nameservers: list[str] | None = None,
        registration_date: str = "",
        expiry_date: str = "",
        auto_renew: bool = True,
        verified: bool = False,
    ) -> DomainInfo:

        timestamp = datetime.now(timezone.utc).isoformat()

        existing = self.database.fetchone(
            """
            SELECT domain_id
            FROM domains
            WHERE domain = ?
            """,
            (domain,),
        )

        if existing:
            raise ValueError("Domain already exists")

        row = self.database.fetchone(
            """
            SELECT COUNT(*) AS total
            FROM domains
            """
        )

        number = int(row["total"]) + 1 if row else 1
        domain_id = f"DOM-{number:06d}"

        if nameservers is None:
            nameservers = []

        self.database.execute(
            """
            INSERT INTO domains (
                domain_id,
                domain,
                status,
                registrar,
                dns_zone_id,
                nameservers,
                registration_date,
                expiry_date,
                auto_renew,
                verified,
                created_at,
                updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                domain_id,
                domain,
                status,
                registrar,
                dns_zone_id,
                json.dumps(nameservers),
                registration_date,
                expiry_date,
                int(auto_renew),
                int(verified),
                timestamp,
                timestamp,
            ),
        )

        return DomainInfo(
            domain_id=domain_id,
            domain=domain,
            status=status,
            registrar=registrar,
            dns_zone_id=dns_zone_id,
            nameservers=nameservers,
            registration_date=registration_date,
            expiry_date=expiry_date,
            auto_renew=auto_renew,
            verified=verified,
            created_at=timestamp,
            updated_at=timestamp,
        )

    def _row_to_model(self, row) -> DomainInfo:
        data = dict(row)

        try:
            nameservers = json.loads(data["nameservers"])
        except (TypeError, json.JSONDecodeError):
            nameservers = []

        data["nameservers"] = nameservers
        data["auto_renew"] = bool(data["auto_renew"])
        data["verified"] = bool(data["verified"])

        return DomainInfo(**data)

    def get(self, domain_id: str) -> DomainInfo | None:
        row = self.database.fetchone(
            """
            SELECT *
            FROM domains
            WHERE domain_id = ?
            """,
            (domain_id,),
        )

        if not row:
            return None

        return self._row_to_model(row)

    def get_by_domain(self, domain: str) -> DomainInfo | None:
        row = self.database.fetchone(
            """
            SELECT *
            FROM domains
            WHERE domain = ?
            """,
            (domain,),
        )

        if not row:
            return None

        return self._row_to_model(row)

    def list_all(self) -> list[DomainInfo]:
        rows = self.database.fetchall(
            """
            SELECT *
            FROM domains
            ORDER BY created_at DESC
            """
        )

        return [
            self._row_to_model(row)
            for row in rows
        ]

    def update_status(
        self,
        domain_id: str,
        status: str,
    ) -> DomainInfo | None:

        timestamp = datetime.now(timezone.utc).isoformat()

        self.database.execute(
            """
            UPDATE domains
            SET status = ?,
                updated_at = ?
            WHERE domain_id = ?
            """,
            (
                status,
                timestamp,
                domain_id,
            ),
        )

        return self.get(domain_id)

    def update_nameservers(
        self,
        domain_id: str,
        nameservers: list[str],
    ) -> DomainInfo | None:

        timestamp = datetime.now(timezone.utc).isoformat()

        self.database.execute(
            """
            UPDATE domains
            SET nameservers = ?,
                updated_at = ?
            WHERE domain_id = ?
            """,
            (
                json.dumps(nameservers),
                timestamp,
                domain_id,
            ),
        )

        return self.get(domain_id)

    def update_verification(
        self,
        domain_id: str,
        verified: bool,
    ) -> DomainInfo | None:

        timestamp = datetime.now(timezone.utc).isoformat()

        self.database.execute(
            """
            UPDATE domains
            SET verified = ?,
                updated_at = ?
            WHERE domain_id = ?
            """,
            (
                int(verified),
                timestamp,
                domain_id,
            ),
        )

        return self.get(domain_id)

    def delete(self, domain_id: str) -> bool:
        row = self.database.fetchone(
            """
            SELECT domain_id
            FROM domains
            WHERE domain_id = ?
            """,
            (domain_id,),
        )

        if not row:
            return False

        self.database.execute(
            """
            DELETE FROM domains
            WHERE domain_id = ?
            """,
            (domain_id,),
        )

        return True
