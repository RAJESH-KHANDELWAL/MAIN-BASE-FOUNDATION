"""SSL/TLS infrastructure controller."""

from .service import SSLService


class SSLController:
    def __init__(self):
        self.service = SSLService()

    def create(self, **kwargs) -> dict:
        ssl = self.service.create(**kwargs)
        return ssl.to_dict()

    def get(self, ssl_id: str) -> dict | None:
        ssl = self.service.get(ssl_id)

        if not ssl:
            return None

        return ssl.to_dict()

    def list(self) -> list[dict]:
        return [
            ssl.to_dict()
            for ssl in self.service.list_all()
        ]

    def update_status(
        self,
        ssl_id: str,
        certificate_status: str,
    ) -> dict | None:

        ssl = self.service.update_status(
            ssl_id,
            certificate_status,
        )

        if not ssl:
            return None

        return ssl.to_dict()

    def update_auto_renew(
        self,
        ssl_id: str,
        auto_renew: bool,
    ) -> dict | None:

        ssl = self.service.update_auto_renew(
            ssl_id,
            auto_renew,
        )

        if not ssl:
            return None

        return ssl.to_dict()

    def delete(self, ssl_id: str) -> bool:
        return self.service.delete(ssl_id)
