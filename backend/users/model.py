"""User models for MAIN-BASE-FOUNDATION."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class User:
    """Represent a user without exposing password credentials."""

    user_id: str
    full_name: str
    username: str
    email: str
    phone: str
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
            "role": self.role,
            "status": self.status,
        }


__all__ = ["User"]
