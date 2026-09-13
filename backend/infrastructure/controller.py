"""Infrastructure controller."""

from typing import Optional

from .model import InfrastructureInfo
from .service import InfrastructureService


class InfrastructureController:

    def __init__(self):
        self.service = InfrastructureService()

    def create(
        self,
        name: str,
        infrastructure_type: str,
        provider: str = "",
        region: str = "",
        public_ipv4: str = "",
        public_ipv6: str = "",
        description: str = "",
    ) -> dict:

        item = self.service.create(
            name=name,
            infrastructure_type=infrastructure_type,
            provider=provider,
            region=region,
            public_ipv4=public_ipv4,
            public_ipv6=public_ipv6,
            description=description,
        )

        return item.to_dict()

    def get(
        self,
        infrastructure_id: str,
    ) -> Optional[dict]:

        item = self.service.get(
            infrastructure_id
        )

        return item.to_dict() if item else None

    def list(self) -> list[dict]:

        return [
            item.to_dict()
            for item in self.service.list_all()
        ]

    def update_status(
        self,
        infrastructure_id: str,
        status: str,
    ) -> Optional[dict]:

        item = self.service.update_status(
            infrastructure_id,
            status,
        )

        return item.to_dict() if item else None

    def delete(
        self,
        infrastructure_id: str,
    ) -> bool:

        return self.service.delete(
            infrastructure_id
        )
