import os
from typing import Any, Dict


class SupremeControlService:
    """Secure command bridge for the Supreme admin owner."""

    _COMMANDS = {
        "platform.status",
        "modules.list",
        "ai.status",
        "users.list",
    }

    @staticmethod
    def _configured_token() -> str:
        return os.getenv("SUPREME_CONTROL_TOKEN", "").strip()

    @classmethod
    def validate_token(cls, token: str | None) -> bool:
        configured = cls._configured_token()
        if not configured:
            return False
        if not token:
            return False
        return token == configured

    @classmethod
    def get_status(cls, controller: Any) -> Dict[str, Any]:
        try:
            owner_exists = bool(controller.exists())
        except Exception:
            owner_exists = False

        return {
            "service": "MAIN-BASE-FOUNDATION",
            "status": "healthy",
            "controller": "SUPREME",
            "owner_exists": owner_exists,
            "token_configured": bool(cls._configured_token()),
            "supported_commands": sorted(cls._COMMANDS),
        }

    @classmethod
    def execute_command(cls, controller: Any, command: str, payload: Dict[str, Any] | None = None) -> Dict[str, Any]:
        selected = (command or "").strip()
        payload = payload or {}

        if selected not in cls._COMMANDS:
            raise ValueError(f"Unsupported command: {selected}")

        if selected == "platform.status":
            return cls.get_status(controller)

        if selected == "modules.list":
            return {
                "command": selected,
                "status": "ok",
                "modules": [
                    "identity",
                    "auth",
                    "users",
                    "business",
                    "projects",
                    "storage",
                    "security",
                    "ai",
                    "dashboard",
                    "supreme",
                ],
            }

        if selected == "ai.status":
            return {
                "command": selected,
                "status": "ok",
                "module": "ai",
                "provider": "MAIN-BASE-FOUNDATION",
                "description": "AI services are controlled through the platform core",
            }

        if selected == "users.list":
            return {
                "command": selected,
                "status": "ok",
                "count": 0,
                "note": "User listing is exposed through the platform user APIs when implemented",
                "payload": payload,
            }

        raise ValueError(f"Command not implemented: {selected}")


__all__ = ["SupremeControlService"]
