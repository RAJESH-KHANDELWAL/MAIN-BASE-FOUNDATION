"""Models used by the matching engine."""

from dataclasses import dataclass, field

from backend.opportunities.model import Opportunity


@dataclass
class MatchingProfile:
    """Represent a person's work preferences and capabilities."""

    person_id: str
    skills: list[str] = field(default_factory=list)
    interests: list[str] = field(default_factory=list)
    languages: list[str] = field(default_factory=list)
    minimum_budget: float = 0.0
    availability: str = "AVAILABLE"

    def to_dict(self) -> dict:
        return {
            "person_id": self.person_id,
            "skills": self.skills,
            "interests": self.interests,
            "languages": self.languages,
            "minimum_budget": self.minimum_budget,
            "availability": self.availability,
        }


@dataclass
class OpportunityMatch:
    """Represent one opportunity matched to a person."""

    opportunity: Opportunity
    score: float
    matched_skills: list[str] = field(default_factory=list)
    matched_interests: list[str] = field(default_factory=list)
    matched_languages: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "opportunity": self.opportunity.to_dict(),
            "match_score": self.score,
            "matched_skills": self.matched_skills,
            "matched_interests": self.matched_interests,
            "matched_languages": self.matched_languages,
        }


__all__ = [
    "MatchingProfile",
    "OpportunityMatch",
]
