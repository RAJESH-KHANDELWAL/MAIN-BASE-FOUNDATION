"""DNS management API for MAIN BASE FOUNDATION."""

from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from backend.infrastructure.dns.controller import DNSController


router = APIRouter(
    prefix="/dns",
    tags=["DNS"],
)

controller = DNSController()


class DNSZoneCreateRequest(BaseModel):
    domain: str = Field(..., min_length=1)
    nameservers: list[str] = Field(default_factory=list)


class DNSRecordCreateRequest(BaseModel):
    zone_id: str = Field(..., min_length=1)
    record_type: str = Field(..., min_length=1)
    name: str = Field(..., min_length=1)
    content: str = Field(..., min_length=1)
    ttl: int = Field(default=300, ge=60)
    priority: Optional[int] = Field(default=None, ge=0)


@router.get("/")
def list_dns_zones():
    """Return all DNS zones."""

    return {
        "status": "RUNNING",
        "zones": controller.list_zones(),
    }


@router.post("/zones")
def create_dns_zone(
    request: DNSZoneCreateRequest,
):
    """Create a DNS zone."""

    try:
        return controller.create_zone(
            domain=request.domain,
            nameservers=request.nameservers,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=409,
            detail=str(exc),
        ) from exc


@router.get("/zones/{zone_id}")
def get_dns_zone(
    zone_id: str,
):
    """Return one DNS zone."""

    zone = controller.get_zone(zone_id)

    if not zone:
        raise HTTPException(
            status_code=404,
            detail="DNS zone not found",
        )

    return zone


@router.post("/records")
def add_dns_record(
    request: DNSRecordCreateRequest,
):
    """Add a DNS record to a zone."""

    try:
        return controller.add_record(
            zone_id=request.zone_id,
            record_type=request.record_type,
            name=request.name,
            content=request.content,
            ttl=request.ttl,
            priority=request.priority,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc


@router.delete("/records/{record_id}")
def delete_dns_record(
    record_id: str,
):
    """Delete a DNS record."""

    deleted = controller.delete_record(
        record_id
    )

    return {
        "deleted": deleted,
        "record_id": record_id,
    }
