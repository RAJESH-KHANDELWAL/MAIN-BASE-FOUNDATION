"""Business domain models for MAIN BASE FOUNDATION."""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Business:
    business_id: str
    owner_id: str
    name: str
    category: str = ""
    location: str = ""
    website: str = ""
    public_contact: str = ""
    source: str = ""
    status: str = "ACTIVE"
    verified: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "business_id": self.business_id,
            "owner_id": self.owner_id,
            "name": self.name,
            "category": self.category,
            "location": self.location,
            "website": self.website,
            "public_contact": self.public_contact,
            "source": self.source,
            "status": self.status,
            "verified": self.verified,
            "metadata": self.metadata,
        }
