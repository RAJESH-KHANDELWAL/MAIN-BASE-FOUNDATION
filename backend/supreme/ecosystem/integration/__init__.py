
"""
MAIN BASE FOUNDATION

SUPREME — Ecosystem Integration Public Interface

Central public interface for:

- Integration providers
- Integration types
- Integration status
- Credential references
- Ecosystem integrations
- Authorization records
- Access decisions
- Integration service
- Integration controller
"""

# =========================================================
# 🌐 INTEGRATION MODELS
# =========================================================

from .model import (
    IntegrationProvider,
    IntegrationType,
    IntegrationStatus,
    IntegrationCredentialReference,
    EcosystemIntegration,
    IntegrationAuthorization,
    IntegrationAccessDecision,
)


# =========================================================
# 🧠 INTEGRATION SERVICE
# =========================================================

from .service import (
    IntegrationService,
)


# =========================================================
# 🎛️ INTEGRATION CONTROLLER
# =========================================================

from .controller import (
    IntegrationController,
)


# =========================================================
# 📦 PUBLIC API
# =========================================================

__all__ = [

    # Providers
    "IntegrationProvider",

    # Integration types
    "IntegrationType",

    # Lifecycle
    "IntegrationStatus",

    # Credentials
    "IntegrationCredentialReference",

    # Integration
    "EcosystemIntegration",

    # Authorization
    "IntegrationAuthorization",

    # Access
    "IntegrationAccessDecision",

    # Service
    "IntegrationService",

    # Controller
    "IntegrationController",
]
