"""
MAIN BASE FOUNDATION

SUPREME — Ecosystem Vault Controller

Central public control entry point for:

- SUPREME Owner Vaults
- User Vaults
- Business Vaults
- Vault access
- Vault locking/unlocking
- Integration references
- Vault status

The controller delegates vault business rules
to VaultService.
"""

from __future__ import annotations

from typing import List, Optional

from backend.supreme.ecosystem.vault.model import (
    EcosystemVault,
    VaultAccessDecision,
    VaultIntegrationReference,
    VaultType,
)

from backend.supreme.ecosystem.vault.service import (
    VaultService,
)


class VaultController:
    """Central controller for SUPREME ecosystem vaults."""

    def __init__(
        self,
        service: Optional[VaultService] = None,
    ) -> None:

        self.service = (
            service
            if service is not None
            else VaultService()
        )

    # =========================================================
    # 🚀 INITIALIZATION
    # =========================================================

    def initialize(self) -> dict:
        """Initialize vault control."""

        return self.service.initialize()

    # =========================================================
    # 🔐 CREATE VAULT
    # =========================================================

    def create_vault(
        self,
        vault_id: str,
        owner_id: str,
        vault_type: VaultType,
        name: str = "",
    ) -> EcosystemVault:
        """Create an isolated ecosystem vault."""

        return self.service.create_vault(
            vault_id=vault_id,
            owner_id=owner_id,
            vault_type=vault_type,
            name=name,
        )

    # =========================================================
    # 🔎 GET VAULT
    # =========================================================

    def get_vault(
        self,
        vault_id: str,
    ) -> Optional[EcosystemVault]:
        """Return a vault."""

        return self.service.get_vault(
            vault_id
        )

    # =========================================================
    # 📋 LIST VAULTS
    # =========================================================

    def list_vaults(
        self,
    ) -> List[EcosystemVault]:
        """Return all registered vaults."""

        return self.service.list_vaults()

    # =========================================================
    # 🔒 LOCK VAULT
    # =========================================================

    def lock_vault(
        self,
        vault_id: str,
        requested_by: str,
    ) -> EcosystemVault:
        """Lock a vault."""

        return self.service.lock_vault(
            vault_id=vault_id,
            requested_by=requested_by,
        )

    # =========================================================
    # 🔓 UNLOCK VAULT
    # =========================================================

    def unlock_vault(
        self,
        vault_id: str,
        requested_by: str,
    ) -> EcosystemVault:
        """Unlock a vault."""

        return self.service.unlock_vault(
            vault_id=vault_id,
            requested_by=requested_by,
        )

    # =========================================================
    # 🔌 REGISTER INTEGRATION
    # =========================================================

    def register_integration(
        self,
        reference: VaultIntegrationReference,
        requested_by: str,
    ) -> VaultIntegrationReference:
        """
        Register an external integration reference
        inside an authorized vault.
        """

        return self.service.register_integration(
            reference=reference,
            requested_by=requested_by,
        )

    # =========================================================
    # 🔎 GET INTEGRATION
    # =========================================================

    def get_integration(
        self,
        reference_id: str,
        requested_by: str,
    ) -> Optional[
        VaultIntegrationReference
    ]:
        """Return an authorized integration reference."""

        return self.service.get_integration(
            reference_id=reference_id,
            requested_by=requested_by,
        )

    # =========================================================
    # 📋 LIST INTEGRATIONS
    # =========================================================

    def list_integrations(
        self,
        vault_id: str,
        requested_by: str,
    ) -> List[
        VaultIntegrationReference
    ]:
        """Return authorized integration references."""

        return self.service.list_integrations(
            vault_id=vault_id,
            requested_by=requested_by,
        )

    # =========================================================
    # ❌ REMOVE INTEGRATION
    # =========================================================

    def remove_integration(
        self,
        reference_id: str,
        requested_by: str,
    ) -> bool:
        """Disable an integration reference."""

        return self.service.remove_integration(
            reference_id=reference_id,
            requested_by=requested_by,
        )

    # =========================================================
    # 🛡️ ACCESS CHECK
    # =========================================================

    def check_access(
        self,
        vault_id: str,
        user_id: str,
        action: str,
    ) -> VaultAccessDecision:
        """Check access to a vault operation."""

        return self.service.check_access(
            vault_id=vault_id,
            user_id=user_id,
            action=action,
        )

    # =========================================================
    # 📊 STATUS
    # =========================================================

    def status(self) -> dict:
        """Return vault controller status."""

        return {
            "controller": (
                "SUPREME_ECOSYSTEM_VAULT"
            ),
            "service": self.service.status(),
        }


__all__ = [
    "VaultController",
]
