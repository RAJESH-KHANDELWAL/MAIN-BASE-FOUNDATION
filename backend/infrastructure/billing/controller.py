"""Billing infrastructure controller."""

from .service import BillingService


class BillingController:
    def __init__(self):
        self.service = BillingService()

    def create(self, **kwargs) -> dict:
        billing = self.service.create(**kwargs)
        return billing.to_dict()

    def get(self, billing_id: str) -> dict | None:
        billing = self.service.get(billing_id)

        if not billing:
            return None

        return billing.to_dict()

    def list(self) -> list[dict]:
        return [
            billing.to_dict()
            for billing in self.service.list_all()
        ]

    def update_status(
        self,
        billing_id: str,
        status: str,
    ) -> dict | None:

        billing = self.service.update_status(
            billing_id,
            status,
        )

        if not billing:
            return None

        return billing.to_dict()

    def update_payment_reference(
        self,
        billing_id: str,
        payment_reference: str,
    ) -> dict | None:

        billing = self.service.update_payment_reference(
            billing_id,
            payment_reference,
        )

        if not billing:
            return None

        return billing.to_dict()

    def delete(self, billing_id: str) -> bool:
        return self.service.delete(billing_id)
