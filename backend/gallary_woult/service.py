from __future__ import annotations

import json
import mimetypes
import sqlite3
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from backend.engines.storage.manager import StorageEngine
from backend.gallary_woult.object_store import GalleryWoultObjectStore


class GalleryWoultService:
    """
    GALLARY WOULT central own-storage service.

    Responsibilities:
    - folders
    - files
    - upload/save
    - listing
    - rename
    - move
    - copy
    - download
    - soft delete
    - restore
    - lock/unlock
    - versions
    - audit

    Binary data is handled by GalleryWoultObjectStore.
    Metadata remains in SQLite.
    """

    def __init__(
        self,
        db_path: str = "main_base_foundation.db",
        storage_root: Optional[str] = None,
    ):
        self.db_path = db_path
        self.object_store = GalleryWoultObjectStore(
            root=storage_root
        )

        # Central AI Store reference.
        self.ai_store = StorageEngine()

        self.initialize()

    # =========================================================
    # DATABASE
    # =========================================================

    def _connect(self):
        connection = sqlite3.connect(
            self.db_path,
            check_same_thread=False,
        )
        connection.row_factory = sqlite3.Row
        return connection

    @staticmethod
    def _now() -> str:
        return datetime.now(
            timezone.utc
        ).isoformat()

    def initialize(self):
        with self._connect() as db:
            db.execute(
                """
                CREATE TABLE IF NOT EXISTS gallery_woult_objects (
                    object_id TEXT PRIMARY KEY,
                    owner_id TEXT NOT NULL,
                    parent_id TEXT,
                    name TEXT NOT NULL,
                    object_type TEXT NOT NULL,
                    storage_key TEXT,
                    mime_type TEXT,
                    size INTEGER DEFAULT 0,
                    sha256 TEXT,
                    content_class TEXT DEFAULT 'GENERAL',
                    status TEXT DEFAULT 'ACTIVE',
                    locked INTEGER DEFAULT 0,
                    metadata TEXT DEFAULT '{}',
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
                """
            )

            db.execute(
                """
                CREATE INDEX IF NOT EXISTS
                idx_gallery_woult_owner
                ON gallery_woult_objects(owner_id)
                """
            )

            db.execute(
                """
                CREATE INDEX IF NOT EXISTS
                idx_gallery_woult_parent
                ON gallery_woult_objects(parent_id)
                """
            )

            db.execute(
                """
                CREATE TABLE IF NOT EXISTS gallery_woult_versions (
                    version_id TEXT PRIMARY KEY,
                    object_id TEXT NOT NULL,
                    storage_key TEXT NOT NULL,
                    size INTEGER DEFAULT 0,
                    sha256 TEXT,
                    created_by TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
                """
            )

            db.execute(
                """
                CREATE TABLE IF NOT EXISTS gallery_woult_audit (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    object_id TEXT,
                    actor_id TEXT NOT NULL,
                    action TEXT NOT NULL,
                    details TEXT DEFAULT '{}',
                    created_at TEXT NOT NULL
                )
                """
            )

            db.commit()

    # =========================================================
    # INTERNAL HELPERS
    # =========================================================

    def _require_actor(self, actor_id: str):
        if not actor_id or not actor_id.strip():
            raise PermissionError(
                "AUTHENTICATED_ACTOR_REQUIRED"
            )

    def _get_object(
        self,
        object_id: str,
    ):
        with self._connect() as db:
            return db.execute(
                """
                SELECT *
                FROM gallery_woult_objects
                WHERE object_id = ?
                """,
                (object_id,),
            ).fetchone()

    def _require_owner(
        self,
        object_id: str,
        actor_id: str,
    ):
        self._require_actor(actor_id)

        obj = self._get_object(object_id)

        if obj is None:
            raise FileNotFoundError(
                "OBJECT_NOT_FOUND"
            )

        if obj["owner_id"] != actor_id:
            raise PermissionError(
                "OBJECT_ACCESS_DENIED"
            )

        return obj

    def _audit(
        self,
        object_id: Optional[str],
        actor_id: str,
        action: str,
        details: Optional[dict] = None,
    ):
        self._require_actor(actor_id)

        with self._connect() as db:
            db.execute(
                """
                INSERT INTO gallery_woult_audit
                (
                    object_id,
                    actor_id,
                    action,
                    details,
                    created_at
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    object_id,
                    actor_id,
                    action,
                    json.dumps(
                        details or {},
                        ensure_ascii=False,
                    ),
                    self._now(),
                ),
            )
            db.commit()

    # =========================================================
    # FOLDERS
    # =========================================================

    def create_folder(
        self,
        actor_id: str,
        name: str,
        parent_id: Optional[str] = None,
    ) -> dict:

        self._require_actor(actor_id)

        name = name.strip()

        if not name:
            raise ValueError(
                "FOLDER_NAME_REQUIRED"
            )

        if parent_id:
            parent = self._require_owner(
                parent_id,
                actor_id,
            )

            if parent["object_type"] != "FOLDER":
                raise ValueError(
                    "PARENT_MUST_BE_FOLDER"
                )

            if parent["status"] != "ACTIVE":
                raise ValueError(
                    "PARENT_NOT_ACTIVE"
                )

        object_id = (
            f"GW-FOLDER-"
            f"{uuid.uuid4().hex.upper()}"
        )

        now = self._now()

        with self._connect() as db:
            db.execute(
                """
                INSERT INTO gallery_woult_objects
                (
                    object_id,
                    owner_id,
                    parent_id,
                    name,
                    object_type,
                    storage_key,
                    mime_type,
                    size,
                    sha256,
                    content_class,
                    status,
                    locked,
                    metadata,
                    created_at,
                    updated_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    object_id,
                    actor_id,
                    parent_id,
                    name,
                    "FOLDER",
                    None,
                    None,
                    0,
                    None,
                    "GENERAL",
                    "ACTIVE",
                    0,
                    "{}",
                    now,
                    now,
                ),
            )
            db.commit()

        self._audit(
            object_id,
            actor_id,
            "CREATE_FOLDER",
            {
                "name": name,
                "parent_id": parent_id,
            },
        )

        return self.get(
            object_id,
            actor_id,
        )

    # =========================================================
    # UPLOAD
    # =========================================================

    def upload(
        self,
        actor_id: str,
        filename: str,
        stream,
        parent_id: Optional[str] = None,
        mime_type: Optional[str] = None,
        content_class: str = "GENERAL",
        metadata: Optional[dict] = None,
    ) -> dict:

        self._require_actor(actor_id)

        if parent_id:
            parent = self._require_owner(
                parent_id,
                actor_id,
            )

            if parent["object_type"] != "FOLDER":
                raise ValueError(
                    "PARENT_MUST_BE_FOLDER"
                )

        filename = filename.strip()

        if not filename:
            raise ValueError(
                "FILENAME_REQUIRED"
            )

        object_id = (
            f"GW-FILE-"
            f"{uuid.uuid4().hex.upper()}"
        )

        storage_key = (
            self.object_store.make_storage_key(
                actor_id,
                object_id,
                filename,
            )
        )

        size, sha256 = (
            self.object_store.save_stream(
                stream,
                storage_key,
            )
        )

        detected_mime = (
            mime_type
            or mimetypes.guess_type(
                filename
            )[0]
            or "application/octet-stream"
        )

        now = self._now()

        with self._connect() as db:
            db.execute(
                """
                INSERT INTO gallery_woult_objects
                (
                    object_id,
                    owner_id,
                    parent_id,
                    name,
                    object_type,
                    storage_key,
                    mime_type,
                    size,
                    sha256,
                    content_class,
                    status,
                    locked,
                    metadata,
                    created_at,
                    updated_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    object_id,
                    actor_id,
                    parent_id,
                    filename,
                    "FILE",
                    storage_key,
                    detected_mime,
                    size,
                    sha256,
                    content_class,
                    "ACTIVE",
                    0,
                    json.dumps(
                        metadata or {},
                        ensure_ascii=False,
                    ),
                    now,
                    now,
                ),
            )
            db.commit()

        self._audit(
            object_id,
            actor_id,
            "UPLOAD",
            {
                "filename": filename,
                "size": size,
                "mime_type": detected_mime,
                "content_class": content_class,
            },
        )

        return self.get(
            object_id,
            actor_id,
        )

    # =========================================================
    # SAVE BYTES
    # =========================================================

    def save_bytes(
        self,
        actor_id: str,
        filename: str,
        data: bytes,
        parent_id: Optional[str] = None,
        mime_type: Optional[str] = None,
        content_class: str = "GENERAL",
        metadata: Optional[dict] = None,
    ) -> dict:

        from io import BytesIO

        return self.upload(
            actor_id=actor_id,
            filename=filename,
            stream=BytesIO(data),
            parent_id=parent_id,
            mime_type=mime_type,
            content_class=content_class,
            metadata=metadata,
        )

    # =========================================================
    # GET
    # =========================================================

    def get(
        self,
        object_id: str,
        actor_id: str,
    ) -> dict:

        obj = self._require_owner(
            object_id,
            actor_id,
        )

        return dict(obj)

    # =========================================================
    # LIST
    # =========================================================

    def list_children(
        self,
        actor_id: str,
        parent_id: Optional[str] = None,
        include_deleted: bool = False,
    ) -> list[dict]:

        self._require_actor(actor_id)

        if parent_id:
            self._require_owner(
                parent_id,
                actor_id,
            )

        query = """
            SELECT *
            FROM gallery_woult_objects
            WHERE owner_id = ?
              AND parent_id IS ?
        """

        params = [
            actor_id,
            parent_id,
        ]

        if not include_deleted:
            query += """
                AND status = 'ACTIVE'
            """

        query += """
            ORDER BY object_type ASC, name ASC
        """

        with self._connect() as db:
            rows = db.execute(
                query,
                params,
            ).fetchall()

        return [
            dict(row)
            for row in rows
        ]

    # =========================================================
    # RENAME
    # =========================================================

    def rename(
        self,
        object_id: str,
        actor_id: str,
        new_name: str,
    ) -> dict:

        obj = self._require_owner(
            object_id,
            actor_id,
        )

        if obj["locked"]:
            raise PermissionError(
                "OBJECT_LOCKED"
            )

        new_name = new_name.strip()

        if not new_name:
            raise ValueError(
                "NAME_REQUIRED"
            )

        now = self._now()

        with self._connect() as db:
            db.execute(
                """
                UPDATE gallery_woult_objects
                SET name = ?,
                    updated_at = ?
                WHERE object_id = ?
                """,
                (
                    new_name,
                    now,
                    object_id,
                ),
            )
            db.commit()

        self._audit(
            object_id,
            actor_id,
            "RENAME",
            {
                "old_name": obj["name"],
                "new_name": new_name,
            },
        )

        return self.get(
            object_id,
            actor_id,
        )

    # =========================================================
    # MOVE
    # =========================================================

    def move(
        self,
        object_id: str,
        actor_id: str,
        parent_id: Optional[str],
    ) -> dict:

        obj = self._require_owner(
            object_id,
            actor_id,
        )

        if obj["locked"]:
            raise PermissionError(
                "OBJECT_LOCKED"
            )

        if parent_id == object_id:
            raise ValueError(
                "OBJECT_CANNOT_BE_OWN_PARENT"
            )

        if parent_id:
            parent = self._require_owner(
                parent_id,
                actor_id,
            )

            if parent["object_type"] != "FOLDER":
                raise ValueError(
                    "TARGET_MUST_BE_FOLDER"
                )

            if parent["status"] != "ACTIVE":
                raise ValueError(
                    "TARGET_FOLDER_NOT_ACTIVE"
                )

        now = self._now()

        with self._connect() as db:
            db.execute(
                """
                UPDATE gallery_woult_objects
                SET parent_id = ?,
                    updated_at = ?
                WHERE object_id = ?
                """,
                (
                    parent_id,
                    now,
                    object_id,
                ),
            )
            db.commit()

        self._audit(
            object_id,
            actor_id,
            "MOVE",
            {
                "old_parent_id": obj["parent_id"],
                "new_parent_id": parent_id,
            },
        )

        return self.get(
            object_id,
            actor_id,
        )

    # =========================================================
    # COPY
    # =========================================================

    def copy(
        self,
        object_id: str,
        actor_id: str,
        parent_id: Optional[str] = None,
        new_name: Optional[str] = None,
    ) -> dict:

        obj = self._require_owner(
            object_id,
            actor_id,
        )

        if obj["status"] != "ACTIVE":
            raise ValueError(
                "OBJECT_NOT_ACTIVE"
            )

        if parent_id:
            parent = self._require_owner(
                parent_id,
                actor_id,
            )

            if parent["object_type"] != "FOLDER":
                raise ValueError(
                    "TARGET_MUST_BE_FOLDER"
                )

        if obj["object_type"] == "FOLDER":
            return self._copy_folder(
                obj,
                actor_id,
                parent_id,
                new_name,
            )

        new_object_id = (
            f"GW-FILE-"
            f"{uuid.uuid4().hex.upper()}"
        )

        filename = (
            new_name
            or f"Copy of {obj['name']}"
        )

        new_storage_key = (
            self.object_store.make_storage_key(
                actor_id,
                new_object_id,
                filename,
            )
        )

        size, sha256 = (
            self.object_store.copy(
                obj["storage_key"],
                new_storage_key,
            )
        )

        now = self._now()

        with self._connect() as db:
            db.execute(
                """
                INSERT INTO gallery_woult_objects
                (
                    object_id,
                    owner_id,
                    parent_id,
                    name,
                    object_type,
                    storage_key,
                    mime_type,
                    size,
                    sha256,
                    content_class,
                    status,
                    locked,
                    metadata,
                    created_at,
                    updated_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    new_object_id,
                    actor_id,
                    parent_id,
                    filename,
                    "FILE",
                    new_storage_key,
                    obj["mime_type"],
                    size,
                    sha256,
                    obj["content_class"],
                    "ACTIVE",
                    0,
                    obj["metadata"],
                    now,
                    now,
                ),
            )
            db.commit()

        self._audit(
            new_object_id,
            actor_id,
            "COPY",
            {
                "source_object_id": object_id,
            },
        )

        return self.get(
            new_object_id,
            actor_id,
        )

    def _copy_folder(
        self,
        source,
        actor_id: str,
        parent_id: Optional[str],
        new_name: Optional[str],
    ) -> dict:

        folder = self.create_folder(
            actor_id,
            new_name or f"Copy of {source['name']}",
            parent_id,
        )

        children = self.list_children(
            actor_id,
            source["object_id"],
        )

        for child in children:
            self.copy(
                child["object_id"],
                actor_id,
                folder["object_id"],
            )

        return self.get(
            folder["object_id"],
            actor_id,
        )

    # =========================================================
    # DOWNLOAD
    # =========================================================

    def get_download_path(
        self,
        object_id: str,
        actor_id: str,
    ) -> Path:

        obj = self._require_owner(
            object_id,
            actor_id,
        )

        if obj["object_type"] != "FILE":
            raise ValueError(
                "OBJECT_IS_NOT_FILE"
            )

        if obj["status"] != "ACTIVE":
            raise ValueError(
                "OBJECT_NOT_ACTIVE"
            )

        if not self.object_store.exists(
            obj["storage_key"]
        ):
            raise FileNotFoundError(
                "STORAGE_OBJECT_NOT_FOUND"
            )

        self._audit(
            object_id,
            actor_id,
            "DOWNLOAD",
        )

        return self.object_store._path_for(
            obj["storage_key"]
        )

    # =========================================================
    # DELETE
    # =========================================================

    def delete(
        self,
        object_id: str,
        actor_id: str,
    ) -> dict:

        obj = self._require_owner(
            object_id,
            actor_id,
        )

        if obj["locked"]:
            raise PermissionError(
                "OBJECT_LOCKED"
            )

        now = self._now()

        with self._connect() as db:
            db.execute(
                """
                UPDATE gallery_woult_objects
                SET status = 'DELETED',
                    updated_at = ?
                WHERE object_id = ?
                """,
                (
                    now,
                    object_id,
                ),
            )
            db.commit()

        self._audit(
            object_id,
            actor_id,
            "DELETE",
        )

        return self.get(
            object_id,
            actor_id,
        )

    # =========================================================
    # RESTORE
    # =========================================================

    def restore(
        self,
        object_id: str,
        actor_id: str,
    ) -> dict:

        obj = self._require_owner(
            object_id,
            actor_id,
        )

        if obj["status"] != "DELETED":
            raise ValueError(
                "OBJECT_NOT_DELETED"
            )

        now = self._now()

        with self._connect() as db:
            db.execute(
                """
                UPDATE gallery_woult_objects
                SET status = 'ACTIVE',
                    updated_at = ?
                WHERE object_id = ?
                """,
                (
                    now,
                    object_id,
                ),
            )
            db.commit()

        self._audit(
            object_id,
            actor_id,
            "RESTORE",
        )

        return self.get(
            object_id,
            actor_id,
        )

    # =========================================================
    # LOCK / UNLOCK
    # =========================================================

    def lock(
        self,
        object_id: str,
        actor_id: str,
        locked: bool = True,
    ) -> dict:

        obj = self._require_owner(
            object_id,
            actor_id,
        )

        now = self._now()

        with self._connect() as db:
            db.execute(
                """
                UPDATE gallery_woult_objects
                SET locked = ?,
                    updated_at = ?
                WHERE object_id = ?
                """,
                (
                    1 if locked else 0,
                    now,
                    object_id,
                ),
            )
            db.commit()

        self._audit(
            object_id,
            actor_id,
            "LOCK" if locked else "UNLOCK",
        )

        return self.get(
            object_id,
            actor_id,
        )

    # =========================================================
    # VERSION
    # =========================================================

    def add_version(
        self,
        object_id: str,
        actor_id: str,
        stream,
    ) -> dict:

        obj = self._require_owner(
            object_id,
            actor_id,
        )

        if obj["object_type"] != "FILE":
            raise ValueError(
                "VERSIONS_REQUIRE_FILE"
            )

        if obj["locked"]:
            raise PermissionError(
                "OBJECT_LOCKED"
            )

        version_id = (
            f"GW-VERSION-"
            f"{uuid.uuid4().hex.upper()}"
        )

        storage_key = (
            self.object_store.make_storage_key(
                actor_id,
                f"version-{version_id}",
                obj["name"],
            )
        )

        size, sha256 = (
            self.object_store.save_stream(
                stream,
                storage_key,
            )
        )

        now = self._now()

        with self._connect() as db:
            db.execute(
                """
                INSERT INTO gallery_woult_versions
                (
                    version_id,
                    object_id,
                    storage_key,
                    size,
                    sha256,
                    created_by,
                    created_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    version_id,
                    object_id,
                    storage_key,
                    size,
                    sha256,
                    actor_id,
                    now,
                ),
            )
            db.commit()

        self._audit(
            object_id,
            actor_id,
            "CREATE_VERSION",
            {
                "version_id": version_id,
                "size": size,
            },
        )

        return {
            "version_id": version_id,
            "object_id": object_id,
            "storage_key": storage_key,
            "size": size,
            "sha256": sha256,
            "created_by": actor_id,
            "created_at": now,
        }

    def versions(
        self,
        object_id: str,
        actor_id: str,
    ) -> list[dict]:

        self._require_owner(
            object_id,
            actor_id,
        )

        with self._connect() as db:
            rows = db.execute(
                """
                SELECT *
                FROM gallery_woult_versions
                WHERE object_id = ?
                ORDER BY created_at DESC
                """,
                (object_id,),
            ).fetchall()

        return [
            dict(row)
            for row in rows
        ]

    # =========================================================
    # STATUS
    # =========================================================

    def status(self) -> dict:
        with self._connect() as db:
            objects = db.execute(
                """
                SELECT COUNT(*)
                FROM gallery_woult_objects
                """
            ).fetchone()[0]

            files = db.execute(
                """
                SELECT COUNT(*)
                FROM gallery_woult_objects
                WHERE object_type = 'FILE'
                """
            ).fetchone()[0]

            folders = db.execute(
                """
                SELECT COUNT(*)
                FROM gallery_woult_objects
                WHERE object_type = 'FOLDER'
                """
            ).fetchone()[0]

        return {
            "system": "GALLARY WOULT",
            "status": "READY",
            "storage": "OWN_STORAGE",
            "objects": objects,
            "files": files,
            "folders": folders,
            "ai_store": "CENTRAL",
        }
