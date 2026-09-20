"""Business domain service for MAIN BASE FOUNDATION."""

from typing import Any

from backend.businesses.model import Business


class BusinessService:
    """Business-domain operations."""

    def __init__(self):
        self.businesses: dict[str, Business] = {}

    def create_business(
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
        if business_id in self.businesses:
            raise ValueError(f"Business already exists: {business_id}")

        business = Business(
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
            metadata=metadata or {},
        )

        self.businesses[business_id] = business
        return business

    def get_business(self, business_id: str) -> Business | None:
        return self.businesses.get(business_id)

    def list_businesses(self) -> list[Business]:
        return list(self.businesses.values())

    def update_status(
        self,
        business_id: str,
        status: str,
    ) -> Business | None:
        business = self.get_business(business_id)

        if business is None:
            return None

        business.status = status
        return business

    def verify_business(
        self,
        business_id: str,
    ) -> Business | None:
        business = self.get_business(business_id)

        if business is None:
            return None

        business.verified = True
        return business

    def delete_business(self, business_id: str) -> bool:
        if business_id not in self.businesses:
            return False

        del self.businesses[business_id]
        return True
