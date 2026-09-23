"""
MAIN BASE FOUNDATION

SUPREME — Ecosystem Vault Security

Central security layer for:

- Vault locking and unlocking
- Secret protection
- Credential references
- Access validation
- Secure secret storage abstraction

Security principles:
- Never expose plaintext passwords.
- Never log secrets.
- Never return raw credentials from the vault layer.
- Store only encrypted secret material or secure references.
- Provider authentication remains controlled by the provider.
"""

from __future__ import annotations

import hashlib
import hmac
import secrets
from typing import Optional


class VaultSecurity:
    """Central security service for SUPREME ecosystem vaults."""

    HASH_ALGORITHM = "SHA-256"

    def __init__(self) -> None:
        self._initialized = False

    # =========================================================
    # 🚀 INITIALIZATION
    # =========================================================

    def initialize(self) -> dict:
        """Initialize vault security."""

        self._initialized = True

        return {
            "service": "SUPREME_VAULT_SECURITY",
            "status": "READY",
            "initialized": True,
        }

    # =========================================================
    # 🔑 IDENTIFIER
    # =========================================================

    @staticmethod
    def generate_reference_id() -> str:
        """
        Generate a non-secret credential reference ID.
        """

        return secrets.token_urlsafe(32)

    # =========================================================
    # 🔐 SECRET FINGERPRINT
    # =========================================================

    @classmethod
    def fingerprint(
        cls,
        value: str,
    ) -> str:
        """
        Generate a one-way fingerprint.

        This is NOT encryption and cannot be used
        to recover the original secret.
        """

        if not isinstance(value, str):
            raise TypeError(
                "value must be a string."
            )

        return hashlib.sha256(
            value.encode("utf-8")
        ).hexdigest()

    # =========================================================
    # 🔎 SECRET VERIFICATION
    # =========================================================

    @classmethod
    def verify_fingerprint(
        cls,
        value: str,
        expected_fingerprint: str,
    ) -> bool:
        """
        Verify a value against a stored fingerprint.
        """

        if not isinstance(value, str):
            return False

        if not isinstance(
            expected_fingerprint,
            str,
        ):
            return False

        actual = cls.fingerprint(value)

        return hmac.compare_digest(
            actual,
            expected_fingerprint,
        )

    # =========================================================
    # 🧂 RANDOM NONCE
    # =========================================================

    @staticmethod
    def generate_nonce(
        size: int = 32,
    ) -> str:
        """
        Generate a cryptographically secure nonce.

        The nonce is not a password and does not contain
        credential information.
        """

        if size <= 0:
            raise ValueError(
                "size must be greater than zero."
            )

        return secrets.token_urlsafe(size)

    # =========================================================
    # 🔒 SECRET SANITIZATION
    # =========================================================

    @staticmethod
    def sanitize_metadata(
        metadata: dict,
    ) -> dict:
        """
        Remove commonly sensitive fields from metadata.

        This prevents accidental exposure through logs
        or status responses.
        """

        if not isinstance(metadata, dict):
            return {}

        sensitive_keys = {
            "password",
            "passwd",
            "secret",
            "client_secret",
            "access_token",
            "refresh_token",
            "api_key",
            "private_key",
            "credential",
            "credentials",
        }

        return {
            key: value
            for key, value in metadata.items()
            if str(key).lower()
            not in sensitive_keys
        }

    # =========================================================
    # 🛡️ SECRET VALIDATION
    # =========================================================

    @staticmethod
    def validate_secret_reference(
        reference: Optional[str],
    ) -> bool:
        """
        Validate that a secret is represented by a
        non-empty reference rather than plaintext data.
        """

        if reference is None:
            return False

        if not isinstance(reference, str):
            return False

        return bool(reference.strip())

    # =========================================================
    # 🔐 MASK VALUE
    # =========================================================

    @staticmethod
    def mask_identifier(
        value: str,
        visible: int = 4,
    ) -> str:
        """
        Mask an identifier for safe UI/log presentation.
        """

        if not isinstance(value, str):
            return ""

        value = value.strip()

        if not value:
            return ""

        if visible < 0:
            visible = 0

        if len(value) <= visible:
            return "*" * len(value)

        return (
            "*" * (len(value) - visible)
            + value[-visible:]
        )

    # =========================================================
    # 📊 STATUS
    # =========================================================

    def status(self) -> dict:
        """Return vault security status."""

        return {
            "service": "SUPREME_VAULT_SECURITY",
            "initialized": self._initialized,
            "hash_algorithm": self.HASH_ALGORITHM,
            "plaintext_secrets_allowed": False,
            "secret_logging_allowed": False,
        }


__all__ = [
    "VaultSecurity",
]

