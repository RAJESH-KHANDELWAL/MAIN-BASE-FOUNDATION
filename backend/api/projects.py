"""Projects API for MAIN-BASE-FOUNDATION."""

from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from backend.projects.controller import ProjectController


router = APIRouter(
    prefix="/projects",
    tags=["Projects"],
)

controller = ProjectController()


class ProjectCreateRequest(BaseModel):
    owner_id: str = Field(..., min_length=1)
    name: str = Field(..., min_length=1)
    description: str = ""
    project_type: str = "GENERAL"
    status: str = "ACTIVE"
    visibility: str = "PRIVATE"
    budget: Optional[float] = None
    currency: str = "INR"
    deadline: Optional[str] = None


class ProjectUpdateRequest(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    project_type: Optional[str] = None
    status: Optional[str] = None
    visibility: Optional[str] = None
    budget: Optional[float] = None
    currency: Optional[str] = None
    deadline: Optional[str] = None


class ProjectStatusRequest(BaseModel):
    status: str = Field(..., min_length=1)


@router.get("/")
def get_projects(
    owner_id: Optional[str] = None,
    status: Optional[str] = None,
):
    projects = controller.list(
        owner_id=owner_id,
        status=status,
    )

    return {
        "message": "Projects fetched successfully.",
        "data": [
            project.to_dict()
            for project in projects
        ],
        "count": len(projects),
    }


@router.post("/")
def create_project(
    payload: ProjectCreateRequest,
):
    project = controller.create(
        owner_id=payload.owner_id,
        name=payload.name,
        description=payload.description,
        project_type=payload.project_type,
        status=payload.status,
        visibility=payload.visibility,
        budget=payload.budget,
        currency=payload.currency,
        deadline=payload.deadline,
    )

    return {
        "message": "Project created successfully.",
        "data": project.to_dict(),
    }


@router.get("/{project_id}")
def get_project(project_id: str):
    project = controller.get(project_id)

    if not project:
        raise HTTPException(
            status_code=404,
            detail="PROJECT_NOT_FOUND",
        )

    return {
        "message": "Project fetched successfully.",
        "data": project.to_dict(),
    }


@router.put("/{project_id}")
def update_project(
    project_id: str,
    payload: ProjectUpdateRequest,
):
    project = controller.update(
        project_id,
        name=payload.name,
        description=payload.description,
        project_type=payload.project_type,
        status=payload.status,
        visibility=payload.visibility,
        budget=payload.budget,
        currency=payload.currency,
        deadline=payload.deadline,
    )

    if not project:
        raise HTTPException(
            status_code=404,
            detail="PROJECT_NOT_FOUND",
        )

    return {
        "message": "Project updated successfully.",
        "data": project.to_dict(),
    }


@router.patch("/{project_id}/status")
def update_project_status(
    project_id: str,
    payload: ProjectStatusRequest,
):
    project = controller.update_status(
        project_id,
        payload.status,
    )

    if not project:
        raise HTTPException(
            status_code=404,
            detail="PROJECT_NOT_FOUND",
        )

    return {
        "message": "Project status updated successfully.",
        "data": project.to_dict(),
    }


@router.delete("/{project_id}")
def delete_project(project_id: str):
    deleted = controller.delete(project_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="PROJECT_NOT_FOUND",
        )

    return {
        "message": "Project deleted successfully.",
        "project_id": project_id,
        "deleted": True,
    }
