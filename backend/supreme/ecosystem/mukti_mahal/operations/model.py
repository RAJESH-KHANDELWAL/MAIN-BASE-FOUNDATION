"""
MUKTI MAHAL OPERATIONS MODELS
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class MuktiMahalDivision:
    division_id: str
    mahal_id: str
    name: str
    division_type: str
    description: str = ""
    status: str = "ACTIVE"
    created_at: str = ""


@dataclass
class MuktiMahalProject:
    project_id: str
    mahal_id: str
    division_id: str
    name: str
    project_type: str
    description: str = ""
    status: str = "PLANNED"
    budget: float = 0.0
    created_at: str = ""


@dataclass
class MuktiMahalWork:
    work_id: str
    mahal_id: str
    project_id: str
    worker_id: Optional[str]
    title: str
    work_type: str
    description: str = ""
    status: str = "ASSIGNED"
    compensation_type: str = "FIXED"
    compensation_amount: float = 0.0
    created_at: str = ""
    completed_at: Optional[str] = None
