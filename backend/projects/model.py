"""Project models for MAIN-BASE-FOUNDATION."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Project:
    project_id: str
    owner_id: str
    name: str
    description: str = ""
    project_type: str = "GENERAL"
    status: str = "ACTIVE"
    visibility: str = "PRIVATE"
    budget: Optional[float] = None
    currency: str = "INR"
    deadline: Optional[str] = None
    created_at: str = ""
    updated_at: str = ""

    def to_dict(self):
        return {
            "project_id": self.project_id,
            "owner_id": self.owner_id,
            "name": self.name,
            "description": self.description,
            "project_type": self.project_type,
            "status": self.status,
            "visibility": self.visibility,
            "budget": self.budget,
            "currency": self.currency,
            "deadline": self.deadline,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
