
"""
MAIN BASE FOUNDATION

SUPREME — Ecosystem Integration Controller

Central public control entry point for:

- Google
- Microsoft
- AWS
- Apple
- Generic Web/API integrations
- Integration authorization
- Connection lifecycle
- Vault association
- Access verification

The controller delegates business rules
to IntegrationService.
"""

from __future__ import annotations

from typing import List, Optional

from backend.supreme.ecosystem.integration.model import (
    EcosystemIntegration,
    IntegrationAccessDecision,
    IntegrationAuthorization,
    IntegrationCredentialReference,
    IntegrationProvider,
)

from backend.supreme.ecosystem.integration.service import (
    IntegrationService,
)


class IntegrationController:
    """Central controller for SUPREME integrations."""

    def __init__(
        self,
        service: Optional[IntegrationService] = None,
    ) -> None:

        self.service = (
            service
            if service is not None
            else IntegrationService()
        )

    # =========================================================
    # 🚀 INITIALIZATION
    # =========================================================

    def initialize(self) -> dict:
        """Initialize integration control."""

        return self.service.initialize()

    # =========================================================
    # 🔌 CREATE INTEGRATION
    # =========================================================

    def create_integration(
        self,
        integration: EcosystemIntegration,
        requested_by: str,
    ) -> EcosystemIntegration:
        """Create a provider integration."""

        return self.service.create_integration(
            integration=integration,
            requested_by=requested_by,
        )

    # =========================================================
    # 🔎 GET INTEGRATION
    # =========================================================

    def get_integration(
        self,
        integration_id: str,
        requested_by: str,
    ) -> Optional[EcosystemIntegration]:
        """Return an authorized integration."""

        return self.service.get_integration(
            integration_id=integration_id,
            requested_by=requested_by,
        )

    # =========================================================
    # 📋 LIST INTEGRATIONS
    # =========================================================

    def list_integrations(
        self,
        vault_id: str,
        requested_by: str,
    ) -> List[EcosystemIntegration]:
        """List integrations belonging to a vault."""

        return self.service.list_integrations(
            vault_id=vault_id,
            requested_by=requested_by,
        )

    # =========================================================
    # 🔐 REGISTER CREDENTIAL REFERENCE
    # =========================================================

    def register_credential_reference(
        self,
        reference: IntegrationCredentialReference,
        requested_by: str,
    ) -> IntegrationCredentialReference:
        """Register a secure credential reference."""

        return self.service.register_credential_reference(
            reference=reference,
            requested_by=requested_by,
        )

    # =========================================================
    # 🔗 ATTACH CREDENTIAL
    # =========================================================

    def attach_credential(
        self,
        integration_id: str,
        credential_reference_id: str,
        requested_by: str,
    ) -> EcosystemIntegration:
        """Attach a secure credential reference."""

        return self.service.attach_credential(
            integration_id=integration_id,
            credential_reference_id=credential_reference_id,
            requested_by=requested_by,
        )

    # =========================================================
    # ✅ AUTHORIZE
    # =========================================================

    def authorize(
        self,
        integration_id: str,
        authorized_by: str,
        scopes: Optional[List[str]] = None,
        authorization_reference: Optional[str] = None,
    ) -> IntegrationAuthorization:
        """Record successful provider authorization."""

        return self.service.authorize(
            integration_id=integration_id,
            authorized_by=authorized_by,
            scopes=scopes,
            authorization_reference=(
                authorization_reference
            ),
        )

    # =========================================================
    # 🔗 MARK CONNECTED
    # =========================================================

    def mark_connected(
        self,
        integration_id: str,
        requested_by: str,
    ) -> EcosystemIntegration:
        """Mark an authorized integration as connected."""

        return self.service.mark_connected(
            integration_id=integration_id,
            requested_by=requested_by,
        )

    # =========================================================
    # 🔌 DISCONNECT
    # =========================================================

    def disconnect(
        self,
        integration_id: str,
        requested_by: str,
    ) -> EcosystemIntegration:
        """Disconnect an integration."""

        return self.service.disconnect(
            integration_id=integration_id,
            requested_by=requested_by,
        )

    # =========================================================
    # 🚫 REVOKE AUTHORIZATION
    # =========================================================

    def revoke_authorization(
        self,
        integration_id: str,
        requested_by: str,
    ) -> EcosystemIntegration:
        """Revoke provider authorization."""

        return self.service.revoke_authorization(
            integration_id=integration_id,
            requested_by=requested_by,
        )

    # =========================================================
    # 🛡️ ACCESS CHECK
    # =========================================================

    def check_access(
        self,
        integration_id: str,
        user_id: str,
        action: str,
    ) -> IntegrationAccessDecision:
        """Check access to an integration."""

        return self.service.check_access(
            integration_id=integration_id,
            user_id=user_id,
            action=action,
        )

    # =========================================================
    # 🌐 PROVIDER FILTER
    # =========================================================

    def list_by_provider(
        self,
        provider: IntegrationProvider,
        requested_by: str,
    ) -> List[EcosystemIntegration]:
        """List integrations for a provider."""

        return self.service.list_by_provider(
            provider=provider,
            requested_by=requested_by,
        )

    # =========================================================
    # 📊 STATUS
    # =========================================================

    def status(self) -> dict:
        """Return integration controller status."""

        return {
            "controller": (
                "SUPREME_ECOSYSTEM_INTEGRATION"
            ),
            "service": self.service.status(),
        }


__all__ = [
    "IntegrationController",
]
