"""
MAIN BASE FOUNDATION

SUPREME — Ecosystem Vault Public Interface

Central public interface for:

- SUPREME Owner Vault
- User Vault
- Business Vault
- Vault status
- Vault integration references
- Vault access policies
- Vault security
- Vault service
- Vault controller
"""

# =========================================================
# 🔐 VAULT MODELS
# =========================================================

from .model import (
    VaultType,
    VaultStatus,
    VaultSecretType,
    VaultIntegrationReference,
    EcosystemVault,
    VaultAccessPolicy,
    VaultAccessDecision,
)


# =========================================================
# 🛡️ VAULT SECURITY
# =========================================================

from .security import (
    VaultSecurity,
)


# =========================================================
# 🧠 VAULT SERVICE
# =========================================================

from .service import (
    VaultService,
)


# =========================================================
# 🎛️ VAULT CONTROLLER
# =========================================================

from .controller import (
    VaultController,
)


# =========================================================
# 📦 PUBLIC API
# =========================================================

__all__ = [

    # Vault types
    "VaultType",
    "VaultStatus",
    "VaultSecretType",

    # Vault models
    "VaultIntegrationReference",
    "EcosystemVault",
    "VaultAccessPolicy",
    "VaultAccessDecision",

    # Security
    "VaultSecurity",

    # Service
    "VaultService",

    # Controller
    "VaultController",
]
