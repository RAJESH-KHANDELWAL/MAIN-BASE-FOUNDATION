"""Server infrastructure controller."""

from .service import ServerService


class ServerController:

    def __init__(self):
        self.service = ServerService()

    def create(self, **kwargs) -> dict:
        return self.service.create(**kwargs).to_dict()

    def get(self, server_id: str) -> dict | None:
        server = self.service.get(server_id)
        return server.to_dict() if server else None

    def list(self) -> list[dict]:
        return [
            server.to_dict()
            for server in self.service.list_all()
        ]

    def update_status(
        self,
        server_id: str,
        status: str,
    ) -> dict | None:

        server = self.service.update_status(
            server_id,
            status,
        )

        return server.to_dict() if server else None

    def delete(self, server_id: str) -> bool:
        return self.service.delete(server_id)
