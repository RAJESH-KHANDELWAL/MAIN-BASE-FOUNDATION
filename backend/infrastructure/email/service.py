"""Email infrastructure service."""

from __future__ import annotations

from datetime import datetime, timezone

from backend.database.controller import DatabaseController

from .model import EmailServiceInfo


class EmailService:
    def __init__(self):
        self.database = DatabaseController()
        self.initialize()

    def initialize(self) -> None:
        self.database.execute(
            """
            CREATE TABLE IF NOT EXISTS email_services (
                email_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                email_type TEXT NOT NULL,
                domain TEXT DEFAULT '',
                provider TEXT DEFAULT '',
                smtp_host TEXT DEFAULT '',
                smtp_port INTEGER DEFAULT 0,
                status TEXT DEFAULT 'PLANNED',
                ssl_enabled INTEGER DEFAULT 1,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )

    def create(
        self,
        name: str,
        email_type: str,
        domain: str = "",
        provider: str = "",
        smtp_host: str = "",
        smtp_port: int = 0,
        status: str = "PLANNED",
        ssl_enabled: bool = True,
    ) -> EmailServiceInfo:

        timestamp = datetime.now(timezone.utc).isoformat()

        row = self.database.fetchone(
            """
            SELECT COUNT(*) AS total
            FROM email_services
            """
        )

        number = int(row["total"]) + 1 if row else 1
        email_id = f"EMAIL-{number:06d}"

        self.database.execute(
            """
            INSERT INTO email_services (
                email_id,
                name,
                email_type,
                domain,
                provider,
                smtp_host,
                smtp_port,
                status,
                ssl_enabled,
                created_at,
                updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                email_id,
                name,
                email_type,
                domain,
                provider,
                smtp_host,
                smtp_port,
                status,
                int(ssl_enabled),
                timestamp,
                timestamp,
            ),
        )

        return EmailServiceInfo(
            email_id=email_id,
            name=name,
            email_type=email_type,
            domain=domain,
            provider=provider,
            smtp_host=smtp_host,
            smtp_port=smtp_port,
            status=status,
            ssl_enabled=ssl_enabled,
            created_at=timestamp,
            updated_at=timestamp,
        )

    def get(self, email_id: str) -> EmailServiceInfo | None:
        row = self.database.fetchone(
            """
            SELECT *
            FROM email_services
            WHERE email_id = ?
            """,
            (email_id,),
        )

        if not row:
            return None

        data = dict(row)
        data["ssl_enabled"] = bool(data["ssl_enabled"])

        return EmailServiceInfo(**data)

    def list_all(self) -> list[EmailServiceInfo]:
        rows = self.database.fetchall(
            """
            SELECT *
            FROM email_services
            ORDER BY created_at DESC
            """
        )

        result = []

        for row in rows:
            data = dict(row)
            data["ssl_enabled"] = bool(data["ssl_enabled"])

            result.append(
                EmailServiceInfo(**data)
            )

        return result

    def update_status(
        self,
        email_id: str,
        status: str,
    ) -> EmailServiceInfo | None:

        timestamp = datetime.now(timezone.utc).isoformat()

        self.database.execute(
            """
            UPDATE email_services
            SET status = ?,
                updated_at = ?
            WHERE email_id = ?
            """,
            (
                status,
                timestamp,
                email_id,
            ),
        )

        return self.get(email_id)

    def delete(self, email_id: str) -> bool:
        row = self.database.fetchone(
            """
            SELECT email_id
            FROM email_services
            WHERE email_id = ?
            """,
            (email_id,),
        )

        if not row:
            return False

        self.database.execute(
            """
            DELETE FROM email_services
            WHERE email_id = ?
            """,
            (email_id,),
        )

        return True
