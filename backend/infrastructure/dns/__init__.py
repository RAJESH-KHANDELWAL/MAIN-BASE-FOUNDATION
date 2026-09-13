"""DNS infrastructure for MAIN BASE FOUNDATION."""

from .model import DNSZone, DNSRecord
from .service import DNSService
from .controller import DNSController

__all__ = [
    "DNSZone",
    "DNSRecord",
    "DNSService",
    "DNSController",
]
