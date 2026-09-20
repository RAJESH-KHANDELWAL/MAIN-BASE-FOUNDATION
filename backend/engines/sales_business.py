from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Dict, List, Optional

from backend.engines.base import BaseEngine


class SalesStatus(str, Enum):
    NEW = "NEW"
    QUALIFIED = "QUALIFIED"
    PROPOSAL = "PROPOSAL"
    NEGOTIATION = "NEGOTIATION"
    WON = "WON"
    LOST = "LOST"
    CANCELLED = "CANCELLED"


@dataclass
class SalesOpportunity:
    opportunity_id: str
    lead_id: str
    customer_id: Optional[str]
    title: str
    description: str
    value: float
    currency: str = "INR"
    status: SalesStatus = SalesStatus.NEW
    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    updated_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


class SalesBusinessEngine(BaseEngine):
    def __init__(self):
        super().__init__("SALES_BUSINESS_ENGINE")
        self.opportunities: Dict[str, SalesOpportunity] = {}

    def create_opportunity(
        self,
        opportunity_id: str,
        lead_id: str,
        title: str,
        description: str,
        value: float,
        customer_id: Optional[str] = None,
        currency: str = "INR",
    ) -> SalesOpportunity:

        if opportunity_id in self.opportunities:
            raise ValueError("opportunity_id already exists.")

        if not lead_id.strip():
            raise ValueError("lead_id is required.")

        if not title.strip():
            raise ValueError("title is required.")

        if value <= 0:
            raise ValueError("value must be greater than zero.")

        opportunity = SalesOpportunity(
            opportunity_id=opportunity_id,
            lead_id=lead_id,
            customer_id=customer_id,
            title=title,
            description=description,
            value=value,
            currency=currency,
        )

        self.opportunities[opportunity_id] = opportunity

        return opportunity

    def update_status(
        self,
        opportunity_id: str,
        status: SalesStatus,
    ) -> SalesOpportunity:

        opportunity = self._get_opportunity(opportunity_id)

        opportunity.status = status
        opportunity.updated_at = datetime.now(timezone.utc)

        return opportunity

    def qualify(
        self,
        opportunity_id: str,
    ) -> SalesOpportunity:

        return self.update_status(
            opportunity_id,
            SalesStatus.QUALIFIED,
        )

    def create_proposal(
        self,
        opportunity_id: str,
    ) -> SalesOpportunity:

        return self.update_status(
            opportunity_id,
            SalesStatus.PROPOSAL,
        )

    def start_negotiation(
        self,
        opportunity_id: str,
    ) -> SalesOpportunity:

        return self.update_status(
            opportunity_id,
            SalesStatus.NEGOTIATION,
        )

    def mark_won(
        self,
        opportunity_id: str,
        customer_id: Optional[str] = None,
    ) -> SalesOpportunity:

        opportunity = self._get_opportunity(opportunity_id)

        opportunity.status = SalesStatus.WON

        if customer_id:
            opportunity.customer_id = customer_id

        opportunity.updated_at = datetime.now(timezone.utc)

        return opportunity

    def mark_lost(
        self,
        opportunity_id: str,
    ) -> SalesOpportunity:

        return self.update_status(
            opportunity_id,
            SalesStatus.LOST,
        )

    def get_opportunity(
        self,
        opportunity_id: str,
    ) -> Optional[SalesOpportunity]:

        return self.opportunities.get(opportunity_id)

    def list_opportunities(
        self,
        status: Optional[SalesStatus] = None,
    ) -> List[SalesOpportunity]:

        opportunities = list(self.opportunities.values())

        if status is None:
            return opportunities

        return [
            opportunity
            for opportunity in opportunities
            if opportunity.status == status
        ]

    def search(
        self,
        lead_id: Optional[str] = None,
        customer_id: Optional[str] = None,
    ) -> List[SalesOpportunity]:

        results = []

        for opportunity in self.opportunities.values():

            lead_match = (
                lead_id is None
                or opportunity.lead_id == lead_id
            )

            customer_match = (
                customer_id is None
                or opportunity.customer_id == customer_id
            )

            if lead_match and customer_match:
                results.append(opportunity)

        return results

    def status(self) -> dict:

        return {
            "engine": self.name,
            "state": self.state,
            "opportunity_count": len(self.opportunities),
            "new_count": sum(
                1
                for item in self.opportunities.values()
                if item.status == SalesStatus.NEW
            ),
            "qualified_count": sum(
                1
                for item in self.opportunities.values()
                if item.status == SalesStatus.QUALIFIED
            ),
            "proposal_count": sum(
                1
                for item in self.opportunities.values()
                if item.status == SalesStatus.PROPOSAL
            ),
            "negotiation_count": sum(
                1
                for item in self.opportunities.values()
                if item.status == SalesStatus.NEGOTIATION
            ),
            "won_count": sum(
                1
                for item in self.opportunities.values()
                if item.status == SalesStatus.WON
            ),
            "lost_count": sum(
                1
                for item in self.opportunities.values()
                if item.status == SalesStatus.LOST
            ),
        }

    def _get_opportunity(
        self,
        opportunity_id: str,
    ) -> SalesOpportunity:

        opportunity = self.opportunities.get(opportunity_id)

        if opportunity is None:
            raise KeyError(
                f"Unknown opportunity_id: {opportunity_id}"
            )

        return opportunity


__all__ = [
    "SalesStatus",
    "SalesOpportunity",
    "SalesBusinessEngine",
]
