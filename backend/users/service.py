"""User persistence and authentication services."""

from __future__ import annotations

import hashlib
import hmac
import secrets
from typing import Optional

from backend.database.service import DatabaseService
from backend.users.model import User


class UserService:
    """Manage users and securely store password hashes."""

    PASSWORD_ITERATIONS = 310000
    PASSWORD_SALT_BYTES = 32

    def __init__(self):
        self.database = DatabaseService()
        self.initialize()

    def initialize(self):
        """Create and migrate the users table."""
        self.database.initialize()

        self.database.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                user_id TEXT PRIMARY KEY,
                full_name TEXT NOT NULL,
                username TEXT NOT NULL UNIQUE,
                email TEXT NOT NULL,
                phone TEXT NOT NULL,
                password TEXT,
                password_hash TEXT,
                role TEXT NOT NULL DEFAULT 'USER',
                status TEXT NOT NULL DEFAULT 'ACTIVE'
            )
            """
        )

        self._migrate_legacy_passwords()

    def _migrate_legacy_passwords(self):
        """Convert legacy plaintext passwords to PBKDF2 hashes."""
        rows = self.database.fetchall(
            """
            SELECT user_id, password
            FROM users
            WHERE password IS NOT NULL
              AND password != ''
              AND (password_hash IS NULL OR password_hash = '')
            """
        )

        for row in rows:
            password = row["password"]
            password_hash = self._hash_password(password)

            self.database.execute(
                """
                UPDATE users
                SET password_hash = ?,
                    password = NULL
                WHERE user_id = ?
                """,
                (password_hash, row["user_id"]),
            )

    @classmethod
    def _hash_password(cls, password: str) -> str:
        """Create a PBKDF2-HMAC-SHA256 password hash."""
        if not password:
            raise ValueError("Password is required.")

        salt = secrets.token_bytes(cls.PASSWORD_SALT_BYTES)

        derived_key = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt,
            cls.PASSWORD_ITERATIONS,
        )

        return (
            f"pbkdf2_sha256${cls.PASSWORD_ITERATIONS}$"
            f"{salt.hex()}${derived_key.hex()}"
        )

    @classmethod
    def _verify_password_hash(
        cls,
        password: str,
        stored_hash: str,
    ) -> bool:
        """Verify a PBKDF2 password hash."""
        try:
            algorithm, iterations, salt_hex, hash_hex = stored_hash.split("$")

            if algorithm != "pbkdf2_sha256":
                return False

            iterations = int(iterations)

            salt = bytes.fromhex(salt_hex)
            expected_hash = bytes.fromhex(hash_hex)

            actual_hash = hashlib.pbkdf2_hmac(
                "sha256",
                password.encode("utf-8"),
                salt,
                iterations,
            )

            return hmac.compare_digest(
                actual_hash,
                expected_hash,
            )

        except (ValueError, TypeError):
            return False

    @staticmethod
    def _generate_user_id() -> str:
        """Generate a unique user identifier."""
        return f"USR-{secrets.token_hex(8).upper()}"

    def create_user(
        self,
        full_name: str,
        username: str,
        email: str,
        phone: str,
        password: str,
        role: str = "USER",
        status: str = "ACTIVE",
        user_id: Optional[str] = None,
    ) -> User:
        """Create a new user."""
        full_name = full_name.strip()
        username = username.strip()
        email = email.strip()
        phone = phone.strip()
        role = role.strip().upper()
        status = status.strip().upper()

        if not full_name:
            raise ValueError("Full name is required.")

        if not username:
            raise ValueError("Username is required.")

        if not email:
            raise ValueError("Email is required.")

        if not phone:
            raise ValueError("Phone is required.")

        if not password:
            raise ValueError("Password is required.")

        if role not in {"USER", "ADMIN", "MANAGER", "OWNER"}:
            raise ValueError("Invalid user role.")

        if status not in {"ACTIVE", "INACTIVE", "BLOCKED", "DELETED"}:
            raise ValueError("Invalid user status.")

        if self.search_user_by_username(username):
            raise ValueError("Username already exists.")

        final_user_id = user_id.strip() if user_id else self._generate_user_id()

        if self.get_user(final_user_id):
            raise ValueError("User ID already exists.")

        user = User(
            user_id=final_user_id,
            full_name=full_name,
            username=username,
            email=email,
            phone=phone,
            role=role,
            status=status,
        )

        user._password_hash = self._hash_password(password)

        return user

    def save_user(self, user: User):
        """Persist a new user."""
        password_hash = getattr(user, "_password_hash", None)

        if not password_hash:
            raise ValueError("Password hash is missing.")

        self.database.execute(
            """
            INSERT INTO users (
                user_id,
                full_name,
                username,
                email,
                phone,
                password,
                password_hash,
                role,
                status
            )
            VALUES (?, ?, ?, ?, ?, NULL, ?, ?, ?)
            """,
            (
                user.user_id,
                user.full_name,
                user.username,
                user.email,
                user.phone,
                password_hash,
                user.role,
                user.status,
            ),
        )

        return user

    def get_user(self, user_id: str) -> Optional[User]:
        """Get a user by ID."""
        row = self.database.fetchone(
            """
            SELECT
                user_id,
                full_name,
                username,
                email,
                phone,
                role,
                status
            FROM users
            WHERE user_id = ?
            """,
            (user_id,),
        )

        if row is None:
            return None

        return User(
            user_id=row["user_id"],
            full_name=row["full_name"],
            username=row["username"],
            email=row["email"],
            phone=row["phone"],
            role=row["role"],
            status=row["status"],
        )

    def update_user(
        self,
        user_id: str,
        full_name: Optional[str] = None,
        username: Optional[str] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        password: Optional[str] = None,
        role: Optional[str] = None,
        status: Optional[str] = None,
    ) -> Optional[User]:
        """Update supplied user fields."""
        current = self.get_user(user_id)

        if current is None:
            return None

        new_full_name = (
            full_name.strip()
            if full_name is not None
            else current.full_name
        )

        new_username = (
            username.strip()
            if username is not None
            else current.username
        )

        new_email = (
            email.strip()
            if email is not None
            else current.email
        )

        new_phone = (
            phone.strip()
            if phone is not None
            else current.phone
        )

        new_role = (
            role.strip().upper()
            if role is not None
            else current.role
        )

        new_status = (
            status.strip().upper()
            if status is not None
            else current.status
        )

        if not new_full_name:
            raise ValueError("Full name cannot be empty.")

        if not new_username:
            raise ValueError("Username cannot be empty.")

        if not new_email:
            raise ValueError("Email cannot be empty.")

        if not new_phone:
            raise ValueError("Phone cannot be empty.")

        if new_role not in {"USER", "ADMIN", "MANAGER", "OWNER"}:
            raise ValueError("Invalid user role.")

        if new_status not in {
            "ACTIVE",
            "INACTIVE",
            "BLOCKED",
            "DELETED",
        }:
            raise ValueError("Invalid user status.")

        existing_username = self.search_user_by_username(new_username)

        if (
            existing_username is not None
            and existing_username.user_id != user_id
        ):
            raise ValueError("Username already exists.")

        self.database.execute(
            """
            UPDATE users
            SET
                full_name = ?,
                username = ?,
                email = ?,
                phone = ?,
                role = ?,
                status = ?
            WHERE user_id = ?
            """,
            (
                new_full_name,
                new_username,
                new_email,
                new_phone,
                new_role,
                new_status,
                user_id,
            ),
        )

        if password is not None:
            if not password:
                raise ValueError("Password cannot be empty.")

            password_hash = self._hash_password(password)

            self.database.execute(
                """
                UPDATE users
                SET password_hash = ?,
                    password = NULL
                WHERE user_id = ?
                """,
                (password_hash, user_id),
            )

        return self.get_user(user_id)

    def delete_user(self, user_id: str) -> bool:
        """Delete a user permanently."""
        existing = self.get_user(user_id)

        if existing is None:
            return False

        self.database.execute(
            """
            DELETE FROM users
            WHERE user_id = ?
            """,
            (user_id,),
        )

        return True

    def get_all_users(self) -> list[User]:
        """Return all users."""
        rows = self.database.fetchall(
            """
            SELECT
                user_id,
                full_name,
                username,
                email,
                phone,
                role,
                status
            FROM users
            ORDER BY rowid DESC
            """
        )

        return [
            User(
                user_id=row["user_id"],
                full_name=row["full_name"],
                username=row["username"],
                email=row["email"],
                phone=row["phone"],
                role=row["role"],
                status=row["status"],
            )
            for row in rows
        ]

    def search_user_by_username(
        self,
        username: str,
    ) -> Optional[User]:
        """Find a user by exact username."""
        row = self.database.fetchone(
            """
            SELECT
                user_id,
                full_name,
                username,
                email,
                phone,
                role,
                status
            FROM users
            WHERE username = ?
            """,
            (username,),
        )

        if row is None:
            return None

        return User(
            user_id=row["user_id"],
            full_name=row["full_name"],
            username=row["username"],
            email=row["email"],
            phone=row["phone"],
            role=row["role"],
            status=row["status"],
        )

    def verify_user_password(
        self,
        username: str,
        password: str,
    ) -> bool:
        """Verify a user's password."""
        row = self.database.fetchone(
            """
            SELECT password_hash, status
            FROM users
            WHERE username = ?
            """,
            (username,),
        )

        if row is None:
            return False

        if row["status"] != "ACTIVE":
            return False

        stored_hash = row["password_hash"]

        if not stored_hash:
            return False

        return self._verify_password_hash(
            password,
            stored_hash,
        )


__all__ = ["UserService"]
