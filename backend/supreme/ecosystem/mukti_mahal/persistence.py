"""
MAIN BASE FOUNDATION

SUPREME — Mukti Mahal Persistence Layer

Persistent database foundation for the Mukti Mahal ecosystem.

This layer stores Mukti Mahal operational records in the
central MAIN BASE FOUNDATION database.

No passwords, OTPs, authentication secrets, raw identity
documents, or payment credentials are stored here.
"""

from __future__ import annotations

import json
from typing import Any, Dict, List, Optional

from backend.database.service import DatabaseService


class MuktiMahalPersistence:
    """Persistent storage foundation for Mukti Mahal."""

    def __init__(
        self,
        database: Optional[DatabaseService] = None,
    ) -> None:
        self.database = database or DatabaseService()
        self._initialized = False

    # =====================================================
    # INITIALIZATION
    # =====================================================

    def initialize(self) -> dict:
        """Create the Mukti Mahal persistence tables."""

        self.database.initialize()

        self.database.execute(
            """
            CREATE TABLE IF NOT EXISTS mukti_mahal_entities (
                entity_id TEXT PRIMARY KEY,
                entity_type TEXT NOT NULL,
                name TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'ACTIVE',
                payload TEXT NOT NULL DEFAULT '{}',
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )

        self.database.execute(
            """
            CREATE INDEX IF NOT EXISTS
            idx_mukti_mahal_entities_type
            ON mukti_mahal_entities(entity_type)
            """
        )

        self.database.execute(
            """
            CREATE INDEX IF NOT EXISTS
            idx_mukti_mahal_entities_status
            ON mukti_mahal_entities(status)
            """
        )

        self.database.execute(
            """
            CREATE TABLE IF NOT EXISTS mukti_mahal_relationships (
                relationship_id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_id TEXT NOT NULL,
                relationship_type TEXT NOT NULL,
                target_id TEXT NOT NULL,
                metadata TEXT NOT NULL DEFAULT '{}',
                created_at TEXT NOT NULL,
                UNIQUE(
                    source_id,
                    relationship_type,
                    target_id
                )
            )
            """
        )

        self.database.execute(
            """
            CREATE INDEX IF NOT EXISTS
            idx_mukti_mahal_relationship_source
            ON mukti_mahal_relationships(source_id)
            """
        )

        self.database.execute(
            """
            CREATE INDEX IF NOT EXISTS
            idx_mukti_mahal_relationship_target
            ON mukti_mahal_relationships(target_id)
            """
        )

        self._initialized = True

        return self.status()

    # =====================================================
    # STATUS
    # =====================================================

    def status(self) -> dict:
        """Return persistence status."""

        return {
            "service": "MUKTI_MAHAL_PERSISTENCE",
            "initialized": self._initialized,
            "storage": "MAIN_BASE_FOUNDATION_DATABASE",
        }

    # =====================================================
    # ENTITY
    # =====================================================

    def save_entity(
        self,
        entity_id: str,
        entity_type: str,
        name: str,
        payload: Optional[Dict[str, Any]] = None,
        status: str = "ACTIVE",
        created_at: str = "",
        updated_at: str = "",
    ) -> Dict[str, Any]:
        """Create or update a persistent Mukti Mahal entity."""

        if not self._initialized:
            self.initialize()

        if not entity_id:
            raise ValueError("entity_id is required.")

        if not entity_type:
            raise ValueError("entity_type is required.")

        if not name:
            raise ValueError("name is required.")

        payload_data = payload or {}

        existing = self.get_entity(entity_id)

        if existing is None:
            if not created_at:
                from .model import utc_now

                created_at = utc_now()

            if not updated_at:
                updated_at = created_at

            self.database.execute(
                """
                INSERT INTO mukti_mahal_entities (
                    entity_id,
                    entity_type,
                    name,
                    status,
                    payload,
                    created_at,
                    updated_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    entity_id,
                    entity_type,
                    name,
                    status,
                    json.dumps(
                        payload_data,
                        ensure_ascii=False,
                        default=str,
                    ),
                    created_at,
                    updated_at,
                ),
            )
        else:
            if not updated_at:
                from .model import utc_now

                updated_at = utc_now()

            self.database.execute(
                """
                UPDATE mukti_mahal_entities
                SET
                    entity_type = ?,
                    name = ?,
                    status = ?,
                    payload = ?,
                    updated_at = ?
                WHERE entity_id = ?
                """,
                (
                    entity_type,
                    name,
                    status,
                    json.dumps(
                        payload_data,
                        ensure_ascii=False,
                        default=str,
                    ),
                    updated_at,
                    entity_id,
                ),
            )

        return self.get_entity(entity_id)

    def get_entity(
        self,
        entity_id: str,
    ) -> Optional[Dict[str, Any]]:
        """Get one persistent entity."""

        if not self._initialized:
            self.initialize()

        row = self.database.fetchone(
            """
            SELECT
                entity_id,
                entity_type,
                name,
                status,
                payload,
                created_at,
                updated_at
            FROM mukti_mahal_entities
            WHERE entity_id = ?
            """,
            (entity_id,),
        )

        if row is None:
            return None

        return self._row_to_entity(row)

    def list_entities(
        self,
        entity_type: Optional[str] = None,
        status: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """List persistent entities."""

        if not self._initialized:
            self.initialize()

        conditions: List[str] = []
        values: List[Any] = []

        if entity_type:
            conditions.append("entity_type = ?")
            values.append(entity_type)

        if status:
            conditions.append("status = ?")
            values.append(status)

        query = """
            SELECT
                entity_id,
                entity_type,
                name,
                status,
                payload,
                created_at,
                updated_at
            FROM mukti_mahal_entities
        """

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        query += " ORDER BY created_at ASC"

        rows = self.database.fetchall(
            query,
            tuple(values),
        )

        return [
            self._row_to_entity(row)
            for row in rows
        ]

    def delete_entity(
        self,
        entity_id: str,
    ) -> bool:
        """Delete a persistent entity."""

        if not self._initialized:
            self.initialize()

        self.database.execute(
            """
            DELETE FROM mukti_mahal_entities
            WHERE entity_id = ?
            """,
            (entity_id,),
        )

        return self.get_entity(entity_id) is None

    # =====================================================
    # RELATIONSHIPS
    # =====================================================

    def create_relationship(
        self,
        source_id: str,
        relationship_type: str,
        target_id: str,
        metadata: Optional[Dict[str, Any]] = None,
        created_at: str = "",
    ) -> Dict[str, Any]:
        """Create a relationship between two entities."""

        if not self._initialized:
            self.initialize()

        if not source_id:
            raise ValueError("source_id is required.")

        if not relationship_type:
            raise ValueError(
                "relationship_type is required."
            )

        if not target_id:
            raise ValueError("target_id is required.")

        if not created_at:
            from .model import utc_now

            created_at = utc_now()

        metadata_data = metadata or {}

        self.database.execute(
            """
            INSERT OR IGNORE INTO
            mukti_mahal_relationships (
                source_id,
                relationship_type,
                target_id,
                metadata,
                created_at
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                source_id,
                relationship_type,
                target_id,
                json.dumps(
                    metadata_data,
                    ensure_ascii=False,
                    default=str,
                ),
                created_at,
            ),
        )

        row = self.database.fetchone(
            """
            SELECT
                relationship_id,
                source_id,
                relationship_type,
                target_id,
                metadata,
                created_at
            FROM mukti_mahal_relationships
            WHERE
                source_id = ?
                AND relationship_type = ?
                AND target_id = ?
            """,
            (
                source_id,
                relationship_type,
                target_id,
            ),
        )

        return self._row_to_relationship(row)

    def list_relationships(
        self,
        source_id: Optional[str] = None,
        target_id: Optional[str] = None,
        relationship_type: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """List entity relationships."""

        if not self._initialized:
            self.initialize()

        conditions: List[str] = []
        values: List[Any] = []

        if source_id:
            conditions.append("source_id = ?")
            values.append(source_id)

        if target_id:
            conditions.append("target_id = ?")
            values.append(target_id)

        if relationship_type:
            conditions.append("relationship_type = ?")
            values.append(relationship_type)

        query = """
            SELECT
                relationship_id,
                source_id,
                relationship_type,
                target_id,
                metadata,
                created_at
            FROM mukti_mahal_relationships
        """

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        query += " ORDER BY relationship_id ASC"

        rows = self.database.fetchall(
            query,
            tuple(values),
        )

        return [
            self._row_to_relationship(row)
            for row in rows
        ]

    # =====================================================
    # INTERNAL CONVERSION
    # =====================================================

    @staticmethod
    def _row_to_entity(
        row: Any,
    ) -> Dict[str, Any]:
        """Convert a database row to a safe entity dict."""

        if row is None:
            return {}

        payload = row[4] or "{}"

        try:
            payload_data = json.loads(payload)
        except (TypeError, ValueError):
            payload_data = {}

        return {
            "entity_id": row[0],
            "entity_type": row[1],
            "name": row[2],
            "status": row[3],
            "payload": payload_data,
            "created_at": row[5],
            "updated_at": row[6],
        }

    @staticmethod
    def _row_to_relationship(
        row: Any,
    ) -> Dict[str, Any]:
        """Convert a relationship row to a safe dict."""

        if row is None:
            return {}

        metadata = row[4] or "{}"

        try:
            metadata_data = json.loads(metadata)
        except (TypeError, ValueError):
            metadata_data = {}

        return {
            "relationship_id": row[0],
            "source_id": row[1],
            "relationship_type": row[2],
            "target_id": row[3],
            "metadata": metadata_data,
            "created_at": row[5],
        }
