"""Project controller for MAIN-BASE-FOUNDATION."""

from .service import ProjectService


class ProjectController:
    def __init__(self, service=None):
        self.service = service or ProjectService()

    def create(self, **kwargs):
        return self.service.create(**kwargs)

    def get(self, project_id):
        return self.service.get(project_id)

    def list(self, owner_id=None, status=None):
        return self.service.list(
            owner_id=owner_id,
            status=status,
        )

    def update(self, project_id, **kwargs):
        return self.service.update(
            project_id,
            **kwargs,
        )

    def update_status(self, project_id, status):
        return self.service.update_status(
            project_id,
            status,
        )

    def delete(self, project_id):
        return self.service.delete(project_id)
