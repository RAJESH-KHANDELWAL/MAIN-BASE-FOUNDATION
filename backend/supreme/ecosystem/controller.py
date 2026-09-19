
"""
MAIN BASE FOUNDATION

SUPREME — Ecosystem Controller

Central controller for:

- Personal profiles
- Professional profiles
- Pages
- Groups
- Channels
- Communities
- Media
- Ownership
- Vault
- Integrations

The controller coordinates ecosystem requests
and delegates business operations to EcosystemService.
"""

from __future__ import annotations

from typing import List, Optional

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

from backend.supreme.ecosystem.service import (
    EcosystemService,
)


class EcosystemController:
    """Central controller for the SUPREME ecosystem."""

    def __init__(
        self,
        service: Optional[EcosystemService] = None,
    ) -> None:

        self.service = (
            service
            if service is not None
            else EcosystemService()
        )

    # =========================================================
    # 🚀 INITIALIZATION
    # =========================================================

    def initialize(self) -> dict:
        """Initialize the complete ecosystem."""

        return self.service.initialize()

    # =========================================================
    # 👤 PERSONAL PROFILE
    # =========================================================

    def create_personal_profile(
        self,
        profile: PersonalProfile,
        primary_owner_id: Optional[str] = None,
    ) -> PersonalProfile:

        return self.service.create_personal_profile(
            profile=profile,
            primary_owner_id=primary_owner_id,
        )

    def get_personal_profile(
        self,
        profile_id: str,
    ) -> Optional[PersonalProfile]:

        return self.service.get_personal_profile(
            profile_id
        )

    def delete_personal_profile(
        self,
        profile_id: str,
    ) -> bool:

        return self.service.delete_personal_profile(
            profile_id
        )

    def list_personal_profiles(
        self,
    ) -> List[PersonalProfile]:

        return self.service.list_personal_profiles()

    # =========================================================
    # 💼 PROFESSIONAL PROFILE
    # =========================================================

    def create_professional_profile(
        self,
        profile: ProfessionalProfile,
        primary_owner_id: Optional[str] = None,
    ) -> ProfessionalProfile:

        return self.service.create_professional_profile(
            profile=profile,
            primary_owner_id=primary_owner_id,
        )

    def get_professional_profile(
        self,
        profile_id: str,
    ) -> Optional[ProfessionalProfile]:

        return self.service.get_professional_profile(
            profile_id
        )

    def delete_professional_profile(
        self,
        profile_id: str,
    ) -> bool:

        return self.service.delete_professional_profile(
            profile_id
        )

    def list_professional_profiles(
        self,
    ) -> List[ProfessionalProfile]:

        return self.service.list_professional_profiles()

    # =========================================================
    # 📄 PAGE
    # =========================================================

    def create_page(
        self,
        page: EcosystemPage,
        primary_owner_id: Optional[str] = None,
    ) -> EcosystemPage:

        return self.service.create_page(
            page=page,
            primary_owner_id=primary_owner_id,
        )

    def get_page(
        self,
        page_id: str,
    ) -> Optional[EcosystemPage]:

        return self.service.get_page(
            page_id
        )

    def delete_page(
        self,
        page_id: str,
    ) -> bool:

        return self.service.delete_page(
            page_id
        )

    def list_pages(
        self,
    ) -> List[EcosystemPage]:

        return self.service.list_pages()

    # =========================================================
    # 👥 GROUP
    # =========================================================

    def create_group(
        self,
        group: EcosystemGroup,
        primary_owner_id: Optional[str] = None,
    ) -> EcosystemGroup:

        return self.service.create_group(
            group=group,
            primary_owner_id=primary_owner_id,
        )

    def get_group(
        self,
        group_id: str,
    ) -> Optional[EcosystemGroup]:

        return self.service.get_group(
            group_id
        )

    def delete_group(
        self,
        group_id: str,
    ) -> bool:

        return self.service.delete_group(
            group_id
        )

    def list_groups(
        self,
    ) -> List[EcosystemGroup]:

        return self.service.list_groups()

    # =========================================================
    # 📢 CHANNEL
    # =========================================================

    def create_channel(
        self,
        channel: EcosystemChannel,
        primary_owner_id: Optional[str] = None,
    ) -> EcosystemChannel:

        return self.service.create_channel(
            channel=channel,
            primary_owner_id=primary_owner_id,
        )

    def get_channel(
        self,
        channel_id: str,
    ) -> Optional[EcosystemChannel]:

        return self.service.get_channel(
            channel_id
        )

    def delete_channel(
        self,
        channel_id: str,
    ) -> bool:

        return self.service.delete_channel(
            channel_id
        )

    def list_channels(
        self,
    ) -> List[EcosystemChannel]:

        return self.service.list_channels()

    # =========================================================
    # 🌐 COMMUNITY
    # =========================================================

    def create_community(
        self,
        community: EcosystemCommunity,
        primary_owner_id: Optional[str] = None,
    ) -> EcosystemCommunity:

        return self.service.create_community(
            community=community,
            primary_owner_id=primary_owner_id,
        )

    def get_community(
        self,
        community_id: str,
    ) -> Optional[EcosystemCommunity]:

        return self.service.get_community(
            community_id
        )

    def delete_community(
        self,
        community_id: str,
    ) -> bool:

        return self.service.delete_community(
            community_id
        )

    def list_communities(
        self,
    ) -> List[EcosystemCommunity]:

        return self.service.list_communities()

    # =========================================================
    # 🖼️ MEDIA
    # =========================================================

    def register_media(
        self,
        media: MediaAsset,
    ) -> MediaAsset:

        return self.service.register_media(
            media
        )

    def get_media(
        self,
        media_id: str,
    ) -> Optional[MediaAsset]:

        return self.service.get_media(
            media_id
        )

    def delete_media(
        self,
        media_id: str,
    ) -> bool:

        return self.service.delete_media(
            media_id
        )

    def list_media(
        self,
    ) -> List[MediaAsset]:

        return self.service.list_media()

    # =========================================================
    # 👑 OWNERSHIP
    # =========================================================

    def get_ownership(
        self,
        entity_id: str,
    ):

        return self.service.get_ownership(
            entity_id
        )

    def ownership_status(
        self,
    ) -> dict:

        return self.service.ownership_status()

    # =========================================================
    # 🔐 VAULT
    # =========================================================

    def get_vault(
        self,
        vault_id: str,
    ):

        return self.service.get_vault(
            vault_id
        )

    def vault_status(
        self,
    ) -> dict:

        return self.service.vault_status()

    # =========================================================
    # 🔌 INTEGRATION
    # =========================================================

    def get_integration(
        self,
        integration_id: str,
        requested_by: str,
    ):

        return self.service.get_integration(
            integration_id=integration_id,
            requested_by=requested_by,
        )

    def integration_status(
        self,
    ) -> dict:

        return self.service.integration_status()

    # =========================================================
    # 📊 STATUS
    # =========================================================

    def status(self) -> dict:
        """Return complete ecosystem controller status."""

        return {
            "controller": "SUPREME_ECOSYSTEM",
            "service": self.service.status(),
        }


__all__ = [
    "EcosystemController",
]
