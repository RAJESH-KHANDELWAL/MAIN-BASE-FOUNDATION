"""Billing infrastructure service."""

from __future__ import annotations

from datetime import datetime, timezone

from backend.database.controller import DatabaseController

from .model import BillingInfo


class BillingService:
    def __init__(self):
        self.database = DatabaseController()
        self.initialize()

    def initialize(self) -> None:
        self.database.execute(
            """
            CREATE TABLE IF NOT EXISTS billing (
                billing_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                billing_type TEXT NOT NULL,
                currency TEXT DEFAULT 'INR',
                amount REAL DEFAULT 0,
                status TEXT DEFAULT 'PENDING',
                customer_id TEXT DEFAULT '',
                invoice_number TEXT DEFAULT '',
                payment_reference TEXT DEFAULT '',
                description TEXT DEFAULT '',
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )

    def create(
        self,
        name: str,
        billing_type: str,
        currency: str = "INR",
        amount: float = 0,
        status: str = "PENDING",
        customer_id: str = "",
        invoice_number: str = "",
        payment_reference: str = "",
        description: str = "",
    ) -> BillingInfo:

        timestamp = datetime.now(timezone.utc).isoformat()

        row = self.database.fetchone(
            """
            SELECT COUNT(*) AS total
            FROM billing
            """
        )

        number = int(row["total"]) + 1 if row else 1
        billing_id = f"BILL-{number:06d}"

        self.database.execute(
            """
            INSERT INTO billing (
                billing_id,
                name,
                billing_type,
                currency,
                amount,
                status,
                customer_id,
                invoice_number,
                payment_reference,
                description,
                created_at,
                updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                billing_id,
                name,
                billing_type,
                currency,
                amount,
                status,
                customer_id,
                invoice_number,
                payment_reference,
                description,
                timestamp,
                timestamp,
            ),
        )

        return BillingInfo(
            billing_id=billing_id,
            name=name,
            billing_type=billing_type,
            currency=currency,
            amount=amount,
            status=status,
            customer_id=customer_id,
            invoice_number=invoice_number,
            payment_reference=payment_reference,
            description=description,
            created_at=timestamp,
            updated_at=timestamp,
        )

    def get(self, billing_id: str) -> BillingInfo | None:
        row = self.database.fetchone(
            """
            SELECT *
            FROM billing
            WHERE billing_id = ?
            """,
            (billing_id,),
        )

        if not row:
            return None

        return BillingInfo(**dict(row))

    def list_all(self) -> list[BillingInfo]:
        rows = self.database.fetchall(
            """
            SELECT *
            FROM billing
            ORDER BY created_at DESC
            """
        )

        return [
            BillingInfo(**dict(row))
            for row in rows
        ]

    def update_status(
        self,
        billing_id: str,
        status: str,
    ) -> BillingInfo | None:

        timestamp = datetime.now(timezone.utc).isoformat()

        self.database.execute(
            """
            UPDATE billing
            SET status = ?,
                updated_at = ?
            WHERE billing_id = ?
            """,
            (
                status,
                timestamp,
                billing_id,
            ),
        )

        return self.get(billing_id)

    def update_payment_reference(
        self,
        billing_id: str,
        payment_reference: str,
    ) -> BillingInfo | None:

        timestamp = datetime.now(timezone.utc).isoformat()

        self.database.execute(
            """
            UPDATE billing
            SET payment_reference = ?,
                updated_at = ?
            WHERE billing_id = ?
            """,
            (
                payment_reference,
                timestamp,
                billing_id,
            ),
        )

        return self.get(billing_id)

    def delete(self, billing_id: str) -> bool:
        row = self.database.fetchone(
            """
            SELECT billing_id
            FROM billing
            WHERE billing_id = ?
            """,
            (billing_id,),
        )

        if not row:
            return False

        self.database.execute(
            """
            DELETE FROM billing
            WHERE billing_id = ?
            """,
            (billing_id,),
        )

        return True
