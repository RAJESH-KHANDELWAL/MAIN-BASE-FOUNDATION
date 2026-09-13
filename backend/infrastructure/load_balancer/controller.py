"""Load balancer infrastructure controller."""

from .service import LoadBalancerService


class LoadBalancerController:
    def __init__(self):
        self.service = LoadBalancerService()

    def create(self, **kwargs) -> dict:
        load_balancer = self.service.create(**kwargs)
        return load_balancer.to_dict()

    def get(
        self,
        load_balancer_id: str,
    ) -> dict | None:

        load_balancer = self.service.get(
            load_balancer_id
        )

        if not load_balancer:
            return None

        return load_balancer.to_dict()

    def list(self) -> list[dict]:
        return [
            load_balancer.to_dict()
            for load_balancer in self.service.list_all()
        ]

    def update_status(
        self,
        load_balancer_id: str,
        status: str,
    ) -> dict | None:

        load_balancer = self.service.update_status(
            load_balancer_id,
            status,
        )

        if not load_balancer:
            return None

        return load_balancer.to_dict()

    def update_enabled(
        self,
        load_balancer_id: str,
        enabled: bool,
    ) -> dict | None:

        load_balancer = self.service.update_enabled(
            load_balancer_id,
            enabled,
        )

        if not load_balancer:
            return None

        return load_balancer.to_dict()

    def update_health_check(
        self,
        load_balancer_id: str,
        health_check_enabled: bool,
    ) -> dict | None:

        load_balancer = self.service.update_health_check(
            load_balancer_id,
            health_check_enabled,
        )

        if not load_balancer:
            return None

        return load_balancer.to_dict()

    def delete(self, load_balancer_id: str) -> bool:
        return self.service.delete(load_balancer_id)
