"""Profile persistence and management service."""

import json
from datetime import datetime, timezone
from typing import Optional

from backend.database.service import DatabaseService
from backend.profiles.model import Profile


class ProfileService:
    """Manage multiple profiles for master identities."""

    PROFILE_TYPES = {
        "PERSONAL",
        "BUSINESS",
        "COMPANY",
        "FARM",
        "SHOP",
    }

    def __init__(self):
        self.database_service = DatabaseService()
        self.initialize()

    def initialize(self):
        self.database_service.initialize()

        self.database_service.execute(
            """
            CREATE TABLE IF NOT EXISTS profiles (
                profile_id TEXT PRIMARY KEY,
                master_id TEXT NOT NULL,
                profile_type TEXT NOT NULL,
                profile_name TEXT NOT NULL,
                display_name TEXT NOT NULL DEFAULT '',
                description TEXT NOT NULL DEFAULT '',
                language TEXT NOT NULL DEFAULT 'en',
                country TEXT NOT NULL DEFAULT '',
                state TEXT NOT NULL DEFAULT '',
                city TEXT NOT NULL DEFAULT '',
                verified INTEGER NOT NULL DEFAULT 0,
                status TEXT NOT NULL DEFAULT 'ACTIVE',
                metadata TEXT NOT NULL DEFAULT '{}',
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )

        return {
            "success": True,
            "message": "Profile storage initialized",
        }

    def create_profile(
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
        verified: bool = False,
        status: str = "ACTIVE",
        metadata: Optional[dict] = None,
    ) -> Profile:

        normalized_type = profile_type.strip().upper()

        if normalized_type not in self.PROFILE_TYPES:
            raise ValueError(
                f"Unsupported profile type: {normalized_type}"
            )

        now = datetime.now(timezone.utc).isoformat()

        profile = Profile(
            profile_id=profile_id,
            master_id=master_id,
            profile_type=normalized_type,
            profile_name=profile_name,
            display_name=display_name,
            description=description,
            language=language,
            country=country,
            state=state,
            city=city,
            verified=verified,
            status=status,
            metadata=metadata or {},
            created_at=now,
            updated_at=now,
        )

        self.database_service.execute(
            """
            INSERT INTO profiles (
                profile_id,
                master_id,
                profile_type,
                profile_name,
                display_name,
                description,
                language,
                country,
                state,
                city,
                verified,
                status,
                metadata,
                created_at,
                updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                profile.profile_id,
                profile.master_id,
                profile.profile_type,
                profile.profile_name,
                profile.display_name,
                profile.description,
                profile.language,
                profile.country,
                profile.state,
                profile.city,
                int(profile.verified),
                profile.status,
                json.dumps(profile.metadata),
                profile.created_at,
                profile.updated_at,
            ),
        )

        return profile

    def _row_to_profile(self, row) -> Profile:
        try:
            metadata = json.loads(row["metadata"])
        except (TypeError, json.JSONDecodeError):
            metadata = {}

        return Profile(
            profile_id=row["profile_id"],
            master_id=row["master_id"],
            profile_type=row["profile_type"],
            profile_name=row["profile_name"],
            display_name=row["display_name"],
            description=row["description"],
            language=row["language"],
            country=row["country"],
            state=row["state"],
            city=row["city"],
            verified=bool(row["verified"]),
            status=row["status"],
            metadata=metadata,
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )

    def get_profile(
        self,
        profile_id: str,
    ) -> Optional[Profile]:

        row = self.database_service.fetchone(
            """
            SELECT *
            FROM profiles
            WHERE profile_id = ?
            """,
            (profile_id,),
        )

        if row is None:
            return None

        return self._row_to_profile(row)

    def get_profiles_for_identity(
        self,
        master_id: str,
    ) -> list[Profile]:

        rows = self.database_service.fetchall(
            """
            SELECT *
            FROM profiles
            WHERE master_id = ?
            ORDER BY created_at DESC
            """,
            (master_id,),
        )

        return [
            self._row_to_profile(row)
            for row in rows
        ]

    def get_profiles_by_type(
        self,
        profile_type: str,
    ) -> list[Profile]:

        normalized_type = profile_type.strip().upper()

        rows = self.database_service.fetchall(
            """
            SELECT *
            FROM profiles
            WHERE profile_type = ?
            ORDER BY created_at DESC
            """,
            (normalized_type,),
        )

        return [
            self._row_to_profile(row)
            for row in rows
        ]

    def update_status(
        self,
        profile_id: str,
        status: str,
    ) -> Optional[Profile]:

        profile = self.get_profile(profile_id)

        if profile is None:
            return None

        now = datetime.now(timezone.utc).isoformat()

        self.database_service.execute(
            """
            UPDATE profiles
            SET status = ?, updated_at = ?
            WHERE profile_id = ?
            """,
            (
                status,
                now,
                profile_id,
            ),
        )

        return self.get_profile(profile_id)


__all__ = ["ProfileService"]
