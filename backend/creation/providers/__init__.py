"""
MAIN BASE FOUNDATION
AI Provider Adapter Layer
"""

from .model import (
    ProviderCapability,
    ProviderGenerationResult,
)

from .service import ProviderService
from .controller import ProviderController

__all__ = [
    "ProviderCapability",
    "ProviderGenerationResult",
    "ProviderService",
    "ProviderController",
]
