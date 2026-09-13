"""Matching logic for live opportunities."""

from backend.matching.model import (
    MatchingProfile,
    OpportunityMatch,
)
from backend.opportunities.service import OpportunityService


class MatchingService:
    """Match available people with relevant live opportunities."""

    def __init__(self):
        self.opportunity_service = OpportunityService()

    @staticmethod
    def _normalize(values: list[str]) -> set[str]:
        return {
            str(value).strip().lower()
            for value in values
            if str(value).strip()
        }

    def calculate_match(
        self,
        profile: MatchingProfile,
        opportunity,
    ) -> OpportunityMatch:

        worker_skills = self._normalize(profile.skills)
        worker_interests = self._normalize(profile.interests)
        worker_languages = self._normalize(profile.languages)

        opportunity_skills = self._normalize(opportunity.skills)
        opportunity_languages = self._normalize(opportunity.languages)

        matched_skills = sorted(
            worker_skills.intersection(opportunity_skills)
        )

        matched_interests = sorted(
            worker_interests.intersection(opportunity_skills)
        )

        matched_languages = sorted(
            worker_languages.intersection(opportunity_languages)
        )

        score = 0.0

        if opportunity_skills:
            skill_ratio = (
                len(matched_skills) / len(opportunity_skills)
            )
            score += skill_ratio * 60

        if matched_interests:
            score += min(
                len(matched_interests) * 10,
                20,
            )

        if matched_languages:
            score += min(
                len(matched_languages) * 10,
                10,
            )

        if profile.minimum_budget <= opportunity.budget:
            score += 10

        if profile.availability.upper() == "AVAILABLE":
            score += 0

        score = min(round(score, 2), 100.0)

        return OpportunityMatch(
            opportunity=opportunity,
            score=score,
            matched_skills=matched_skills,
            matched_interests=matched_interests,
            matched_languages=matched_languages,
        )

    def find_matches(
        self,
        profile: MatchingProfile,
        minimum_score: float = 40.0,
    ) -> list[OpportunityMatch]:

        if profile.availability.upper() != "AVAILABLE":
            return []

        opportunities = (
            self.opportunity_service.get_live_opportunities()
        )

        matches = []

        for opportunity in opportunities:
            match = self.calculate_match(
                profile,
                opportunity,
            )

            if match.score >= minimum_score:
                matches.append(match)

        matches.sort(
            key=lambda item: item.score,
            reverse=True,
        )

        return matches


__all__ = ["MatchingService"]
