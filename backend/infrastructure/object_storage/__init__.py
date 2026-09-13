"""Object storage infrastructure for MAIN BASE FOUNDATION."""

from .model import ObjectStorageInfo
from .service import ObjectStorageService
from .controller import ObjectStorageController

__all__ = [
    "ObjectStorageInfo",
    "ObjectStorageService",
    "ObjectStorageController",
]
