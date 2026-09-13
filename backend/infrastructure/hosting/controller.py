"""Hosting infrastructure controller."""

from .service import HostingService


class HostingController:
    def __init__(self):
        self.service = HostingService()

    def create(self, **kwargs) -> dict:
        hosting = self.service.create(**kwargs)
        return hosting.to_dict()

    def get(self, hosting_id: str) -> dict | None:
        hosting = self.service.get(hosting_id)

        if not hosting:
            return None

        return hosting.to_dict()

    def list(self) -> list[dict]:
        return [
            hosting.to_dict()
            for hosting in self.service.list_all()
        ]

    def update_status(
        self,
        hosting_id: str,
        status: str,
    ) -> dict | None:

        hosting = self.service.update_status(
            hosting_id,
            status,
        )

        if not hosting:
            return None

        return hosting.to_dict()

    def delete(self, hosting_id: str) -> bool:
        return self.service.delete(hosting_id)
