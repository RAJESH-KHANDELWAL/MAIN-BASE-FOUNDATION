"""CDN infrastructure controller."""

from .service import CDNService


class CDNController:
    def __init__(self):
        self.service = CDNService()

    def create(self, **kwargs) -> dict:
        cdn = self.service.create(**kwargs)
        return cdn.to_dict()

    def get(self, cdn_id: str) -> dict | None:
        cdn = self.service.get(cdn_id)

        if not cdn:
            return None

        return cdn.to_dict()

    def list(self) -> list[dict]:
        return [
            cdn.to_dict()
            for cdn in self.service.list_all()
        ]

    def update_status(
        self,
        cdn_id: str,
        status: str,
    ) -> dict | None:

        cdn = self.service.update_status(
            cdn_id,
            status,
        )

        if not cdn:
            return None

        return cdn.to_dict()

    def update_cache(
        self,
        cdn_id: str,
        cache_enabled: bool,
    ) -> dict | None:

        cdn = self.service.update_cache(
            cdn_id,
            cache_enabled,
        )

        if not cdn:
            return None

        return cdn.to_dict()

    def update_ssl(
        self,
        cdn_id: str,
        ssl_enabled: bool,
    ) -> dict | None:

        cdn = self.service.update_ssl(
            cdn_id,
            ssl_enabled,
        )

        if not cdn:
            return None

        return cdn.to_dict()

    def delete(self, cdn_id: str) -> bool:
        return self.service.delete(cdn_id)
