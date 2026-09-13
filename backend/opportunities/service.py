"""Persistence and business logic for work and business opportunities."""

from datetime import datetime, timezone
from typing import Optional

from backend.database.service import DatabaseService
from backend.opportunities.model import Opportunity


class OpportunityService:
    """Manage persistent work and business opportunities."""

    def __init__(self):
        self.database_service = DatabaseService()
        self.initialize()

    def initialize(self):
        self.database_service.initialize()

        self.database_service.execute(
            """
            CREATE TABLE IF NOT EXISTS opportunities (
                opportunity_id TEXT PRIMARY KEY,
                owner_id TEXT NOT NULL,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                opportunity_type TEXT NOT NULL,
                skills TEXT NOT NULL DEFAULT '',
                languages TEXT NOT NULL DEFAULT '',
                budget REAL NOT NULL DEFAULT 0,
                currency TEXT NOT NULL DEFAULT 'INR',
                deadline TEXT,
                status TEXT NOT NULL DEFAULT 'DRAFT',
                availability TEXT NOT NULL DEFAULT 'OPEN',
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )

        return {
            "success": True,
            "message": "Opportunity storage initialized",
        }

    @staticmethod
    def _split_values(value: str) -> list[str]:
        if not value:
            return []

        return [
            item.strip()
            for item in value.split(",")
            if item.strip()
        ]

    @staticmethod
    def _join_values(values: list[str]) -> str:
        return ",".join(
            str(value).strip()
            for value in values
            if str(value).strip()
        )

    def _row_to_opportunity(self, row) -> Opportunity:
        return Opportunity(
            opportunity_id=row["opportunity_id"],
            owner_id=row["owner_id"],
            title=row["title"],
            description=row["description"],
            opportunity_type=row["opportunity_type"],
            skills=self._split_values(row["skills"]),
            languages=self._split_values(row["languages"]),
            budget=float(row["budget"]),
            currency=row["currency"],
            deadline=row["deadline"],
            status=row["status"],
            availability=row["availability"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )

    def create_opportunity(
        self,
        opportunity_id: str,
        owner_id: str,
        title: str,
        description: str,
        opportunity_type: str,
        skills: list[str] | None = None,
        languages: list[str] | None = None,
        budget: float = 0.0,
        currency: str = "INR",
        deadline: Optional[str] = None,
        status: str = "LIVE",
        availability: str = "OPEN",
    ) -> Opportunity:

        now = datetime.now(timezone.utc).isoformat()

        opportunity = Opportunity(
            opportunity_id=opportunity_id,
            owner_id=owner_id,
            title=title,
            description=description,
            opportunity_type=opportunity_type,
            skills=skills or [],
            languages=languages or [],
            budget=budget,
            currency=currency,
            deadline=deadline,
            status=status,
            availability=availability,
            created_at=now,
            updated_at=now,
        )

        self.database_service.execute(
            """
            INSERT INTO opportunities (
                opportunity_id,
                owner_id,
                title,
                description,
                opportunity_type,
                skills,
                languages,
                budget,
                currency,
                deadline,
                status,
                availability,
                created_at,
                updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                opportunity.opportunity_id,
                opportunity.owner_id,
                opportunity.title,
                opportunity.description,
                opportunity.opportunity_type,
                self._join_values(opportunity.skills),
                self._join_values(opportunity.languages),
                opportunity.budget,
                opportunity.currency,
                opportunity.deadline,
                opportunity.status,
                opportunity.availability,
                opportunity.created_at,
                opportunity.updated_at,
            ),
        )

        return opportunity

    def get_opportunity(
        self,
        opportunity_id: str,
    ) -> Optional[Opportunity]:

        row = self.database_service.fetchone(
            """
            SELECT *
            FROM opportunities
            WHERE opportunity_id = ?
            """,
            (opportunity_id,),
        )

        if row is None:
            return None

        return self._row_to_opportunity(row)

    def get_all_opportunities(self) -> list[Opportunity]:
        rows = self.database_service.fetchall(
            """
            SELECT *
            FROM opportunities
            ORDER BY created_at DESC
            """
        )

        return [
            self._row_to_opportunity(row)
            for row in rows
        ]

    def get_live_opportunities(self) -> list[Opportunity]:
        rows = self.database_service.fetchall(
            """
            SELECT *
            FROM opportunities
            WHERE status = 'LIVE'
              AND availability = 'OPEN'
            ORDER BY created_at DESC
            """
        )

        return [
            self._row_to_opportunity(row)
            for row in rows
        ]

    def update_status(
        self,
        opportunity_id: str,
        status: str,
    ) -> Optional[Opportunity]:

        opportunity = self.get_opportunity(opportunity_id)

        if opportunity is None:
            return None

        now = datetime.now(timezone.utc).isoformat()

        self.database_service.execute(
            """
            UPDATE opportunities
            SET status = ?, updated_at = ?
            WHERE opportunity_id = ?
            """,
            (
                status,
                now,
                opportunity_id,
            ),
        )

        return self.get_opportunity(opportunity_id)


__all__ = ["OpportunityService"]
