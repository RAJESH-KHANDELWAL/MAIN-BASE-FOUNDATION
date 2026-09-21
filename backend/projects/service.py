"""Project persistence service for MAIN-BASE-FOUNDATION."""

from datetime import datetime, timezone
from uuid import uuid4

from backend.database.service import DatabaseService

from .model import Project


class ProjectService:
    def __init__(self, database=None):
        self.database = database or DatabaseService()
        self._ensure_table()

    def _now(self):
        return datetime.now(timezone.utc).isoformat()

    def _ensure_table(self):
        self.database.initialize()

        self.database.execute(
            """
            CREATE TABLE IF NOT EXISTS projects (
                project_id TEXT PRIMARY KEY,
                owner_id TEXT NOT NULL,
                name TEXT NOT NULL,
                description TEXT DEFAULT '',
                project_type TEXT DEFAULT 'GENERAL',
                status TEXT DEFAULT 'ACTIVE',
                visibility TEXT DEFAULT 'PRIVATE',
                budget REAL,
                currency TEXT DEFAULT 'INR',
                deadline TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )

    def _row_to_project(self, row):
        if not row:
            return None

        return Project(
            project_id=row["project_id"],
            owner_id=row["owner_id"],
            name=row["name"],
            description=row["description"] or "",
            project_type=row["project_type"] or "GENERAL",
            status=row["status"] or "ACTIVE",
            visibility=row["visibility"] or "PRIVATE",
            budget=row["budget"],
            currency=row["currency"] or "INR",
            deadline=row["deadline"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )

    def create(
        self,
        owner_id,
        name,
        description="",
        project_type="GENERAL",
        status="ACTIVE",
        visibility="PRIVATE",
        budget=None,
        currency="INR",
        deadline=None,
    ):
        project_id = str(uuid4())
        now = self._now()

        self.database.execute(
            """
            INSERT INTO projects (
                project_id,
                owner_id,
                name,
                description,
                project_type,
                status,
                visibility,
                budget,
                currency,
                deadline,
                created_at,
                updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                project_id,
                owner_id,
                name,
                description,
                project_type,
                status,
                visibility,
                budget,
                currency,
                deadline,
                now,
                now,
            ),
        )

        return self.get(project_id)

    def get(self, project_id):
        row = self.database.fetchone(
            """
            SELECT *
            FROM projects
            WHERE project_id = ?
            """,
            (project_id,),
        )

        return self._row_to_project(row)

    def list(self, owner_id=None, status=None):
        query = """
            SELECT *
            FROM projects
            WHERE 1 = 1
        """

        params = []

        if owner_id:
            query += " AND owner_id = ?"
            params.append(owner_id)

        if status:
            query += " AND status = ?"
            params.append(status)

        query += " ORDER BY created_at DESC"

        rows = self.database.fetchall(query, tuple(params))

        return [
            self._row_to_project(row)
            for row in rows
        ]

    def update(
        self,
        project_id,
        name=None,
        description=None,
        project_type=None,
        status=None,
        visibility=None,
        budget=None,
        currency=None,
        deadline=None,
    ):
        existing = self.get(project_id)

        if not existing:
            return None

        values = {
            "name": (
                name
                if name is not None
                else existing.name
            ),
            "description": (
                description
                if description is not None
                else existing.description
            ),
            "project_type": (
                project_type
                if project_type is not None
                else existing.project_type
            ),
            "status": (
                status
                if status is not None
                else existing.status
            ),
            "visibility": (
                visibility
                if visibility is not None
                else existing.visibility
            ),
            "budget": (
                budget
                if budget is not None
                else existing.budget
            ),
            "currency": (
                currency
                if currency is not None
                else existing.currency
            ),
            "deadline": (
                deadline
                if deadline is not None
                else existing.deadline
            ),
            "updated_at": self._now(),
        }

        self.database.execute(
            """
            UPDATE projects
            SET
                name = ?,
                description = ?,
                project_type = ?,
                status = ?,
                visibility = ?,
                budget = ?,
                currency = ?,
                deadline = ?,
                updated_at = ?
            WHERE project_id = ?
            """,
            (
                values["name"],
                values["description"],
                values["project_type"],
                values["status"],
                values["visibility"],
                values["budget"],
                values["currency"],
                values["deadline"],
                values["updated_at"],
                project_id,
            ),
        )

        return self.get(project_id)

    def update_status(self, project_id, status):
        existing = self.get(project_id)

        if not existing:
            return None

        self.database.execute(
            """
            UPDATE projects
            SET status = ?, updated_at = ?
            WHERE project_id = ?
            """,
            (
                status,
                self._now(),
                project_id,
            ),
        )

        return self.get(project_id)

    def delete(self, project_id):
        existing = self.get(project_id)

        if not existing:
            return False

        self.database.execute(
            """
            DELETE FROM projects
            WHERE project_id = ?
            """,
            (project_id,),
        )

        return True
