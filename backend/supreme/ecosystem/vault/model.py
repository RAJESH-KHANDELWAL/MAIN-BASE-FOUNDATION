"""
MAIN BASE FOUNDATION

SUPREME — Ecosystem Vault Models

Secure vault models for:

- SUPREME Owner Vault
- User Vault
- Business Vault
- Integration credential references
- Vault access control
- Vault status

Security principle:
- Never store plaintext passwords.
- Never expose raw credentials through the model.
- Store references to encrypted secrets only.
- Provider authorization remains with the external provider.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Dict, List, Optional


# =========================================================
# 🕐 TIME
# =========================================================


def utc_now() -> str:
    """Return an ISO-8601 UTC timestamp."""
    return datetime.now(timezone.utc).isoformat()


# =========================================================
# 🔐 VAULT TYPE
# =========================================================


class VaultType(str, Enum):
    """Supported SUPREME ecosystem vault types."""

    SUPREME_OWNER = "SUPREME_OWNER"
    USER = "USER"
    BUSINESS = "BUSINESS"


# =========================================================
# 📊 VAULT STATUS
# =========================================================


class VaultStatus(str, Enum):
    """Vault lifecycle status."""

    ACTIVE = "ACTIVE"
    LOCKED = "LOCKED"
    SUSPENDED = "SUSPENDED"
    DISABLED = "DISABLED"


# =========================================================
# 🔑 SECRET TYPE
# =========================================================


class VaultSecretType(str, Enum):
    """Types of protected credential references."""

    PASSWORD = "PASSWORD"
    ACCESS_TOKEN = "ACCESS_TOKEN"
    REFRESH_TOKEN = "REFRESH_TOKEN"
    API_KEY = "API_KEY"
    CLIENT_SECRET = "CLIENT_SECRET"
    PRIVATE_KEY = "PRIVATE_KEY"
    OTHER = "OTHER"


# =========================================================
# 🔌 PROVIDER REFERENCE
# =========================================================


@dataclass
class VaultIntegrationReference:
    """
    Reference to an external provider credential.

    The actual secret is NOT stored here.

    Only the secure vault reference is stored.
    """

    reference_id: str

    vault_id: str

    provider: str

    account_reference: str = ""

    secret_type: VaultSecretType = (
        VaultSecretType.OTHER
    )

    encrypted_secret_reference: Optional[str] = None

    active: bool = True

    metadata: Dict[str, str] = field(
        default_factory=dict
    )

    created_at: str = field(
        default_factory=utc_now
    )

    updated_at: str = field(
        default_factory=utc_now
    )

    def __post_init__(self) -> None:

        if not self.reference_id.strip():
            raise ValueError(
                "reference_id cannot be empty."
            )

        if not self.vault_id.strip():
            raise ValueError(
                "vault_id cannot be empty."
            )

        if not self.provider.strip():
            raise ValueError(
                "provider cannot be empty."
            )


# =========================================================
# 👑 VAULT
# =========================================================


@dataclass
class EcosystemVault:
    """
    Central secure vault belonging to an ecosystem owner.

    SUPREME_OWNER vault:
        Belongs to the SUPREME owner.

    USER vault:
        Belongs to an individual user.

    BUSINESS vault:
        Belongs to a business/entity.

    Secrets themselves are never stored as plaintext.
    """

    vault_id: str

    owner_id: str

    vault_type: VaultType

    name: str = ""

    status: VaultStatus = VaultStatus.ACTIVE

    encryption_version: str = "1.0"

    integration_references: List[str] = field(
        default_factory=list
    )

    metadata: Dict[str, str] = field(
        default_factory=dict
    )

    created_at: str = field(
        default_factory=utc_now
    )

    updated_at: str = field(
        default_factory=utc_now
    )

    def __post_init__(self) -> None:

        if not self.vault_id.strip():
            raise ValueError(
                "vault_id cannot be empty."
            )

        if not self.owner_id.strip():
            raise ValueError(
                "owner_id cannot be empty."
            )

        if not self.name.strip():
            self.name = (
                f"{self.vault_type.value} VAULT"
            )


# =========================================================
# 🔐 VAULT ACCESS
# =========================================================


@dataclass
class VaultAccessPolicy:
    """
    Defines who can access a vault.

    The policy controls SUPREME-side authorization.
    """

    vault_id: str

    primary_owner_id: str

    owner_ids: List[str] = field(
        default_factory=list
    )

    admin_ids: List[str] = field(
        default_factory=list
    )

    read_allowed: bool = True

    manage_allowed: bool = False

    integration_manage_allowed: bool = False

    owner_only: bool = True

    active: bool = True

    created_at: str = field(
        default_factory=utc_now
    )

    updated_at: str = field(
        default_factory=utc_now
    )

    def __post_init__(self) -> None:

        if not self.vault_id.strip():
            raise ValueError(
                "vault_id cannot be empty."
            )

        if not self.primary_owner_id.strip():
            raise ValueError(
                "primary_owner_id cannot be empty."
            )


# =========================================================
# 🔎 VAULT ACCESS DECISION
# =========================================================


@dataclass(frozen=True)
class VaultAccessDecision:
    """Result of a vault access authorization check."""

    vault_id: str

    user_id: str

    allowed: bool

    action: str

    reason: str = ""

    checked_at: str = field(
        default_factory=utc_now
    )


# =========================================================
# 📦 PUBLIC API
# =========================================================


__all__ = [
    "VaultType",
    "VaultStatus",
    "VaultSecretType",
    "VaultIntegrationReference",
    "EcosystemVault",
    "VaultAccessPolicy",
    "VaultAccessDecision",
]
