"""
MUKTI MAHAL OPERATIONS API

Live API for:
- Divisions
- Projects
- Work
"""

from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from backend.supreme.ecosystem.mukti_mahal.operations.controller import (
    MuktiMahalOperationsController,
)


router = APIRouter(
    prefix="/mukti-mahal",
    tags=["Mukti Mahal"],
)


controller = MuktiMahalOperationsController()


# =========================================================
# REQUEST MODELS
# =========================================================

class DivisionCreateRequest(BaseModel):
    mahal_id: str
    name: str
    division_type: str
    description: str = ""


class DivisionUpdateRequest(BaseModel):
    name: Optional[str] = None
    division_type: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None


class ProjectCreateRequest(BaseModel):
    mahal_id: str
    division_id: str
    name: str
    project_type: str
    description: str = ""
    budget: float = Field(default=0.0, ge=0.0)


class ProjectUpdateRequest(BaseModel):
    name: Optional[str] = None
    project_type: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    budget: Optional[float] = Field(default=None, ge=0.0)


class WorkCreateRequest(BaseModel):
    mahal_id: str
    project_id: str
    title: str
    work_type: str
    worker_id: Optional[str] = None
    description: str = ""
    compensation_type: str = "FIXED"
    compensation_amount: float = Field(default=0.0, ge=0.0)


class WorkUpdateRequest(BaseModel):
    worker_id: Optional[str] = None
    title: Optional[str] = None
    work_type: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    compensation_type: Optional[str] = None
    compensation_amount: Optional[float] = Field(
        default=None,
        ge=0.0,
    )


# =========================================================
# SERIALIZATION
# =========================================================

def _to_dict(item):

    if item is None:
        return None

    if hasattr(item, "__dataclass_fields__"):
        return {
            key: getattr(item, key)
            for key in item.__dataclass_fields__
        }

    return item


def _list_to_dict(items):

    return [_to_dict(item) for item in items]


# =========================================================
# STATUS
# =========================================================

@router.get("/")
def mukti_mahal_status():

    return controller.status()


@router.get("/status")
def mukti_mahal_operations_status():

    return controller.status()


# =========================================================
# DIVISIONS
# =========================================================

@router.post("/divisions")
def create_division(request: DivisionCreateRequest):

    try:
        division = controller.create_division(
            mahal_id=request.mahal_id,
            name=request.name,
            division_type=request.division_type,
            description=request.description,
        )

        return {
            "status": "CREATED",
            "data": _to_dict(division),
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"{type(exc).__name__}: {exc}",
        )


@router.get("/divisions")
def list_divisions(
    mahal_id: Optional[str] = None,
    status: Optional[str] = None,
):

    return {
        "status": "LIVE",
        "count": len(
            controller.list_divisions(
                mahal_id=mahal_id,
                status=status,
            )
        ),
        "data": _list_to_dict(
            controller.list_divisions(
                mahal_id=mahal_id,
                status=status,
            )
        ),
    }


@router.get("/divisions/{division_id}")
def get_division(division_id: str):

    division = controller.get_division(division_id)

    if not division:
        raise HTTPException(
            status_code=404,
            detail="Division not found",
        )

    return {
        "status": "LIVE",
        "data": _to_dict(division),
    }


@router.put("/divisions/{division_id}")
def update_division(
    division_id: str,
    request: DivisionUpdateRequest,
):

    division = controller.update_division(
        division_id=division_id,
        name=request.name,
        division_type=request.division_type,
        description=request.description,
        status=request.status,
    )

    if not division:
        raise HTTPException(
            status_code=404,
            detail="Division not found",
        )

    return {
        "status": "UPDATED",
        "data": _to_dict(division),
    }


@router.delete("/divisions/{division_id}")
def delete_division(division_id: str):

    deleted = controller.delete_division(division_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Division not found",
        )

    return {
        "status": "DELETED",
        "division_id": division_id,
    }


# =========================================================
# PROJECTS
# =========================================================

@router.post("/projects")
def create_project(request: ProjectCreateRequest):

    try:
        project = controller.create_project(
            mahal_id=request.mahal_id,
            division_id=request.division_id,
            name=request.name,
            project_type=request.project_type,
            description=request.description,
            budget=request.budget,
        )

        return {
            "status": "CREATED",
            "data": _to_dict(project),
        }

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"{type(exc).__name__}: {exc}",
        )


@router.get("/projects")
def list_projects(
    mahal_id: Optional[str] = None,
    division_id: Optional[str] = None,
    status: Optional[str] = None,
):

    projects = controller.list_projects(
        mahal_id=mahal_id,
        division_id=division_id,
        status=status,
    )

    return {
        "status": "LIVE",
        "count": len(projects),
        "data": _list_to_dict(projects),
    }


@router.get("/projects/{project_id}")
def get_project(project_id: str):

    project = controller.get_project(project_id)

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found",
        )

    return {
        "status": "LIVE",
        "data": _to_dict(project),
    }


@router.put("/projects/{project_id}")
def update_project(
    project_id: str,
    request: ProjectUpdateRequest,
):

    project = controller.update_project(
        project_id=project_id,
        name=request.name,
        project_type=request.project_type,
        description=request.description,
        status=request.status,
        budget=request.budget,
    )

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found",
        )

    return {
        "status": "UPDATED",
        "data": _to_dict(project),
    }


@router.delete("/projects/{project_id}")
def delete_project(project_id: str):

    deleted = controller.delete_project(project_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Project not found",
        )

    return {
        "status": "DELETED",
        "project_id": project_id,
    }


# =========================================================
# WORK
# =========================================================

@router.post("/work")
def create_work(request: WorkCreateRequest):

    try:
        work = controller.create_work(
            mahal_id=request.mahal_id,
            project_id=request.project_id,
            title=request.title,
            work_type=request.work_type,
            worker_id=request.worker_id,
            description=request.description,
            compensation_type=request.compensation_type,
            compensation_amount=request.compensation_amount,
        )

        return {
            "status": "CREATED",
            "data": _to_dict(work),
        }

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"{type(exc).__name__}: {exc}",
        )


@router.get("/work")
def list_work(
    mahal_id: Optional[str] = None,
    project_id: Optional[str] = None,
    worker_id: Optional[str] = None,
    status: Optional[str] = None,
):

    work = controller.list_work(
        mahal_id=mahal_id,
        project_id=project_id,
        worker_id=worker_id,
        status=status,
    )

    return {
        "status": "LIVE",
        "count": len(work),
        "data": _list_to_dict(work),
    }


@router.get("/work/{work_id}")
def get_work(work_id: str):

    work = controller.get_work(work_id)

    if not work:
        raise HTTPException(
            status_code=404,
            detail="Work not found",
        )

    return {
        "status": "LIVE",
        "data": _to_dict(work),
    }


@router.put("/work/{work_id}")
def update_work(
    work_id: str,
    request: WorkUpdateRequest,
):

    work = controller.update_work(
        work_id=work_id,
        worker_id=request.worker_id,
        title=request.title,
        work_type=request.work_type,
        description=request.description,
        status=request.status,
        compensation_type=request.compensation_type,
        compensation_amount=request.compensation_amount,
    )

    if not work:
        raise HTTPException(
            status_code=404,
            detail="Work not found",
        )

    return {
        "status": "UPDATED",
        "data": _to_dict(work),
    }


@router.delete("/work/{work_id}")
def delete_work(work_id: str):

    deleted = controller.delete_work(work_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Work not found",
        )

    return {
        "status": "DELETED",
        "work_id": work_id,
    }
