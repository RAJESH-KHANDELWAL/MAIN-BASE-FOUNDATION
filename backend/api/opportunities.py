"""API routes for work and business opportunities."""

from fastapi import APIRouter
from pydantic import BaseModel, Field

from backend.opportunities.controller import OpportunityController


router = APIRouter(
    prefix="/opportunities",
    tags=["Opportunities"],
)

controller = OpportunityController()


class OpportunityCreateRequest(BaseModel):
    owner_id: str
    title: str
    description: str
    opportunity_type: str = Field(
        default="WORK",
        description="WORK or BUSINESS",
    )
    skills: list[str] = Field(default_factory=list)
    languages: list[str] = Field(default_factory=list)
    budget: float = 0.0
    currency: str = "INR"
    deadline: str | None = None
    status: str = "LIVE"
    availability: str = "OPEN"


class OpportunityStatusRequest(BaseModel):
    status: str


@router.get("/")
def get_opportunities():
    opportunities = controller.list()

    return {
        "message": "Opportunities retrieved successfully",
        "data": [
            opportunity.to_dict()
            for opportunity in opportunities
        ],
    }


@router.get("/live")
def get_live_opportunities():
    opportunities = controller.live()

    return {
        "message": "Live opportunities retrieved successfully",
        "data": [
            opportunity.to_dict()
            for opportunity in opportunities
        ],
    }


@router.get("/{opportunity_id}")
def get_opportunity(opportunity_id: str):
    opportunity = controller.get(opportunity_id)

    if opportunity is None:
        return {
            "message": "Opportunity not found",
            "data": None,
        }

    return {
        "message": "Opportunity retrieved successfully",
        "data": opportunity.to_dict(),
    }


@router.post("/")
def create_opportunity(
    request: OpportunityCreateRequest,
):
    opportunity_id = controller.service.database_service.fetchone(
        """
        SELECT opportunity_id
        FROM opportunities
        ORDER BY rowid DESC
        LIMIT 1
        """
    )

    if opportunity_id is None:
        next_id = "OPP-000001"
    else:
        previous_id = opportunity_id["opportunity_id"]
        try:
            number = int(previous_id.split("-")[-1])
            next_id = f"OPP-{number + 1:06d}"
        except (ValueError, IndexError):
            next_id = "OPP-000001"

    opportunity = controller.create(
        opportunity_id=next_id,
        owner_id=request.owner_id,
        title=request.title,
        description=request.description,
        opportunity_type=request.opportunity_type,
        skills=request.skills,
        languages=request.languages,
        budget=request.budget,
        currency=request.currency,
        deadline=request.deadline,
        status=request.status,
        availability=request.availability,
    )

    return {
        "message": "Opportunity created successfully",
        "data": opportunity.to_dict(),
    }


@router.put("/{opportunity_id}/status")
def update_opportunity_status(
    opportunity_id: str,
    request: OpportunityStatusRequest,
):
    opportunity = controller.update_status(
        opportunity_id,
        request.status,
    )

    if opportunity is None:
        return {
            "message": "Opportunity not found",
            "data": None,
        }

    return {
        "message": "Opportunity status updated successfully",
        "data": opportunity.to_dict(),
    }
