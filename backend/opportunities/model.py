"""Models for work and business opportunities."""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional


@dataclass
class Opportunity:
    opportunity_id: str
    owner_id: str
    title: str
    description: str
    opportunity_type: str
    skills: list[str] = field(default_factory=list)
    languages: list[str] = field(default_factory=list)
    budget: float = 0.0
    currency: str = "INR"
    deadline: Optional[str] = None
    status: str = "DRAFT"
    availability: str = "OPEN"
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    updated_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def to_dict(self) -> dict:
        return {
            "opportunity_id": self.opportunity_id,
            "owner_id": self.owner_id,
            "title": self.title,
            "description": self.description,
            "opportunity_type": self.opportunity_type,
            "skills": self.skills,
            "languages": self.languages,
            "budget": self.budget,
            "currency": self.currency,
            "deadline": self.deadline,
            "status": self.status,
            "availability": self.availability,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


__all__ = ["Opportunity"]
