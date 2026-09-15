"""
MUKTI MAHAL OPERATIONS CONTROLLER
"""

from typing import Optional

from .service import MuktiMahalOperationsService


class MuktiMahalOperationsController:

    def __init__(self):
        self.service = MuktiMahalOperationsService()

    # ---------------------------------------------------------
    # DIVISIONS
    # ---------------------------------------------------------

    def create_division(
        self,
        mahal_id: str,
        name: str,
        division_type: str,
        description: str = "",
    ):
        return self.service.create_division(
            mahal_id=mahal_id,
            name=name,
            division_type=division_type,
            description=description,
        )

    def get_division(self, division_id: str):
        return self.service.get_division(division_id)

    def list_divisions(
        self,
        mahal_id: Optional[str] = None,
        status: Optional[str] = None,
    ):
        return self.service.list_divisions(
            mahal_id=mahal_id,
            status=status,
        )

    def update_division(
        self,
        division_id: str,
        name: Optional[str] = None,
        division_type: Optional[str] = None,
        description: Optional[str] = None,
        status: Optional[str] = None,
    ):
        return self.service.update_division(
            division_id=division_id,
            name=name,
            division_type=division_type,
            description=description,
            status=status,
        )

    def delete_division(self, division_id: str):
        return self.service.delete_division(division_id)

    # ---------------------------------------------------------
    # PROJECTS
    # ---------------------------------------------------------

    def create_project(
        self,
        mahal_id: str,
        division_id: str,
        name: str,
        project_type: str,
        description: str = "",
        budget: float = 0.0,
    ):
        return self.service.create_project(
            mahal_id=mahal_id,
            division_id=division_id,
            name=name,
            project_type=project_type,
            description=description,
            budget=budget,
        )

    def get_project(self, project_id: str):
        return self.service.get_project(project_id)

    def list_projects(
        self,
        mahal_id: Optional[str] = None,
        division_id: Optional[str] = None,
        status: Optional[str] = None,
    ):
        return self.service.list_projects(
            mahal_id=mahal_id,
            division_id=division_id,
            status=status,
        )

    def update_project(
        self,
        project_id: str,
        name: Optional[str] = None,
        project_type: Optional[str] = None,
        description: Optional[str] = None,
        status: Optional[str] = None,
        budget: Optional[float] = None,
    ):
        return self.service.update_project(
            project_id=project_id,
            name=name,
            project_type=project_type,
            description=description,
            status=status,
            budget=budget,
        )

    def delete_project(self, project_id: str):
        return self.service.delete_project(project_id)

    # ---------------------------------------------------------
    # WORK
    # ---------------------------------------------------------

    def create_work(
        self,
        mahal_id: str,
        project_id: str,
        title: str,
        work_type: str,
        worker_id: Optional[str] = None,
        description: str = "",
        compensation_type: str = "FIXED",
        compensation_amount: float = 0.0,
    ):
        return self.service.create_work(
            mahal_id=mahal_id,
            project_id=project_id,
            title=title,
            work_type=work_type,
            worker_id=worker_id,
            description=description,
            compensation_type=compensation_type,
            compensation_amount=compensation_amount,
        )

    def get_work(self, work_id: str):
        return self.service.get_work(work_id)

    def list_work(
        self,
        mahal_id: Optional[str] = None,
        project_id: Optional[str] = None,
        worker_id: Optional[str] = None,
        status: Optional[str] = None,
    ):
        return self.service.list_work(
            mahal_id=mahal_id,
            project_id=project_id,
            worker_id=worker_id,
            status=status,
        )

    def update_work(
        self,
        work_id: str,
        worker_id: Optional[str] = None,
        title: Optional[str] = None,
        work_type: Optional[str] = None,
        description: Optional[str] = None,
        status: Optional[str] = None,
        compensation_type: Optional[str] = None,
        compensation_amount: Optional[float] = None,
    ):
        return self.service.update_work(
            work_id=work_id,
            worker_id=worker_id,
            title=title,
            work_type=work_type,
            description=description,
            status=status,
            compensation_type=compensation_type,
            compensation_amount=compensation_amount,
        )

    def delete_work(self, work_id: str):
        return self.service.delete_work(work_id)

    # ---------------------------------------------------------
    # STATUS
    # ---------------------------------------------------------

    def status(self):
        return self.service.status()
