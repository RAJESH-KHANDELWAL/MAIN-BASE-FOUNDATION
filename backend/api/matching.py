"""API for matching people with live opportunities."""

from fastapi import APIRouter
from pydantic import BaseModel, Field

from backend.matching.controller import MatchingController
from backend.matching.model import MatchingProfile


router = APIRouter(
    prefix="/matching",
    tags=["Matching"],
)

controller = MatchingController()


class MatchingRequest(BaseModel):
    person_id: str
    skills: list[str] = Field(default_factory=list)
    interests: list[str] = Field(default_factory=list)
    languages: list[str] = Field(default_factory=list)
    minimum_budget: float = 0.0
    availability: str = "AVAILABLE"
    minimum_score: float = 40.0


@router.post("/opportunities")
def match_opportunities(
    request: MatchingRequest,
):
    profile = MatchingProfile(
        person_id=request.person_id,
        skills=request.skills,
        interests=request.interests,
        languages=request.languages,
        minimum_budget=request.minimum_budget,
        availability=request.availability,
    )

    matches = controller.service.find_matches(
        profile,
        minimum_score=request.minimum_score,
    )

    return {
        "message": "Opportunity matching completed successfully",
        "person_id": request.person_id,
        "match_count": len(matches),
        "data": [
            match.to_dict()
            for match in matches
        ],
    }
