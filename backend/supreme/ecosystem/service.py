
"""
MAIN BASE FOUNDATION

SUPREME — Central Ecosystem Service

Central service for managing:

- Personal profiles
- Professional profiles
- Pages
- Groups
- Channels
- Communities
- Media assets
- Entity ownership
- Vaults
- External integrations

Architecture:

SUPREME
    ↓
ECOSYSTEM
    ├── ENTITIES
    ├── OWNERSHIP
    ├── VAULT
    └── INTEGRATIONS

Every ecosystem entity may have an ownership record.

The creator can become PRIMARY_OWNER when the
creator/owner identity is supplied.

Security principle:
- Ownership controls authority.
- Vault controls protected references.
- Integration controls external connections.
- Raw credentials are never stored here.
"""

from __future__ import annotations

from typing import Dict, List, Optional, Union

from backend.supreme.ecosystem.media import (
    MediaAsset,
)

from backend.supreme.ecosystem.profile import (
    PersonalProfile,
    ProfessionalProfile,
)

from backend.supreme.ecosystem.page import (
    EcosystemPage,
)

from backend.supreme.ecosystem.community import (
    EcosystemGroup,
    EcosystemChannel,
    EcosystemCommunity,
)

from backend.supreme.ecosystem.ownership import (
    OwnershipController,
)

from backend.supreme.ecosystem.vault import (
    VaultController,
)

from backend.supreme.ecosystem.integration import (
    IntegrationController,
    IntegrationService,
)


# =========================================================
# 🌐 ECOSYSTEM ENTITY
# =========================================================

EcosystemEntity = Union[
    PersonalProfile,
    ProfessionalProfile,
    EcosystemPage,
    EcosystemGroup,
    EcosystemChannel,
    EcosystemCommunity,
    MediaAsset,
]


class EcosystemService:
    """Central SUPREME ecosystem service."""

    def __init__(self) -> None:

        # =====================================================
        # 👤 CORE ENTITY REGISTRIES
        # =====================================================

        self._personal_profiles: Dict[
            str,
            PersonalProfile,
        ] = {}

        self._professional_profiles: Dict[
            str,
            ProfessionalProfile,
        ] = {}

        self._pages: Dict[
            str,
            EcosystemPage,
        ] = {}

        self._groups: Dict[
            str,
            EcosystemGroup,
        ] = {}

        self._channels: Dict[
            str,
            EcosystemChannel,
        ] = {}

        self._communities: Dict[
            str,
            EcosystemCommunity,
        ] = {}

        self._media: Dict[
            str,
            MediaAsset,
        ] = {}

        # =====================================================
        # 👑 OWNERSHIP
        # =====================================================

        self.ownership = OwnershipController()

        # =====================================================
        # 🔐 CENTRAL VAULT
        # =====================================================

        self.vault = VaultController()

        # =====================================================
        # 🔌 CENTRAL INTEGRATION
        #
        # IMPORTANT:
        # IntegrationService receives the SAME VaultService
        # instance used by the central Ecosystem Vault.
        # =====================================================

        self.integration = IntegrationController(
            service=IntegrationService(
                vault_service=self.vault.service
            )
        )

        # =====================================================
        # 🚀 STATE
        # =====================================================

        self._initialized = False

    # =========================================================
    # 🚀 INITIALIZE
    # =========================================================

    def initialize(self) -> dict:
        """Initialize the complete ecosystem."""

        ownership_status = (
            self.ownership.initialize()
        )

        vault_status = (
            self.vault.initialize()
        )

        integration_status = (
            self.integration.initialize()
        )

        self._initialized = True

        return {
            "service": "SUPREME_ECOSYSTEM",
            "status": "READY",
            "initialized": True,
            "layers": {
                "ownership": ownership_status,
                "vault": vault_status,
                "integration": integration_status,
            },
        }

    # =========================================================
    # 👑 INTERNAL OWNERSHIP CREATION
    # =========================================================

    def _create_entity_ownership(
        self,
        entity_id: str,
        primary_owner_id: Optional[str],
    ) -> None:
        """
        Create ownership for an entity.

        If a creator/owner identity is supplied,
        that identity becomes PRIMARY_OWNER.
        """

        if primary_owner_id is None:
            return

        if not isinstance(
            primary_owner_id,
            str,
        ):
            raise TypeError(
                "primary_owner_id must be a string."
            )

        if not primary_owner_id.strip():
            raise ValueError(
                "primary_owner_id cannot be empty."
            )

        self.ownership.create_ownership(
            entity_id=entity_id,
            primary_owner_id=primary_owner_id,
        )

    # =========================================================
    # 👤 PERSONAL PROFILE
    # =========================================================

    def create_personal_profile(
        self,
        profile: PersonalProfile,
        primary_owner_id: Optional[str] = None,
    ) -> PersonalProfile:

        self._personal_profiles[
            profile.profile_id
        ] = profile

        self._create_entity_ownership(
            entity_id=profile.profile_id,
            primary_owner_id=primary_owner_id,
        )

        return profile

    def get_personal_profile(
        self,
        profile_id: str,
    ) -> Optional[PersonalProfile]:

        return self._personal_profiles.get(
            profile_id
        )

    def delete_personal_profile(
        self,
        profile_id: str,
    ) -> bool:

        return (
            self._personal_profiles.pop(
                profile_id,
                None,
            )
            is not None
        )

    def list_personal_profiles(
        self,
    ) -> List[PersonalProfile]:

        return list(
            self._personal_profiles.values()
        )

    # =========================================================
    # 💼 PROFESSIONAL PROFILE
    # =========================================================

    def create_professional_profile(
        self,
        profile: ProfessionalProfile,
        primary_owner_id: Optional[str] = None,
    ) -> ProfessionalProfile:

        self._professional_profiles[
            profile.profile_id
        ] = profile

        self._create_entity_ownership(
            entity_id=profile.profile_id,
            primary_owner_id=primary_owner_id,
        )

        return profile

    def get_professional_profile(
        self,
        profile_id: str,
    ) -> Optional[ProfessionalProfile]:

        return self._professional_profiles.get(
            profile_id
        )

    def delete_professional_profile(
        self,
        profile_id: str,
    ) -> bool:

        return (
            self._professional_profiles.pop(
                profile_id,
                None,
            )
            is not None
        )

    def list_professional_profiles(
        self,
    ) -> List[ProfessionalProfile]:

        return list(
            self._professional_profiles.values()
        )

    # =========================================================
    # 📄 PAGE
    # =========================================================

    def create_page(
        self,
        page: EcosystemPage,
        primary_owner_id: Optional[str] = None,
    ) -> EcosystemPage:

        self._pages[
            page.page_id
        ] = page

        self._create_entity_ownership(
            entity_id=page.page_id,
            primary_owner_id=primary_owner_id,
        )

        return page

    def get_page(
        self,
        page_id: str,
    ) -> Optional[EcosystemPage]:

        return self._pages.get(
            page_id
        )

    def delete_page(
        self,
        page_id: str,
    ) -> bool:

        return (
            self._pages.pop(
                page_id,
                None,
            )
            is not None
        )

    def list_pages(
        self,
    ) -> List[EcosystemPage]:

        return list(
            self._pages.values()
        )

    # =========================================================
    # 👥 GROUP
    # =========================================================

    def create_group(
        self,
        group: EcosystemGroup,
        primary_owner_id: Optional[str] = None,
    ) -> EcosystemGroup:

        self._groups[
            group.group_id
        ] = group

        self._create_entity_ownership(
            entity_id=group.group_id,
            primary_owner_id=primary_owner_id,
        )

        return group

    def get_group(
        self,
        group_id: str,
    ) -> Optional[EcosystemGroup]:

        return self._groups.get(
            group_id
        )

    def delete_group(
        self,
        group_id: str,
    ) -> bool:

        return (
            self._groups.pop(
                group_id,
                None,
            )
            is not None
        )

    def list_groups(
        self,
    ) -> List[EcosystemGroup]:

        return list(
            self._groups.values()
        )

    # =========================================================
    # 📢 CHANNEL
    # =========================================================

    def create_channel(
        self,
        channel: EcosystemChannel,
        primary_owner_id: Optional[str] = None,
    ) -> EcosystemChannel:

        self._channels[
            channel.channel_id
        ] = channel

        self._create_entity_ownership(
            entity_id=channel.channel_id,
            primary_owner_id=primary_owner_id,
        )

        return channel

    def get_channel(
        self,
        channel_id: str,
    ) -> Optional[EcosystemChannel]:

        return self._channels.get(
            channel_id
        )

    def delete_channel(
        self,
        channel_id: str,
    ) -> bool:

        return (
            self._channels.pop(
                channel_id,
                None,
            )
            is not None
        )

    def list_channels(
        self,
    ) -> List[EcosystemChannel]:

        return list(
            self._channels.values()
        )

    # =========================================================
    # 🌐 COMMUNITY
    # =========================================================

    def create_community(
        self,
        community: EcosystemCommunity,
        primary_owner_id: Optional[str] = None,
    ) -> EcosystemCommunity:

        self._communities[
            community.community_id
        ] = community

        self._create_entity_ownership(
            entity_id=community.community_id,
            primary_owner_id=primary_owner_id,
        )

        return community

    def get_community(
        self,
        community_id: str,
    ) -> Optional[EcosystemCommunity]:

        return self._communities.get(
            community_id
        )

    def delete_community(
        self,
        community_id: str,
    ) -> bool:

        return (
            self._communities.pop(
                community_id,
                None,
            )
            is not None
        )

    def list_communities(
        self,
    ) -> List[EcosystemCommunity]:

        return list(
            self._communities.values()
        )

    # =========================================================
    # 🖼️ MEDIA
    # =========================================================

    def register_media(
        self,
        media: MediaAsset,
    ) -> MediaAsset:

        self._media[
            media.media_id
        ] = media

        return media

    def get_media(
        self,
        media_id: str,
    ) -> Optional[MediaAsset]:

        return self._media.get(
            media_id
        )

    def delete_media(
        self,
        media_id: str,
    ) -> bool:

        return (
            self._media.pop(
                media_id,
                None,
            )
            is not None
        )

    def list_media(
        self,
    ) -> List[MediaAsset]:

        return list(
            self._media.values()
        )

    # =========================================================
    # 👑 OWNERSHIP ACCESS
    # =========================================================

    def get_ownership(
        self,
        entity_id: str,
    ):
        """Return entity ownership."""

        return self.ownership.get_ownership(
            entity_id
        )

    def ownership_status(self) -> dict:
        """Return ownership subsystem status."""

        return self.ownership.status()

    # =========================================================
    # 🔐 VAULT ACCESS
    # =========================================================

    def get_vault(
        self,
        vault_id: str,
    ):
        """Return a vault."""

        return self.vault.get_vault(
            vault_id
        )

    def vault_status(self) -> dict:
        """Return vault subsystem status."""

        return self.vault.status()

    # =========================================================
    # 🔌 INTEGRATION ACCESS
    # =========================================================

    def get_integration(
        self,
        integration_id: str,
        requested_by: str,
    ):
        """Return an authorized integration."""

        return self.integration.get_integration(
            integration_id=integration_id,
            requested_by=requested_by,
        )

    def integration_status(self) -> dict:
        """Return integration subsystem status."""

        return self.integration.status()

    # =========================================================
    # 📊 COMPLETE STATUS
    # =========================================================

    def status(self) -> dict:
        """Return complete ecosystem status."""

        return {
            "service": "SUPREME_ECOSYSTEM",
            "initialized": self._initialized,

            "entities": {
                "personal_profiles": len(
                    self._personal_profiles
                ),
                "professional_profiles": len(
                    self._professional_profiles
                ),
                "pages": len(
                    self._pages
                ),
                "groups": len(
                    self._groups
                ),
                "channels": len(
                    self._channels
                ),
                "communities": len(
                    self._communities
                ),
                "media": len(
                    self._media
                ),
            },

            "ownership": (
                self.ownership.status()
            ),

            "vault": (
                self.vault.status()
            ),

            "integration": (
                self.integration.status()
            ),
        }


__all__ = [
    "EcosystemEntity",
    "EcosystemService",
]
