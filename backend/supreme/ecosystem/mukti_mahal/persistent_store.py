"""
MAIN BASE FOUNDATION

SUPREME — Mukti Mahal Persistent Store

Database-backed dictionary-compatible storage for
the Mukti Mahal application service.
"""

from __future__ import annotations

import pickle
import sqlite3
from typing import Any, List, Optional

from backend.database.service import DatabaseService


class PersistentDict:
    """Persistent dictionary backed by MAIN BASE FOUNDATION DB."""

    def __init__(
        self,
        name: str,
        database: Optional[DatabaseService] = None,
    ) -> None:
        if not name:
            raise ValueError(
                "Persistent store name is required."
            )

        self.name = name
        self.database = (
            database or DatabaseService()
        )

        self.table_name = (
            "mukti_mahal_store_"
            + self._safe_name(name)
        )

        self._initialize()

    def _initialize(self) -> None:
        self.database.initialize()

        self.database.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {self.table_name} (
                item_key TEXT PRIMARY KEY,
                item_value BLOB NOT NULL
            )
            """
        )

    def __contains__(self, key: object) -> bool:
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

        return int(row[0]) if row else 0

    def __getitem__(self, key: str) -> Any:
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

        data = sqlite3.Binary(
            pickle.dumps(
                value,
                protocol=pickle.HIGHEST_PROTOCOL,
            )
        )

        self.database.execute(
            f"""
            INSERT OR REPLACE INTO {self.table_name}
            (
                item_key,
                item_value
            )
            VALUES (?, ?)
            """,
            (
                str(key),
                data,
            ),
        )

    def __delitem__(self, key: str) -> None:
        affected = self.database.execute(
            f"""
            DELETE FROM {self.table_name}
            WHERE item_key = ?
            """,
            (str(key),),
        )

        if affected == 0:
            raise KeyError(key)

    def get(
        self,
        key: str,
        default: Any = None,
    ) -> Any:
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
                "Unable to deserialize Mukti Mahal data."
            ) from exc

    def values(self) -> List[Any]:
        rows = self.database.fetchall(
            f"""
            SELECT item_value
            FROM {self.table_name}
            ORDER BY item_key ASC
            """
        )

        result: List[Any] = []

        for row in rows:
            result.append(
                pickle.loads(row[0])
            )

        return result

    def items(self) -> List[tuple[str, Any]]:
        rows = self.database.fetchall(
            f"""
            SELECT item_key, item_value
            FROM {self.table_name}
            ORDER BY item_key ASC
            """
        )

        return [
            (
                str(row[0]),
                pickle.loads(row[1]),
            )
            for row in rows
        ]

    def pop(
        self,
        key: str,
        default: Any = None,
    ) -> Any:
        value = self.get(
            key,
            default,
        )

        if key in self:
            del self[key]

        return value

    def clear(self) -> None:
        self.database.execute(
            f"""
            DELETE FROM {self.table_name}
            """
        )

    @staticmethod
    def _safe_name(name: str) -> str:
        allowed = (
            "abcdefghijklmnopqrstuvwxyz"
            "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            "0123456789_"
        )

        result = "".join(
            char if char in allowed else "_"
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
