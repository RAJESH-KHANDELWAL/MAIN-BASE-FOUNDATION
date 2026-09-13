"""Billing infrastructure models."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass
class BillingInfo:
    billing_id: str
    name: str
    billing_type: str
    currency: str = "INR"
    amount: float = 0
    status: str = "PENDING"
    customer_id: str = ""
    invoice_number: str = ""
    payment_reference: str = ""
    description: str = ""
    created_at: str = ""
    updated_at: str = ""

    def __post_init__(self):
        now = datetime.now(timezone.utc).isoformat()

        if not self.created_at:
            self.created_at = now

        if not self.updated_at:
            self.updated_at = now

    def to_dict(self) -> dict:
        return {
            "billing_id": self.billing_id,
            "name": self.name,
            "billing_type": self.billing_type,
            "currency": self.currency,
            "amount": self.amount,
            "status": self.status,
            "customer_id": self.customer_id,
            "invoice_number": self.invoice_number,
            "payment_reference": self.payment_reference,
            "description": self.description,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
