"""DNS controller."""

from .service import DNSService


class DNSController:

    def __init__(self):
        self.service = DNSService()

    def create_zone(
        self,
        domain: str,
        nameservers: list[str] | None = None,
    ) -> dict:

        return self.service.create_zone(
            domain=domain,
            nameservers=nameservers,
        ).to_dict()

    def get_zone(
        self,
        zone_id: str,
    ) -> dict | None:

        zone = self.service.get_zone(zone_id)

        return zone.to_dict() if zone else None

    def list_zones(self) -> list[dict]:

        return [
            zone.to_dict()
            for zone in self.service.list_zones()
        ]

    def add_record(
        self,
        zone_id: str,
        record_type: str,
        name: str,
        content: str,
        ttl: int = 300,
        priority: int | None = None,
    ) -> dict:

        return self.service.add_record(
            zone_id=zone_id,
            record_type=record_type,
            name=name,
            content=content,
            ttl=ttl,
            priority=priority,
        ).to_dict()

    def delete_record(
        self,
        record_id: str,
    ) -> bool:

        return self.service.delete_record(
            record_id
        )
