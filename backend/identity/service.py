"""Identity persistence and business logic."""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from backend.database.service import DatabaseService
from backend.identity.generator import IdentityGenerator
from backend.identity.model import MasterIdentity
from backend.identity.validator import IdentityValidator


class IdentityService:
    """Manage master identities."""

    def __init__(self):
        self.database = DatabaseService()
        self.generator = IdentityGenerator()
        self.validator = IdentityValidator()
        self.initialize()

    @staticmethod
    def _utc_now() -> str:
        return datetime.utcnow().isoformat()

    def initialize(self):
        """Create and migrate the master identity table."""
        self.database.initialize()

        self.database.execute(
            """
            CREATE TABLE IF NOT EXISTS master_identity (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                master_id TEXT NOT NULL UNIQUE,
                identity_id TEXT NOT NULL UNIQUE,
                supreme_id TEXT,
                full_name TEXT NOT NULL,
                display_name TEXT,
                username TEXT NOT NULL UNIQUE,
                email TEXT NOT NULL,
                phone TEXT NOT NULL,
                country TEXT,
                state TEXT,
                city TEXT,
                language TEXT DEFAULT 'en',
                timezone TEXT DEFAULT 'UTC',
                status TEXT DEFAULT 'ACTIVE',
                verified INTEGER DEFAULT 0,
                profile_photo TEXT DEFAULT '',
                profile_type TEXT DEFAULT 'PERSONAL',
                version INTEGER DEFAULT 1,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )

        self._migrate_columns()

    def _migrate_columns(self):
        """Add identity columns when upgrading an older database."""
        rows = self.database.fetchall(
            "PRAGMA table_info(master_identity)"
        )

        existing_columns = {
            row["name"]
            for row in rows
        }

        migrations = {
            "profile_photo": (
                "ALTER TABLE master_identity "
                "ADD COLUMN profile_photo TEXT DEFAULT ''"
            ),
            "profile_type": (
                "ALTER TABLE master_identity "
                "ADD COLUMN profile_type TEXT DEFAULT 'PERSONAL'"
            ),
            "version": (
                "ALTER TABLE master_identity "
                "ADD COLUMN version INTEGER DEFAULT 1"
            ),
        }

        for column, statement in migrations.items():
            if column not in existing_columns:
                self.database.execute(statement)

    def create_identity(
        self,
        full_name: str,
        username: str,
        email: str,
        phone: str,
        supreme_id: str = "",
        display_name: str = "",
        country: str = "",
        state: str = "",
        city: str = "",
        language: str = "en",
        timezone: str = "UTC",
        status: str = "ACTIVE",
        profile_photo: str = "",
        profile_type: str = "PERSONAL",
    ) -> MasterIdentity:
        """Create a new master identity."""

        full_name = full_name.strip()
        username = username.strip()
        email = email.strip()
        phone = phone.strip()
        display_name = (
            display_name.strip()
            if display_name
            else full_name
        )

        status = status.strip().upper()
        profile_type = profile_type.strip().upper()

        if not full_name:
            raise ValueError("Full name is required.")

        if not self.validator.validate_username(username):
            raise ValueError("Invalid username.")

        if not self.validator.validate_email(email):
            raise ValueError("Invalid email.")

        if not self.validator.validate_phone(phone):
            raise ValueError("Invalid phone number.")

        if not self.validator.validate_status(status):
            raise ValueError("Invalid identity status.")

        if self.search_identity(username):
            raise ValueError("Username already exists.")

        master_id = self.generator.generate_master_id()
        identity_id = self.generator.generate_identity_id()

        while self.identity_exists(master_id):
            master_id = self.generator.generate_master_id()

        return MasterIdentity(
            master_id=master_id,
            identity_id=identity_id,
            supreme_id=supreme_id.strip(),
            full_name=full_name,
            display_name=display_name,
            username=username,
            email=email,
            phone=phone,
            country=country.strip(),
            state=state.strip(),
            city=city.strip(),
            language=language.strip() or "en",
            timezone=timezone.strip() or "UTC",
            status=status,
            verified=False,
            profile_photo=profile_photo.strip(),
            profile_type=profile_type or "PERSONAL",
            version=1,
        )

    def save_identity(
        self,
        identity: MasterIdentity,
    ) -> MasterIdentity:
        """Persist an identity."""
        self.database.execute(
            """
            INSERT INTO master_identity (
                master_id,
                identity_id,
                supreme_id,
                full_name,
                display_name,
                username,
                email,
                phone,
                country,
                state,
                city,
                language,
                timezone,
                status,
                verified,
                profile_photo,
                profile_type,
                version,
                created_at,
                updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                identity.master_id,
                identity.identity_id,
                identity.supreme_id,
                identity.full_name,
                identity.display_name,
                identity.username,
                identity.email,
                identity.phone,
                identity.country,
                identity.state,
                identity.city,
                identity.language,
                identity.timezone,
                identity.status,
                int(identity.verified),
                identity.profile_photo,
                identity.profile_type,
                identity.version,
                identity.created_at,
                identity.updated_at,
            ),
        )

        return identity

    @staticmethod
    def _row_to_identity(row) -> MasterIdentity:
        """Convert a database row into a MasterIdentity."""
        return MasterIdentity(
            id=row["id"],
            master_id=row["master_id"],
            identity_id=row["identity_id"],
            supreme_id=row["supreme_id"] or "",
            full_name=row["full_name"],
            display_name=row["display_name"] or "",
            username=row["username"],
            email=row["email"],
            phone=row["phone"],
            country=row["country"] or "",
            state=row["state"] or "",
            city=row["city"] or "",
            language=row["language"] or "en",
            timezone=row["timezone"] or "UTC",
            status=row["status"] or "ACTIVE",
            verified=bool(row["verified"]),
            profile_photo=row["profile_photo"] or "",
            profile_type=row["profile_type"] or "PERSONAL",
            version=int(row["version"] or 1),
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )

    def get_identity(
        self,
        master_id: str,
    ) -> Optional[MasterIdentity]:
        """Get an identity by master ID."""
        row = self.database.fetchone(
            """
            SELECT *
            FROM master_identity
            WHERE master_id = ?
            """,
            (master_id,),
        )

        if row is None:
            return None

        return self._row_to_identity(row)

    def list_identity(self) -> list[MasterIdentity]:
        """Return all identities."""
        rows = self.database.fetchall(
            """
            SELECT *
            FROM master_identity
            ORDER BY id DESC
            """
        )

        return [
            self._row_to_identity(row)
            for row in rows
        ]

    def update_identity(
        self,
        master_id: str,
        **fields,
    ) -> Optional[MasterIdentity]:
        """Update supplied identity fields."""
        identity = self.get_identity(master_id)

        if identity is None:
            return None

        allowed_fields = {
            "supreme_id",
            "full_name",
            "display_name",
            "username",
            "email",
            "phone",
            "country",
            "state",
            "city",
            "language",
            "timezone",
            "status",
            "profile_photo",
            "profile_type",
        }

        updates = {}

        for field_name, value in fields.items():
            if field_name in allowed_fields and value is not None:
                if isinstance(value, str):
                    value = value.strip()

                updates[field_name] = value

        if "username" in updates:
            username = updates["username"]

            if not self.validator.validate_username(username):
                raise ValueError("Invalid username.")

            existing = self.search_identity(username)

            if (
                existing
                and existing.master_id != master_id
            ):
                raise ValueError(
                    "Username already exists."
                )

        if "email" in updates:
            if not self.validator.validate_email(
                updates["email"]
            ):
                raise ValueError("Invalid email.")

        if "phone" in updates:
            if not self.validator.validate_phone(
                updates["phone"]
            ):
                raise ValueError("Invalid phone number.")

        if "status" in updates:
            updates["status"] = updates["status"].upper()

            if not self.validator.validate_status(
                updates["status"]
            ):
                raise ValueError("Invalid identity status.")

        if "profile_type" in updates:
            updates["profile_type"] = (
                updates["profile_type"].upper()
            )

        if "full_name" in updates and not updates["full_name"]:
            raise ValueError("Full name cannot be empty.")

        if not updates:
            return identity

        assignments = []
        values = []

        for field_name, value in updates.items():
            assignments.append(f"{field_name} = ?")
            values.append(value)

        new_version = identity.version + 1

        assignments.append("version = ?")
        values.append(new_version)

        assignments.append("updated_at = ?")
        values.append(self._utc_now())

        values.append(master_id)

        self.database.execute(
            f"""
            UPDATE master_identity
            SET {", ".join(assignments)}
            WHERE master_id = ?
            """,
            tuple(values),
        )

        return self.get_identity(master_id)

    def delete_identity(self, master_id: str) -> bool:
        """Delete an identity."""
        identity = self.get_identity(master_id)

        if identity is None:
            return False

        self.database.execute(
            """
            DELETE FROM master_identity
            WHERE master_id = ?
            """,
            (master_id,),
        )

        return True

    def search_identity(
        self,
        keyword: str,
    ) -> Optional[MasterIdentity]:
        """Find an identity by username."""
        row = self.database.fetchone(
            """
            SELECT *
            FROM master_identity
            WHERE username = ?
            LIMIT 1
            """,
            (keyword.strip(),),
        )

        if row is None:
            return None

        return self._row_to_identity(row)

    def search_identities(
        self,
        keyword: str,
    ) -> list[MasterIdentity]:
        """Search identities by common identity fields."""
        value = f"%{keyword.strip()}%"

        rows = self.database.fetchall(
            """
            SELECT *
            FROM master_identity
            WHERE master_id LIKE ?
               OR identity_id LIKE ?
               OR username LIKE ?
               OR full_name LIKE ?
               OR email LIKE ?
            ORDER BY id DESC
            """,
            (
                value,
                value,
                value,
                value,
                value,
            ),
        )

        return [
            self._row_to_identity(row)
            for row in rows
        ]

    def verify_identity(
        self,
        master_id: str,
    ) -> Optional[MasterIdentity]:
        """Mark an identity as verified."""
        identity = self.get_identity(master_id)

        if identity is None:
            return None

        self.database.execute(
            """
            UPDATE master_identity
            SET verified = 1,
                version = version + 1,
                updated_at = ?
            WHERE master_id = ?
            """,
            (
                self._utc_now(),
                master_id,
            ),
        )

        return self.get_identity(master_id)

    def identity_exists(
        self,
        master_id: str,
    ) -> bool:
        """Check whether an identity exists."""
        row = self.database.fetchone(
            """
            SELECT master_id
            FROM master_identity
            WHERE master_id = ?
            """,
            (master_id,),
        )

        return row is not None


__all__ = ["IdentityService"]
