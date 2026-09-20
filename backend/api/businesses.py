"""Business API routes for MAIN BASE FOUNDATION."""

from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel, Field

from backend.businesses.controller import BusinessController


router = APIRouter(
    prefix="/businesses",
    tags=["Businesses"],
)

controller = BusinessController()


class BusinessCreateRequest(BaseModel):
    owner_id: str
    name: str
    category: str = ""
    location: str = ""
    website: str = ""
    public_contact: str = ""
    source: str = ""
    status: str = "ACTIVE"
    verified: bool = False
    metadata: dict[str, Any] = Field(default_factory=dict)


class BusinessStatusRequest(BaseModel):
    status: str


@router.get("/")
def get_businesses():
    businesses = controller.list()

    return {
        "message": "Businesses retrieved successfully",
        "count": len(businesses),
        "data": [
            business.to_dict()
            for business in businesses
        ],
    }


@router.get("/{business_id}")
def get_business(business_id: str):
    business = controller.get(business_id)

    if business is None:
        return {
            "message": "Business not found",
            "data": None,
        }

    return {
        "message": "Business retrieved successfully",
        "data": business.to_dict(),
    }


@router.post("/")
def create_business(request: BusinessCreateRequest):
    business_id = f"BUS-{len(controller.list()) + 1:06d}"

    business = controller.create(
        business_id=business_id,
        owner_id=request.owner_id,
        name=request.name,
        category=request.category,
        location=request.location,
        website=request.website,
        public_contact=request.public_contact,
        source=request.source,
        status=request.status,
        verified=request.verified,
        metadata=request.metadata,
    )

    return {
        "message": "Business created successfully",
        "data": business.to_dict(),
    }


@router.put("/{business_id}/status")
def update_business_status(
    business_id: str,
    request: BusinessStatusRequest,
):
    business = controller.update_status(
        business_id=business_id,
        status=request.status,
    )

    if business is None:
        return {
            "message": "Business not found",
            "data": None,
        }

    return {
        "message": "Business status updated successfully",
        "data": business.to_dict(),
    }


@router.put("/{business_id}/verify")
def verify_business(business_id: str):
    business = controller.verify(business_id)

    if business is None:
        return {
            "message": "Business not found",
            "data": None,
        }

    return {
        "message": "Business verified successfully",
        "data": business.to_dict(),
    }


@router.delete("/{business_id}")
def delete_business(business_id: str):
    deleted = controller.delete(business_id)

    if not deleted:
        return {
            "message": "Business not found",
            "deleted": False,
        }

    return {
        "message": "Business deleted successfully",
        "deleted": True,
        "business_id": business_id,
    }
