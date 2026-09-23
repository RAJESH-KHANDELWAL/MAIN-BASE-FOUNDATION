"""
MAIN BASE FOUNDATION

SUPREME — Ecosystem Vault Service

Central service for managing:

- SUPREME Owner Vaults
- User Vaults
- Business Vaults
- Vault access policies
- Vault locking and unlocking
- Integration references
- Secure credential references

Security principle:
- Vaults are isolated by owner.
- Raw passwords and secrets are never stored.
- External credentials are represented by secure references.
- Access is explicitly checked before protected operations.
"""

from __future__ import annotations

from typing import Dict, List, Optional

from backend.supreme.ecosystem.vault.model import (
    EcosystemVault,
    VaultAccessDecision,
    VaultAccessPolicy,
    VaultIntegrationReference,
    VaultStatus,
    VaultType,
)

from backend.supreme.ecosystem.vault.security import (
    VaultSecurity,
)


class VaultService:
    """Central SUPREME ecosystem vault service."""

    def __init__(
        self,
        security: Optional[VaultSecurity] = None,
    ) -> None:

        self.security = (
            security
            if security is not None
            else VaultSecurity()
        )

        self._vaults: Dict[
            str,
            EcosystemVault,
        ] = {}

        self._policies: Dict[
            str,
            VaultAccessPolicy,
        ] = {}

        self._integrations: Dict[
            str,
            VaultIntegrationReference,
        ] = {}

        self._initialized = False

    # =========================================================
    # 🚀 INITIALIZE
    # =========================================================

    def initialize(self) -> dict:
        """Initialize the vault service."""

        self.security.initialize()

        self._initialized = True

        return {
            "service": "SUPREME_ECOSYSTEM_VAULT",
            "status": "READY",
            "initialized": True,
        }

    # =========================================================
    # 👑 CREATE VAULT
    # =========================================================

    def create_vault(
        self,
        vault_id: str,
        owner_id: str,
        vault_type: VaultType,
        name: str = "",
    ) -> EcosystemVault:
        """Create an isolated ecosystem vault."""

        if vault_id in self._vaults:
            raise ValueError(
                "Vault already exists."
            )

        vault = EcosystemVault(
            vault_id=vault_id,
            owner_id=owner_id,
            vault_type=vault_type,
            name=name,
        )

        self._vaults[
            vault.vault_id
        ] = vault

        self._policies[
            vault.vault_id
        ] = VaultAccessPolicy(
            vault_id=vault.vault_id,
            primary_owner_id=vault.owner_id,
            owner_ids=[vault.owner_id],
            owner_only=True,
        )

        return vault

    # =========================================================
    # 🔎 GET VAULT
    # =========================================================

    def get_vault(
        self,
        vault_id: str,
    ) -> Optional[EcosystemVault]:
        """Return a vault."""

        return self._vaults.get(
            vault_id
        )

    # =========================================================
    # 📋 LIST VAULTS
    # =========================================================

    def list_vaults(
        self,
    ) -> List[EcosystemVault]:
        """Return all registered vaults."""

        return list(
            self._vaults.values()
        )

    # =========================================================
    # 🔒 LOCK
    # =========================================================

    def lock_vault(
        self,
        vault_id: str,
        requested_by: str,
    ) -> EcosystemVault:
        """Lock a vault."""

        vault = self._require_vault(
            vault_id
        )

        decision = self.check_access(
            vault_id=vault_id,
            user_id=requested_by,
            action="LOCK",
        )

        if not decision.allowed:
            raise PermissionError(
                decision.reason
            )

        vault.status = VaultStatus.LOCKED

        return vault

    # =========================================================
    # 🔓 UNLOCK
    # =========================================================

    def unlock_vault(
        self,
        vault_id: str,
        requested_by: str,
    ) -> EcosystemVault:
        """Unlock a vault."""

        vault = self._require_vault(
            vault_id
        )

        decision = self.check_access(
            vault_id=vault_id,
            user_id=requested_by,
            action="UNLOCK",
        )

        if not decision.allowed:
            raise PermissionError(
                decision.reason
            )

        vault.status = VaultStatus.ACTIVE

        return vault

    # =========================================================
    # 🔐 REGISTER INTEGRATION
    # =========================================================

    def register_integration(
        self,
        reference: VaultIntegrationReference,
        requested_by: str,
    ) -> VaultIntegrationReference:
        """
        Register an external integration reference.

        The actual credential/secret is not stored here.
        """

        vault = self._require_vault(
            reference.vault_id
        )

        decision = self.check_access(
            vault_id=vault.vault_id,
            user_id=requested_by,
            action="MANAGE_INTEGRATION",
        )

        if not decision.allowed:
            raise PermissionError(
                decision.reason
            )

        if vault.status != VaultStatus.ACTIVE:
            raise PermissionError(
                "Vault is not active."
            )

        if (
            reference.reference_id
            in self._integrations
        ):
            raise ValueError(
                "Integration reference already exists."
            )

        self._integrations[
            reference.reference_id
        ] = reference

        vault.integration_references.append(
            reference.reference_id
        )

        return reference

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

        reference = self._integrations.get(
            reference_id
        )

        if reference is None:
            return None

        decision = self.check_access(
            vault_id=reference.vault_id,
            user_id=requested_by,
            action="READ_INTEGRATION",
        )

        if not decision.allowed:
            raise PermissionError(
                decision.reason
            )

        return reference

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
        """List authorized integration references."""

        self._require_vault(
            vault_id
        )

        decision = self.check_access(
            vault_id=vault_id,
            user_id=requested_by,
            action="READ_INTEGRATION",
        )

        if not decision.allowed:
            raise PermissionError(
                decision.reason
            )

        return [
            reference
            for reference
            in self._integrations.values()
            if reference.vault_id == vault_id
            and reference.active
        ]

    # =========================================================
    # ❌ REMOVE INTEGRATION
    # =========================================================

    def remove_integration(
        self,
        reference_id: str,
        requested_by: str,
    ) -> bool:
        """Remove an integration reference."""

        reference = self._integrations.get(
            reference_id
        )

        if reference is None:
            return False

        decision = self.check_access(
            vault_id=reference.vault_id,
            user_id=requested_by,
            action="MANAGE_INTEGRATION",
        )

        if not decision.allowed:
            raise PermissionError(
                decision.reason
            )

        reference.active = False

        return True

    # =========================================================
    # 🛡️ ACCESS CHECK
    # =========================================================

    def check_access(
        self,
        vault_id: str,
        user_id: str,
        action: str,
    ) -> VaultAccessDecision:
        """Check whether a user may access a vault."""

        vault = self._vaults.get(
            vault_id
        )

        policy = self._policies.get(
            vault_id
        )

        if vault is None:
            return VaultAccessDecision(
                vault_id=vault_id,
                user_id=user_id,
                allowed=False,
                action=action,
                reason="Vault does not exist.",
            )

        if policy is None:
            return VaultAccessDecision(
                vault_id=vault_id,
                user_id=user_id,
                allowed=False,
                action=action,
                reason="Vault access policy does not exist.",
            )

        if not policy.active:
            return VaultAccessDecision(
                vault_id=vault_id,
                user_id=user_id,
                allowed=False,
                action=action,
                reason="Vault access policy is inactive.",
            )

        if vault.status != VaultStatus.ACTIVE:
            return VaultAccessDecision(
                vault_id=vault_id,
                user_id=user_id,
                allowed=False,
                action=action,
                reason="Vault is not active.",
            )

        if user_id == policy.primary_owner_id:
            return VaultAccessDecision(
                vault_id=vault_id,
                user_id=user_id,
                allowed=True,
                action=action,
                reason="PRIMARY_OWNER authorized.",
            )

        if user_id in policy.owner_ids:
            return VaultAccessDecision(
                vault_id=vault_id,
                user_id=user_id,
                allowed=True,
                action=action,
                reason="OWNER authorized.",
            )

        if user_id in policy.admin_ids:

            if action in {
                "READ",
                "READ_INTEGRATION",
            } and policy.read_allowed:
                return VaultAccessDecision(
                    vault_id=vault_id,
                    user_id=user_id,
                    allowed=True,
                    action=action,
                    reason="ADMIN read access authorized.",
                )

            if action == "MANAGE_INTEGRATION":
                if policy.integration_manage_allowed:
                    return VaultAccessDecision(
                        vault_id=vault_id,
                        user_id=user_id,
                        allowed=True,
                        action=action,
                        reason=(
                            "ADMIN integration management "
                            "authorized."
                        ),
                    )

            if action in {
                "LOCK",
                "UNLOCK",
            } and policy.manage_allowed:
                return VaultAccessDecision(
                    vault_id=vault_id,
                    user_id=user_id,
                    allowed=True,
                    action=action,
                    reason="ADMIN management authorized.",
                )

        return VaultAccessDecision(
            vault_id=vault_id,
            user_id=user_id,
            allowed=False,
            action=action,
            reason="Access denied by vault policy.",
        )

    # =========================================================
    # 🔎 INTERNAL
    # =========================================================

    def _require_vault(
        self,
        vault_id: str,
    ) -> EcosystemVault:
        """Return an existing vault."""

        vault = self._vaults.get(
            vault_id
        )

        if vault is None:
            raise ValueError(
                "Vault does not exist."
            )

        return vault

    # =========================================================
    # 📊 STATUS
    # =========================================================

    def status(self) -> dict:
        """Return vault service status."""

        return {
            "service": "SUPREME_ECOSYSTEM_VAULT",
            "initialized": self._initialized,
            "vaults": len(
                self._vaults
            ),
            "integration_references": len(
                self._integrations
            ),
            "security": self.security.status(),
        }


__all__ = [
    "VaultService",
]
