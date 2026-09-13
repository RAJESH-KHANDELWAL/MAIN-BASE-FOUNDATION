"""Monitoring infrastructure controller."""

from .service import MonitoringService


class MonitoringController:
    def __init__(self):
        self.service = MonitoringService()

    def create(self, **kwargs) -> dict:
        monitoring = self.service.create(**kwargs)
        return monitoring.to_dict()

    def get(self, monitoring_id: str) -> dict | None:
        monitoring = self.service.get(monitoring_id)

        if not monitoring:
            return None

        return monitoring.to_dict()

    def list(self) -> list[dict]:
        return [
            monitoring.to_dict()
            for monitoring in self.service.list_all()
        ]

    def update_status(
        self,
        monitoring_id: str,
        status: str,
    ) -> dict | None:

        monitoring = self.service.update_status(
            monitoring_id,
            status,
        )

        if not monitoring:
            return None

        return monitoring.to_dict()

    def record_check(
        self,
        monitoring_id: str,
        check_status: str,
    ) -> dict | None:

        monitoring = self.service.record_check(
            monitoring_id,
            check_status,
        )

        if not monitoring:
            return None

        return monitoring.to_dict()

    def delete(self, monitoring_id: str) -> bool:
        return self.service.delete(monitoring_id)
