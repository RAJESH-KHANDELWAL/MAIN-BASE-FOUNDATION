
"""User models for MAIN-BASE-FOUNDATION."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class User:
    """Represent a user without exposing password credentials."""

    user_id: str
    full_name: str
    email: str
    username: str = ""
    phone: str = ""
    phone_no: str = ""
    mobile_no: str = ""
    whatsapp_no: str = ""
    role: str = "USER"
    status: str = "ACTIVE"

    def to_dict(self) -> dict:
        """Return safe public user data."""
        return {
            "user_id": self.user_id,
            "full_name": self.full_name,
            "username": self.username,
            "email": self.email,
            "phone": self.phone,
            "phone_no": self.phone_no,
            "mobile_no": self.mobile_no,
            "whatsapp_no": self.whatsapp_no,
            "role": self.role,
            "status": self.status,
        }


__all__ = ["User"]
