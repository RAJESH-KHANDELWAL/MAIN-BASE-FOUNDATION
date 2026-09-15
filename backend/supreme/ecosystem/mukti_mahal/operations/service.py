"""
MUKTI MAHAL OPERATIONS SERVICE

Persistent operational database layer for:
- Divisions
- Projects
- Work

Uses the central MAIN BASE FOUNDATION DatabaseService.
"""

from datetime import datetime, timezone
from typing import Optional

from backend.database.service import DatabaseService

from .model import (
    MuktiMahalDivision,
    MuktiMahalProject,
    MuktiMahalWork,
)


class MuktiMahalOperationsService:

    def __init__(self):
        self.database = DatabaseService()
        self.initialize()

    # ---------------------------------------------------------
    # COMMON
    # ---------------------------------------------------------

    @staticmethod
    def _now() -> str:
        return datetime.now(timezone.utc).isoformat()

    @staticmethod
    def _next_id(prefix: str, table: str, column: str) -> str:
        """
        Generate sequential public IDs.

        Example:
        DIV-000001
        PRJ-000001
        WRK-000001
        """

        # This method is replaced at runtime by _generate_id.
        return f"{prefix}-000001"

    def _generate_id(self, prefix: str, table: str, column: str) -> str:
        row = self.database.fetchone(
            f"""
            SELECT MAX(CAST(SUBSTR({column}, ?) AS INTEGER)) AS max_number
            FROM {table}
            """,
            (len(prefix) + 2,),
        )

        max_number = 0

        if row and row["max_number"] is not None:
            max_number = int(row["max_number"])

        return f"{prefix}-{max_number + 1:06d}"

    # ---------------------------------------------------------
    # DATABASE INITIALIZATION
    # ---------------------------------------------------------

    def initialize(self) -> None:

        self.database.initialize()

        self.database.execute(
            """
            CREATE TABLE IF NOT EXISTS mukti_mahal_divisions (
                division_id TEXT PRIMARY KEY,
                mahal_id TEXT NOT NULL,
                name TEXT NOT NULL,
                division_type TEXT NOT NULL,
                description TEXT NOT NULL DEFAULT '',
                status TEXT NOT NULL DEFAULT 'ACTIVE',
                created_at TEXT NOT NULL
            )
            """
        )

        self.database.execute(
            """
            CREATE TABLE IF NOT EXISTS mukti_mahal_projects (
                project_id TEXT PRIMARY KEY,
                mahal_id TEXT NOT NULL,
                division_id TEXT NOT NULL,
                name TEXT NOT NULL,
                project_type TEXT NOT NULL,
                description TEXT NOT NULL DEFAULT '',
                status TEXT NOT NULL DEFAULT 'PLANNED',
                budget REAL NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL
            )
            """
        )

        self.database.execute(
            """
            CREATE TABLE IF NOT EXISTS mukti_mahal_work (
                work_id TEXT PRIMARY KEY,
                mahal_id TEXT NOT NULL,
                project_id TEXT NOT NULL,
                worker_id TEXT,
                title TEXT NOT NULL,
                work_type TEXT NOT NULL,
                description TEXT NOT NULL DEFAULT '',
                status TEXT NOT NULL DEFAULT 'ASSIGNED',
                compensation_type TEXT NOT NULL DEFAULT 'FIXED',
                compensation_amount REAL NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL,
                completed_at TEXT
            )
            """
        )

    # =========================================================
    # DIVISIONS
    # =========================================================

    def create_division(
        self,
        mahal_id: str,
        name: str,
        division_type: str,
        description: str = "",
    ) -> MuktiMahalDivision:

        division_id = self._generate_id(
            "DIV",
            "mukti_mahal_divisions",
            "division_id",
        )

        created_at = self._now()

        self.database.execute(
            """
            INSERT INTO mukti_mahal_divisions (
                division_id,
                mahal_id,
                name,
                division_type,
                description,
                status,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                division_id,
                mahal_id,
                name,
                division_type,
                description,
                "ACTIVE",
                created_at,
            ),
        )

        return MuktiMahalDivision(
            division_id=division_id,
            mahal_id=mahal_id,
            name=name,
            division_type=division_type,
            description=description,
            status="ACTIVE",
            created_at=created_at,
        )

    def get_division(
        self,
        division_id: str,
    ) -> Optional[MuktiMahalDivision]:

        row = self.database.fetchone(
            """
            SELECT *
            FROM mukti_mahal_divisions
            WHERE division_id = ?
            """,
            (division_id,),
        )

        if not row:
            return None

        return MuktiMahalDivision(**dict(row))

    def list_divisions(
        self,
        mahal_id: Optional[str] = None,
        status: Optional[str] = None,
    ):

        query = """
            SELECT *
            FROM mukti_mahal_divisions
            WHERE 1 = 1
        """

        params = []

        if mahal_id:
            query += " AND mahal_id = ?"
            params.append(mahal_id)

        if status:
            query += " AND status = ?"
            params.append(status)

        query += " ORDER BY created_at ASC"

        rows = self.database.fetchall(query, tuple(params))

        return [
            MuktiMahalDivision(**dict(row))
            for row in rows
        ]

    def update_division(
        self,
        division_id: str,
        name: Optional[str] = None,
        division_type: Optional[str] = None,
        description: Optional[str] = None,
        status: Optional[str] = None,
    ) -> Optional[MuktiMahalDivision]:

        current = self.get_division(division_id)

        if not current:
            return None

        new_name = name if name is not None else current.name
        new_type = (
            division_type
            if division_type is not None
            else current.division_type
        )
        new_description = (
            description
            if description is not None
            else current.description
        )
        new_status = (
            status
            if status is not None
            else current.status
        )

        self.database.execute(
            """
            UPDATE mukti_mahal_divisions
            SET
                name = ?,
                division_type = ?,
                description = ?,
                status = ?
            WHERE division_id = ?
            """,
            (
                new_name,
                new_type,
                new_description,
                new_status,
                division_id,
            ),
        )

        return self.get_division(division_id)

    def delete_division(self, division_id: str) -> bool:

        current = self.get_division(division_id)

        if not current:
            return False

        self.database.execute(
            """
            DELETE FROM mukti_mahal_divisions
            WHERE division_id = ?
            """,
            (division_id,),
        )

        return True

    # =========================================================
    # PROJECTS
    # =========================================================

    def create_project(
        self,
        mahal_id: str,
        division_id: str,
        name: str,
        project_type: str,
        description: str = "",
        budget: float = 0.0,
    ) -> MuktiMahalProject:

        division = self.get_division(division_id)

        if not division:
            raise ValueError("Division not found")

        if division.mahal_id != mahal_id:
            raise ValueError(
                "Division does not belong to the supplied Mahal"
            )

        project_id = self._generate_id(
            "PRJ",
            "mukti_mahal_projects",
            "project_id",
        )

        created_at = self._now()

        self.database.execute(
            """
            INSERT INTO mukti_mahal_projects (
                project_id,
                mahal_id,
                division_id,
                name,
                project_type,
                description,
                status,
                budget,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                project_id,
                mahal_id,
                division_id,
                name,
                project_type,
                description,
                "PLANNED",
                float(budget),
                created_at,
            ),
        )

        return MuktiMahalProject(
            project_id=project_id,
            mahal_id=mahal_id,
            division_id=division_id,
            name=name,
            project_type=project_type,
            description=description,
            status="PLANNED",
            budget=float(budget),
            created_at=created_at,
        )

    def get_project(
        self,
        project_id: str,
    ) -> Optional[MuktiMahalProject]:

        row = self.database.fetchone(
            """
            SELECT *
            FROM mukti_mahal_projects
            WHERE project_id = ?
            """,
            (project_id,),
        )

        if not row:
            return None

        return MuktiMahalProject(**dict(row))

    def list_projects(
        self,
        mahal_id: Optional[str] = None,
        division_id: Optional[str] = None,
        status: Optional[str] = None,
    ):

        query = """
            SELECT *
            FROM mukti_mahal_projects
            WHERE 1 = 1
        """

        params = []

        if mahal_id:
            query += " AND mahal_id = ?"
            params.append(mahal_id)

        if division_id:
            query += " AND division_id = ?"
            params.append(division_id)

        if status:
            query += " AND status = ?"
            params.append(status)

        query += " ORDER BY created_at ASC"

        rows = self.database.fetchall(query, tuple(params))

        return [
            MuktiMahalProject(**dict(row))
            for row in rows
        ]

    def update_project(
        self,
        project_id: str,
        name: Optional[str] = None,
        project_type: Optional[str] = None,
        description: Optional[str] = None,
        status: Optional[str] = None,
        budget: Optional[float] = None,
    ) -> Optional[MuktiMahalProject]:

        current = self.get_project(project_id)

        if not current:
            return None

        self.database.execute(
            """
            UPDATE mukti_mahal_projects
            SET
                name = ?,
                project_type = ?,
                description = ?,
                status = ?,
                budget = ?
            WHERE project_id = ?
            """,
            (
                name if name is not None else current.name,
                (
                    project_type
                    if project_type is not None
                    else current.project_type
                ),
                (
                    description
                    if description is not None
                    else current.description
                ),
                status if status is not None else current.status,
                (
                    float(budget)
                    if budget is not None
                    else current.budget
                ),
                project_id,
            ),
        )

        return self.get_project(project_id)

    def delete_project(self, project_id: str) -> bool:

        current = self.get_project(project_id)

        if not current:
            return False

        self.database.execute(
            """
            DELETE FROM mukti_mahal_projects
            WHERE project_id = ?
            """,
            (project_id,),
        )

        return True

    # =========================================================
    # WORK
    # =========================================================

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
    ) -> MuktiMahalWork:

        project = self.get_project(project_id)

        if not project:
            raise ValueError("Project not found")

        if project.mahal_id != mahal_id:
            raise ValueError(
                "Project does not belong to the supplied Mahal"
            )

        work_id = self._generate_id(
            "WRK",
            "mukti_mahal_work",
            "work_id",
        )

        created_at = self._now()

        self.database.execute(
            """
            INSERT INTO mukti_mahal_work (
                work_id,
                mahal_id,
                project_id,
                worker_id,
                title,
                work_type,
                description,
                status,
                compensation_type,
                compensation_amount,
                created_at,
                completed_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                work_id,
                mahal_id,
                project_id,
                worker_id,
                title,
                work_type,
                description,
                "ASSIGNED",
                compensation_type,
                float(compensation_amount),
                created_at,
                None,
            ),
        )

        return MuktiMahalWork(
            work_id=work_id,
            mahal_id=mahal_id,
            project_id=project_id,
            worker_id=worker_id,
            title=title,
            work_type=work_type,
            description=description,
            status="ASSIGNED",
            compensation_type=compensation_type,
            compensation_amount=float(compensation_amount),
            created_at=created_at,
            completed_at=None,
        )

    def get_work(
        self,
        work_id: str,
    ) -> Optional[MuktiMahalWork]:

        row = self.database.fetchone(
            """
            SELECT *
            FROM mukti_mahal_work
            WHERE work_id = ?
            """,
            (work_id,),
        )

        if not row:
            return None

        return MuktiMahalWork(**dict(row))

    def list_work(
        self,
        mahal_id: Optional[str] = None,
        project_id: Optional[str] = None,
        worker_id: Optional[str] = None,
        status: Optional[str] = None,
    ):

        query = """
            SELECT *
            FROM mukti_mahal_work
            WHERE 1 = 1
        """

        params = []

        if mahal_id:
            query += " AND mahal_id = ?"
            params.append(mahal_id)

        if project_id:
            query += " AND project_id = ?"
            params.append(project_id)

        if worker_id:
            query += " AND worker_id = ?"
            params.append(worker_id)

        if status:
            query += " AND status = ?"
            params.append(status)

        query += " ORDER BY created_at ASC"

        rows = self.database.fetchall(query, tuple(params))

        return [
            MuktiMahalWork(**dict(row))
            for row in rows
        ]

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
    ) -> Optional[MuktiMahalWork]:

        current = self.get_work(work_id)

        if not current:
            return None

        new_status = (
            status
            if status is not None
            else current.status
        )

        completed_at = current.completed_at

        if new_status.upper() == "COMPLETED":
            completed_at = completed_at or self._now()

        self.database.execute(
            """
            UPDATE mukti_mahal_work
            SET
                worker_id = ?,
                title = ?,
                work_type = ?,
                description = ?,
                status = ?,
                compensation_type = ?,
                compensation_amount = ?,
                completed_at = ?
            WHERE work_id = ?
            """,
            (
                worker_id
                if worker_id is not None
                else current.worker_id,
                title if title is not None else current.title,
                (
                    work_type
                    if work_type is not None
                    else current.work_type
                ),
                (
                    description
                    if description is not None
                    else current.description
                ),
                new_status,
                (
                    compensation_type
                    if compensation_type is not None
                    else current.compensation_type
                ),
                (
                    float(compensation_amount)
                    if compensation_amount is not None
                    else current.compensation_amount
                ),
                completed_at,
                work_id,
            ),
        )

        return self.get_work(work_id)

    def delete_work(self, work_id: str) -> bool:

        current = self.get_work(work_id)

        if not current:
            return False

        self.database.execute(
            """
            DELETE FROM mukti_mahal_work
            WHERE work_id = ?
            """,
            (work_id,),
        )

        return True

    # =========================================================
    # STATUS / SUMMARY
    # =========================================================

    def status(self):

        divisions = self.database.fetchone(
            """
            SELECT COUNT(*) AS count
            FROM mukti_mahal_divisions
            """
        )

        projects = self.database.fetchone(
            """
            SELECT COUNT(*) AS count
            FROM mukti_mahal_projects
            """
        )

        work = self.database.fetchone(
            """
            SELECT COUNT(*) AS count
            FROM mukti_mahal_work
            """
        )

        return {
            "system": "MUKTI MAHAL OPERATIONS",
            "status": "LIVE",
            "modules": {
                "divisions": {
                    "status": "READY",
                    "count": int(divisions["count"]),
                },
                "projects": {
                    "status": "READY",
                    "count": int(projects["count"]),
                },
                "work": {
                    "status": "READY",
                    "count": int(work["count"]),
                },
            },
        }
