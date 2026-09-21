"""Project database connection for MAIN-BASE-FOUNDATION."""

from backend.database.service import DatabaseService


def get_project_database():
    return DatabaseService()
