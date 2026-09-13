"""Security infrastructure controller."""

from .service import SecurityService


class SecurityController:
    def __init__(self):
        self.service = SecurityService()

    def create(self, **kwargs) -> dict:
        security = self.service.create(**kwargs)
        return security.to_dict()

    def get(self, security_id: str) -> dict | None:
        security = self.service.get(security_id)

        if not security:
            return None

        return security.to_dict()

    def list(self) -> list[dict]:
        return [
            security.to_dict()
            for security in self.service.list_all()
        ]

    def update_status(
        self,
        security_id: str,
        status: str,
    ) -> dict | None:

        security = self.service.update_status(
            security_id,
            status,
        )

        if not security:
            return None

        return security.to_dict()

    def update_enabled(
        self,
        security_id: str,
        enabled: bool,
    ) -> dict | None:

        security = self.service.update_enabled(
            security_id,
            enabled,
        )

        if not security:
            return None

        return security.to_dict()

    def delete(self, security_id: str) -> bool:
        return self.service.delete(security_id)
