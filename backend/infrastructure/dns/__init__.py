"""
MAIN BASE FOUNDATION
Infrastructure - DNS Package
"""

from .model import DNSZoneInfo, DNSRecordInfo
from .service import DNSService
from .controller import DNSController


__all__ = [
    "DNSZoneInfo",
    "DNSRecordInfo",
    "DNSService",
    "DNSController",
]
