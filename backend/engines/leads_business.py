from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Dict, List, Optional

from backend.engines.base import BaseEngine


class LeadStatus(str, Enum):
    NEW = "NEW"
    VERIFIED = "VERIFIED"
    CONTACTED = "CONTACTED"
    QUALIFIED = "QUALIFIED"
    CONVERTED = "CONVERTED"
    REJECTED = "REJECTED"
    ARCHIVED = "ARCHIVED"


class LeadSourceType(str, Enum):
    PUBLIC_BUSINESS_DATA = "PUBLIC_BUSINESS_DATA"
    BUSINESS_SUBMITTED = "BUSINESS_SUBMITTED"
    PLATFORM_REFERRAL = "PLATFORM_REFERRAL"
    PARTNER = "PARTNER"


@dataclass
class BusinessLead:
    lead_id: str
    business_name: str
    category: str
    location: str
    website: Optional[str] = None
    public_contact: Optional[str] = None
    social_profile: Optional[str] = None
    source: LeadSourceType = LeadSourceType.PUBLIC_BUSINESS_DATA
    status: LeadStatus = LeadStatus.NEW
    last_verified_at: Optional[datetime] = None
    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


class LeadsBusinessEngine(BaseEngine):

    def __init__(self):
        super().__init__("LEADS_BUSINESS_ENGINE")
        self.leads: Dict[str, BusinessLead] = {}

    def create_lead(
        self,
        lead_id: str,
        business_name: str,
        category: str,
        location: str,
        website: Optional[str] = None,
        public_contact: Optional[str] = None,
        social_profile: Optional[str] = None,
        source: LeadSourceType = LeadSourceType.PUBLIC_BUSINESS_DATA,
    ) -> BusinessLead:

        if lead_id in self.leads:
            raise ValueError("lead_id already exists.")

        if not business_name.strip():
            raise ValueError("business_name is required.")

        if not category.strip():
            raise ValueError("category is required.")

        if not location.strip():
            raise ValueError("location is required.")

        lead = BusinessLead(
            lead_id=lead_id,
            business_name=business_name,
            category=category,
            location=location,
            website=website,
            public_contact=public_contact,
            social_profile=social_profile,
            source=source,
        )

        self.leads[lead_id] = lead
        return lead

    def verify_lead(
        self,
        lead_id: str,
    ) -> BusinessLead:

        lead = self._get_lead(lead_id)

        lead.status = LeadStatus.VERIFIED
        lead.last_verified_at = datetime.now(timezone.utc)

        return lead

    def update_status(
        self,
        lead_id: str,
        status: LeadStatus,
    ) -> BusinessLead:

        lead = self._get_lead(lead_id)
        lead.status = status

        return lead

    def get_lead(
        self,
        lead_id: str,
    ) -> Optional[BusinessLead]:

        return self.leads.get(lead_id)

    def list_leads(
        self,
        status: Optional[LeadStatus] = None,
    ) -> List[BusinessLead]:

        leads = list(self.leads.values())

        if status is None:
            return leads

        return [
            lead
            for lead in leads
            if lead.status == status
        ]

    def search(
        self,
        category: Optional[str] = None,
        location: Optional[str] = None,
    ) -> List[BusinessLead]:

        results = []

        for lead in self.leads.values():

            category_match = (
                category is None
                or lead.category.lower() == category.lower()
            )

            location_match = (
                location is None
                or lead.location.lower() == location.lower()
            )

            if category_match and location_match:
                results.append(lead)

        return results

    def status(self) -> dict:

        return {
            "engine": self.name,
            "state": self.state,
            "lead_count": len(self.leads),
            "verified_count": sum(
                1
                for lead in self.leads.values()
                if lead.status == LeadStatus.VERIFIED
            ),
            "qualified_count": sum(
                1
                for lead in self.leads.values()
                if lead.status == LeadStatus.QUALIFIED
            ),
            "converted_count": sum(
                1
                for lead in self.leads.values()
                if lead.status == LeadStatus.CONVERTED
            ),
        }

    def _get_lead(
        self,
        lead_id: str,
    ) -> BusinessLead:

        lead = self.leads.get(lead_id)

        if lead is None:
            raise KeyError(
                f"Unknown lead_id: {lead_id}"
            )

        return lead


__all__ = [
    "LeadStatus",
    "LeadSourceType",
    "BusinessLead",
    "LeadsBusinessEngine",
]
