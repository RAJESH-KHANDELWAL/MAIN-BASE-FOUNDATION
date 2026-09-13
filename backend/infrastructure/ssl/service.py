"""SSL/TLS infrastructure service."""

from __future__ import annotations

from datetime import datetime, timezone

from backend.database.controller import DatabaseController

from .model import SSLInfo


class SSLService:
    def __init__(self):
        self.database = DatabaseController()
        self.initialize()

    def initialize(self) -> None:
        self.database.execute(
            """
            CREATE TABLE IF NOT EXISTS ssl_certificates (
                ssl_id TEXT PRIMARY KEY,
                domain TEXT NOT NULL,
                certificate_type TEXT DEFAULT 'TLS',
                issuer TEXT DEFAULT '',
                certificate_status TEXT DEFAULT 'PLANNED',
                expires_at TEXT DEFAULT '',
                auto_renew INTEGER DEFAULT 1,
                server_id TEXT DEFAULT '',
                provider TEXT DEFAULT '',
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )

    def create(
        self,
        domain: str,
        certificate_type: str = "TLS",
        issuer: str = "",
        certificate_status: str = "PLANNED",
        expires_at: str = "",
        auto_renew: bool = True,
        server_id: str = "",
        provider: str = "",
    ) -> SSLInfo:

        timestamp = datetime.now(timezone.utc).isoformat()

        row = self.database.fetchone(
            """
            SELECT COUNT(*) AS total
            FROM ssl_certificates
            """
        )

        number = int(row["total"]) + 1 if row else 1
        ssl_id = f"SSL-{number:06d}"

        self.database.execute(
            """
            INSERT INTO ssl_certificates (
                ssl_id,
                domain,
                certificate_type,
                issuer,
                certificate_status,
                expires_at,
                auto_renew,
                server_id,
                provider,
                created_at,
                updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                ssl_id,
                domain,
                certificate_type,
                issuer,
                certificate_status,
                expires_at,
                int(auto_renew),
                server_id,
                provider,
                timestamp,
                timestamp,
            ),
        )

        return SSLInfo(
            ssl_id=ssl_id,
            domain=domain,
            certificate_type=certificate_type,
            issuer=issuer,
            certificate_status=certificate_status,
            expires_at=expires_at,
            auto_renew=auto_renew,
            server_id=server_id,
            provider=provider,
            created_at=timestamp,
            updated_at=timestamp,
        )

    def get(self, ssl_id: str) -> SSLInfo | None:
        row = self.database.fetchone(
            """
            SELECT *
            FROM ssl_certificates
            WHERE ssl_id = ?
            """,
            (ssl_id,),
        )

        if not row:
            return None

        data = dict(row)
        data["auto_renew"] = bool(data["auto_renew"])

        return SSLInfo(**data)

    def list_all(self) -> list[SSLInfo]:
        rows = self.database.fetchall(
            """
            SELECT *
            FROM ssl_certificates
            ORDER BY created_at DESC
            """
        )

        result = []

        for row in rows:
            data = dict(row)
            data["auto_renew"] = bool(data["auto_renew"])
            result.append(SSLInfo(**data))

        return result

    def update_status(
        self,
        ssl_id: str,
        certificate_status: str,
    ) -> SSLInfo | None:

        timestamp = datetime.now(timezone.utc).isoformat()

        self.database.execute(
            """
            UPDATE ssl_certificates
            SET certificate_status = ?,
                updated_at = ?
            WHERE ssl_id = ?
            """,
            (
                certificate_status,
                timestamp,
                ssl_id,
            ),
        )

        return self.get(ssl_id)

    def update_auto_renew(
        self,
        ssl_id: str,
        auto_renew: bool,
    ) -> SSLInfo | None:

        timestamp = datetime.now(timezone.utc).isoformat()

        self.database.execute(
            """
            UPDATE ssl_certificates
            SET auto_renew = ?,
                updated_at = ?
            WHERE ssl_id = ?
            """,
            (
                int(auto_renew),
                timestamp,
                ssl_id,
            ),
        )

        return self.get(ssl_id)

    def delete(self, ssl_id: str) -> bool:
        row = self.database.fetchone(
            """
            SELECT ssl_id
            FROM ssl_certificates
            WHERE ssl_id = ?
            """,
            (ssl_id,),
        )

        if not row:
            return False

        self.database.execute(
            """
            DELETE FROM ssl_certificates
            WHERE ssl_id = ?
            """,
            (ssl_id,),
        )

        return True
