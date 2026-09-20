"""Business controller for MAIN BASE FOUNDATION."""

from typing import Any

from backend.businesses.model import Business
from backend.businesses.service import BusinessService


class BusinessController:
    """Coordinates business-domain operations."""

    def __init__(self):
        self.service = BusinessService()

    def create(
        self,
        business_id: str,
        owner_id: str,
        name: str,
        category: str = "",
        location: str = "",
        website: str = "",
        public_contact: str = "",
        source: str = "",
        status: str = "ACTIVE",
        verified: bool = False,
        metadata: dict[str, Any] | None = None,
    ) -> Business:
        return self.service.create_business(
            business_id=business_id,
            owner_id=owner_id,
            name=name,
            category=category,
            location=location,
            website=website,
            public_contact=public_contact,
            source=source,
            status=status,
            verified=verified,
            metadata=metadata,
        )

    def get(self, business_id: str) -> Business | None:
        return self.service.get_business(business_id)

    def list(self) -> list[Business]:
        return self.service.list_businesses()

    def update_status(
        self,
        business_id: str,
        status: str,
    ) -> Business | None:
        return self.service.update_status(
            business_id=business_id,
            status=status,
        )

    def verify(self, business_id: str) -> Business | None:
        return self.service.verify_business(business_id)

    def delete(self, business_id: str) -> bool:
        return self.service.delete_business(business_id)
