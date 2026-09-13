"""
MAIN BASE FOUNDATION
Infrastructure - DNS Controller

Controller layer for DNS infrastructure management.
"""

from typing import Any, Dict, List, Optional

from backend.infrastructure.dns.service import DNSService


class DNSController:
    """
    Public controller facade for DNSService.
    """

    def __init__(self):
        self.service = DNSService()

    # ---------------------------------------------------------
    # ZONES
    # ---------------------------------------------------------

    def create_zone(
        self,
        domain_name: str,
        zone_type: str = "PRIMARY",
        primary_nameserver: Optional[str] = None,
        secondary_nameserver: Optional[str] = None,
        nameserver_status: str = "PENDING",
        dns_status: str = "PENDING",
        status: str = "ACTIVE",
        verified: bool = False,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:

        result = self.service.create_zone(
            domain_name=domain_name,
            zone_type=zone_type,
            primary_nameserver=primary_nameserver,
            secondary_nameserver=secondary_nameserver,
            nameserver_status=nameserver_status,
            dns_status=dns_status,
            status=status,
            verified=verified,
            metadata=metadata,
        )

        return result.to_dict()

    def get_zone(
        self,
        zone_id: str,
    ) -> Optional[Dict[str, Any]]:

        result = self.service.get_zone(zone_id)

        if not result:
            return None

        return result.to_dict()

    def get_zone_by_domain(
        self,
        domain_name: str,
    ) -> Optional[Dict[str, Any]]:

        result = self.service.get_zone_by_domain(
            domain_name
        )

        if not result:
            return None

        return result.to_dict()

    def list_zones(
        self,
        status: Optional[str] = None,
    ) -> List[Dict[str, Any]]:

        results = self.service.list_zones(
            status=status
        )

        return [
            result.to_dict()
            for result in results
        ]

    def update_zone(
        self,
        zone_id: str,
        **updates,
    ) -> Optional[Dict[str, Any]]:

        result = self.service.update_zone(
            zone_id,
            **updates,
        )

        if not result:
            return None

        return result.to_dict()

    def delete_zone(
        self,
        zone_id: str,
    ) -> bool:

        return self.service.delete_zone(
            zone_id
        )

    # ---------------------------------------------------------
    # DNS RECORDS
    # ---------------------------------------------------------

    def create_record(
        self,
        domain_name: str,
        record_type: str,
        record_name: str,
        record_value: str,
        ttl: int = 3600,
        priority: Optional[int] = None,
        status: str = "ACTIVE",
        verified: bool = False,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:

        result = self.service.create_record(
            domain_name=domain_name,
            record_type=record_type,
            record_name=record_name,
            record_value=record_value,
            ttl=ttl,
            priority=priority,
            status=status,
            verified=verified,
            metadata=metadata,
        )

        return result.to_dict()

    def get_record(
        self,
        record_id: str,
    ) -> Optional[Dict[str, Any]]:

        result = self.service.get_record(record_id)

        if not result:
            return None

        return result.to_dict()

    def list_records(
        self,
        domain_name: Optional[str] = None,
        record_type: Optional[str] = None,
    ) -> List[Dict[str, Any]]:

        results = self.service.list_records(
            domain_name=domain_name,
            record_type=record_type,
        )

        return [
            result.to_dict()
            for result in results
        ]

    def update_record(
        self,
        record_id: str,
        **updates,
    ) -> Optional[Dict[str, Any]]:

        result = self.service.update_record(
            record_id,
            **updates,
        )

        if not result:
            return None

        return result.to_dict()

    def delete_record(
        self,
        record_id: str,
    ) -> bool:

        return self.service.delete_record(
            record_id
        )

    # ---------------------------------------------------------
    # DNS STATE OPERATIONS
    # ---------------------------------------------------------

    def activate_zone(
        self,
        zone_id: str,
    ) -> Optional[Dict[str, Any]]:

        result = self.service.activate_zone(
            zone_id
        )

        if not result:
            return None

        return result.to_dict()

    def set_zone_propagating(
        self,
        zone_id: str,
    ) -> Optional[Dict[str, Any]]:

        result = self.service.set_zone_propagating(
            zone_id
        )

        if not result:
            return None

        return result.to_dict()

    def suspend_zone(
        self,
        zone_id: str,
    ) -> Optional[Dict[str, Any]]:

        result = self.service.suspend_zone(
            zone_id
        )

        if not result:
            return None

        return result.to_dict()

    def verify_zone(
        self,
        zone_id: str,
    ) -> Optional[Dict[str, Any]]:

        result = self.service.verify_zone(
            zone_id
        )

        if not result:
            return None

        return result.to_dict()

    def verify_record(
        self,
        record_id: str,
    ) -> Optional[Dict[str, Any]]:

        result = self.service.verify_record(
            record_id
        )

        if not result:
            return None

        return result.to_dict()
