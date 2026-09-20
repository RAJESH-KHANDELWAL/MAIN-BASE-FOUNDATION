from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Dict, List, Optional

from backend.engines.base import BaseEngine


class CustomerStatus(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    SUSPENDED = "SUSPENDED"
    CLOSED = "CLOSED"


@dataclass
class Customer:
    customer_id: str
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    organization: Optional[str] = None
    source_opportunity_id: Optional[str] = None
    status: CustomerStatus = CustomerStatus.ACTIVE
    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    updated_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


class CustomerBusinessEngine(BaseEngine):
    def __init__(self):
        super().__init__("CUSTOMER_BUSINESS_ENGINE")
        self.customers: Dict[str, Customer] = {}

    def create_customer(
        self,
        customer_id: str,
        name: str,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        organization: Optional[str] = None,
        source_opportunity_id: Optional[str] = None,
    ) -> Customer:

        if customer_id in self.customers:
            raise ValueError("customer_id already exists.")

        if not name.strip():
            raise ValueError("name is required.")

        customer = Customer(
            customer_id=customer_id,
            name=name,
            email=email,
            phone=phone,
            organization=organization,
            source_opportunity_id=source_opportunity_id,
        )

        self.customers[customer_id] = customer

        return customer

    def update_status(
        self,
        customer_id: str,
        status: CustomerStatus,
    ) -> Customer:

        customer = self._get_customer(customer_id)

        customer.status = status
        customer.updated_at = datetime.now(timezone.utc)

        return customer

    def activate(
        self,
        customer_id: str,
    ) -> Customer:

        return self.update_status(
            customer_id,
            CustomerStatus.ACTIVE,
        )

    def deactivate(
        self,
        customer_id: str,
    ) -> Customer:

        return self.update_status(
            customer_id,
            CustomerStatus.INACTIVE,
        )

    def suspend(
        self,
        customer_id: str,
    ) -> Customer:

        return self.update_status(
            customer_id,
            CustomerStatus.SUSPENDED,
        )

    def close(
        self,
        customer_id: str,
    ) -> Customer:

        return self.update_status(
            customer_id,
            CustomerStatus.CLOSED,
        )

    def get_customer(
        self,
        customer_id: str,
    ) -> Optional[Customer]:

        return self.customers.get(customer_id)

    def list_customers(
        self,
        status: Optional[CustomerStatus] = None,
    ) -> List[Customer]:

        customers = list(self.customers.values())

        if status is None:
            return customers

        return [
            customer
            for customer in customers
            if customer.status == status
        ]

    def search(
        self,
        name: Optional[str] = None,
        organization: Optional[str] = None,
    ) -> List[Customer]:

        results = []

        for customer in self.customers.values():

            name_match = (
                name is None
                or name.lower() in customer.name.lower()
            )

            organization_match = (
                organization is None
                or (
                    customer.organization is not None
                    and organization.lower()
                    in customer.organization.lower()
                )
            )

            if name_match and organization_match:
                results.append(customer)

        return results

    def status(self) -> dict:

        return {
            "engine": self.name,
            "state": self.state,
            "customer_count": len(self.customers),
            "active_count": sum(
                1
                for customer in self.customers.values()
                if customer.status == CustomerStatus.ACTIVE
            ),
            "inactive_count": sum(
                1
                for customer in self.customers.values()
                if customer.status == CustomerStatus.INACTIVE
            ),
            "suspended_count": sum(
                1
                for customer in self.customers.values()
                if customer.status == CustomerStatus.SUSPENDED
            ),
            "closed_count": sum(
                1
                for customer in self.customers.values()
                if customer.status == CustomerStatus.CLOSED
            ),
        }

    def _get_customer(
        self,
        customer_id: str,
    ) -> Customer:

        customer = self.customers.get(customer_id)

        if customer is None:
            raise KeyError(
                f"Unknown customer_id: {customer_id}"
            )

        return customer


__all__ = [
    "CustomerStatus",
    "Customer",
    "CustomerBusinessEngine",
]
