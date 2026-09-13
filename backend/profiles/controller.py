"""MAIN BASE FOUNDATION profile controller."""

from __future__ import annotations

from typing import Any, Optional

from backend.profiles.model import Profile
from backend.profiles.service import ProfileService


class ProfileController:
    """Application-level controller for universal profiles."""

    def __init__(self, service: Optional[ProfileService] = None):
        self.service = service or ProfileService()

    def create(
        self,
        profile_id: str,
        master_id: str,
        profile_type: str,
        profile_name: str,
        display_name: str = "",
        description: str = "",
        language: str = "en",
        country: str = "",
        state: str = "",
        city: str = "",
        metadata: Optional[dict[str, Any]] = None,
    ) -> Profile:
        """Create a universal profile."""

        profile = Profile(
            profile_id=profile_id,
            master_id=master_id,
            profile_type=profile_type,
            profile_name=profile_name,
            display_name=display_name,
            description=description,
            language=language,
            country=country,
            state=state,
            city=city,
            metadata=metadata or {},
        )

        return self.service.create_profile(profile)

    def get(self, profile_id: str) -> Optional[Profile]:
        """Get a profile by ID."""

        return self.service.get_profile(profile_id)

    def list(
        self,
        master_id: Optional[str] = None,
        profile_type: Optional[str] = None,
        status: Optional[str] = None,
    ) -> list[Profile]:
        """List profiles using optional filters."""

        return self.service.list_profiles(
            master_id=master_id,
            profile_type=profile_type,
            status=status,
        )

    def update(
        self,
        profile_id: str,
        updates: dict[str, Any],
    ) -> Optional[Profile]:
        """Update a profile."""

        return self.service.update_profile(
            profile_id=profile_id,
            updates=updates,
        )

    def delete(self, profile_id: str) -> bool:
        """Delete a profile."""

        return self.service.delete_profile(profile_id)

    def exists(self, profile_id: str) -> bool:
        """Check whether a profile exists."""

        return self.service.profile_exists(profile_id)


__all__ = ["ProfileController"]
