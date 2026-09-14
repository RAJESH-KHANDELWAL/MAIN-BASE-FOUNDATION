"""
MAIN BASE FOUNDATION

SUPREME — Mukti Mahal Persistent Store

Database-backed dictionary compatible with the existing
Mukti Mahal service architecture.

The existing MuktiMahalService uses dictionaries for its
runtime collections. This store preserves that interface
while making the state persistent in the central
MAIN BASE FOUNDATION SQLite database.

No credentials, passwords, OTPs, authentication secrets,
raw identity documents, or payment credentials are stored.
"""

from __future__ import annotations

import pickle
import sqlite3
from typing import Any, Dict, Iterable, List, Optional

from backend.database.service import DatabaseService


class PersistentDict:
    """
    Small dictionary-compatible persistent store.

    Supported operations used by MuktiMahalService:

    - get()
    - values()
    - len()
    - contains / `in`
    - item assignment
    - item deletion
    - clear()
    """

    def __init__(
        self,
        name: str,
        database: Optional[DatabaseService] = None,
    ) -> None:
        if not name:
            raise ValueError("Persistent store name is required.")

        self.name = name
        self.database = database or DatabaseService()

        self.table_name = (
            "mukti_mahal_store_"
            + self._safe_name(name)
        )

        self._initialize()

    # =====================================================
    # INITIALIZATION
    # =====================================================

    def _initialize(self) -> None:
        """Initialize the persistent table."""

        self.database.initialize()

        self.database.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {self.table_name} (
                item_key TEXT PRIMARY KEY,
                item_value BLOB NOT NULL
            )
            """
        )

    # =====================================================
    # DICT INTERFACE
    # =====================================================

    def __contains__(
        self,
        key: object,
    ) -> bool:
        if key is None:
            return False

        row = self.database.fetchone(
            f"""
            SELECT item_key
            FROM {self.table_name}
            WHERE item_key = ?
            """,
            (str(key),),
        )

        return row is not None

    def __len__(self) -> int:
        row = self.database.fetchone(
            f"""
            SELECT COUNT(*)
            FROM {self.table_name}
            """
        )

        if row is None:
            return 0

        return int(row[0])

    def __getitem__(
        self,
        key: str,
    ) -> Any:
        value = self.get(key)

        if value is None:
            raise KeyError(key)

        return value

    def __setitem__(
        self,
        key: str,
        value: Any,
    ) -> None:
        if not key:
            raise ValueError(
                "Persistent store key is required."
            )

        serialized = sqlite3.Binary(
            pickle.dumps(
                value,
                protocol=pickle.HIGHEST_PROTOCOL,
            )
        )

        self.database.execute(
            f"""
            INSERT OR REPLACE INTO {self.table_name} (
                item_key,
                item_value
            )
            VALUES (?, ?)
            """,
            (
                str(key),
                serialized,
            ),
        )

    def __delitem__(
        self,
        key: str,
    ) -> None:
        affected = self.database.execute(
            f"""
            DELETE FROM {self.table_name}
            WHERE item_key = ?
            """,
            (str(key),),
        )

        if affected == 0:
            raise KeyError(key)

    # =====================================================
    # GET
    # =====================================================

    def get(
        self,
        key: str,
        default: Any = None,
    ) -> Any:
        """Return an item or default."""

        if not key:
            return default

        row = self.database.fetchone(
            f"""
            SELECT item_value
            FROM {self.table_name}
            WHERE item_key = ?
            """,
            (str(key),),
        )

        if row is None:
            return default

        try:
            return pickle.loads(row[0])
        except (
            pickle.PickleError,
            EOFError,
            TypeError,
            ValueError,
        ) as exc:
            raise RuntimeError(
                f"Unable to deserialize persistent "
                f"Mukti Mahal item: {key}"
            ) from exc

    # =====================================================
    # VALUES
    # =====================================================

    def values(self) -> List[Any]:
        """Return all stored values."""

        rows = self.database.fetchall(
            f"""
            SELECT item_value
            FROM {self.table_name}
            ORDER BY item_key ASC
            """
        )

        values: List[Any] = []

        for row in rows:
            try:
                values.append(
                    pickle.loads(row[0])
                )
            except (
                pickle.PickleError,
                EOFError,
                TypeError,
                ValueError,
            ) as exc:
                raise RuntimeError(
                    "Unable to deserialize a stored "
                    "Mukti Mahal item."
                ) from exc

        return values

    # =====================================================
    # ITEMS
    # =====================================================

    def items(self) -> List[tuple[str, Any]]:
        """Return all stored key/value pairs."""

        rows = self.database.fetchall(
            f"""
            SELECT item_key, item_value
            FROM {self.table_name}
            ORDER BY item_key ASC
            """
        )

        result: List[tuple[str, Any]] = []

        for row in rows:
            try:
                value = pickle.loads(row[1])
            except (
                pickle.PickleError,
                EOFError,
                TypeError,
                ValueError,
            ) as exc:
                raise RuntimeError(
                    "Unable to deserialize a stored "
                    "Mukti Mahal item."
                ) from exc

            result.append(
                (
                    str(row[0]),
                    value,
                )
            )

        return result

    # =====================================================
    # DELETE
    # =====================================================

    def pop(
        self,
        key: str,
        default: Any = None,
    ) -> Any:
        """Remove and return an item."""

        value = self.get(
            key,
            default,
        )

        if key in self:
            del self[key]

        return value

    # =====================================================
    # CLEAR
    # =====================================================

    def clear(self) -> None:
        """Remove all records from this collection."""

        self.database.execute(
            f"""
            DELETE FROM {self.table_name}
            """
        )

    # =====================================================
    # STATUS
    # =====================================================

    def count(self) -> int:
        """Return persistent record count."""

        return len(self)

    # =====================================================
    # INTERNAL
    # =====================================================

    @staticmethod
    def _safe_name(
        name: str,
    ) -> str:
        """
        Convert a logical store name into a safe SQLite
        identifier.
        """

        allowed = (
            "abcdefghijklmnopqrstuvwxyz"
            "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            "0123456789_"
        )

        result = "".join(
            char
            if char in allowed
            else "_"
            for char in name
        )

        if not result:
            raise ValueError(
                "Invalid persistent store name."
            )

        return result


__all__ = [
    "PersistentDict",
]
