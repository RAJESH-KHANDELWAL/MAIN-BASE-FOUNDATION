"""Domain infrastructure controller."""

from .service import DomainService


class DomainController:
    def __init__(self):
        self.service = DomainService()

    def create(self, **kwargs) -> dict:
        domain = self.service.create(**kwargs)
        return domain.to_dict()

    def get(self, domain_id: str) -> dict | None:
        domain = self.service.get(domain_id)

        if not domain:
            return None

        return domain.to_dict()

    def get_by_domain(self, domain_name: str) -> dict | None:
        domain = self.service.get_by_domain(domain_name)

        if not domain:
            return None

        return domain.to_dict()

    def list(self) -> list[dict]:
        return [
            domain.to_dict()
            for domain in self.service.list_all()
        ]

    def update_status(
        self,
        domain_id: str,
        status: str,
    ) -> dict | None:

        domain = self.service.update_status(
            domain_id,
            status,
        )

        if not domain:
            return None

        return domain.to_dict()

    def update_nameservers(
        self,
        domain_id: str,
        nameservers: list[str],
    ) -> dict | None:

        domain = self.service.update_nameservers(
            domain_id,
            nameservers,
        )

        if not domain:
            return None

        return domain.to_dict()

    def update_verification(
        self,
        domain_id: str,
        verified: bool,
    ) -> dict | None:

        domain = self.service.update_verification(
            domain_id,
            verified,
        )

        if not domain:
            return None

        return domain.to_dict()

    def delete(self, domain_id: str) -> bool:
        return self.service.delete(domain_id)
