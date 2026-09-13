"""Email infrastructure for MAIN BASE FOUNDATION."""

from .model import EmailServiceInfo
from .service import EmailService
from .controller import EmailController

__all__ = [
    "EmailServiceInfo",
    "EmailService",
    "EmailController",
]
