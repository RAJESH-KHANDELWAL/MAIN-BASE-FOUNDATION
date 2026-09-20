from __future__ import annotations

import hashlib
import os
import re
import shutil
from io import BytesIO
from pathlib import Path
from typing import BinaryIO


class GalleryWoultObjectStore:
    """
    GALLARY WOULT native object storage.

    Binary files are stored outside SQLite/Git.
    SQLite stores metadata, ownership, permissions,
    versions and audit information.
    """

    def __init__(self, root: str | None = None):
        configured_root = root or os.getenv(
            "GALLERY_WOULT_STORAGE_ROOT",
            "data/gallery_woult",
        )

        self.root = Path(configured_root).resolve()
        self.root.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def _safe_name(name: str) -> str:
        value = Path(name or "file").name
        value = re.sub(
            r"[^A-Za-z0-9._ -]",
            "_",
            value,
        ).strip()

        return value or "file"

    @staticmethod
    def _safe_component(value: str) -> str:
        value = re.sub(
            r"[^A-Za-z0-9._-]",
            "_",
            str(value),
        )

        return value.strip("._") or "unknown"

    def _path_for(self, storage_key: str) -> Path:
        candidate = (
            self.root / storage_key
        ).resolve()

        if (
            candidate != self.root
            and self.root not in candidate.parents
        ):
            raise ValueError(
                "INVALID_STORAGE_KEY"
            )

        return candidate

    def make_storage_key(
        self,
        owner_id: str,
        object_id: str,
        filename: str,
    ) -> str:
        owner = self._safe_component(owner_id)
        object_id = self._safe_component(object_id)
        filename = self._safe_name(filename)

        return (
            f"{owner}/"
            f"{object_id}/"
            f"{filename}"
        )

    def save_stream(
        self,
        stream: BinaryIO,
        storage_key: str,
    ) -> tuple[int, str]:

        target = self._path_for(
            storage_key
        )

        target.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        sha256 = hashlib.sha256()
        size = 0

        with target.open("wb") as output:
            while True:
                chunk = stream.read(
                    1024 * 1024
                )

                if not chunk:
                    break

                output.write(chunk)
                sha256.update(chunk)
                size += len(chunk)

        return (
            size,
            sha256.hexdigest(),
        )

    def save_bytes(
        self,
        data: bytes,
        storage_key: str,
    ) -> tuple[int, str]:

        return self.save_stream(
            BytesIO(data),
            storage_key,
        )

    def open(
        self,
        storage_key: str,
    ) -> BinaryIO:

        path = self._path_for(
            storage_key
        )

        if not path.is_file():
            raise FileNotFoundError(
                storage_key
            )

        return path.open("rb")

    def exists(
        self,
        storage_key: str,
    ) -> bool:

        return self._path_for(
            storage_key
        ).is_file()

    def copy(
        self,
        source_storage_key: str,
        target_storage_key: str,
    ) -> tuple[int, str]:

        source = self._path_for(
            source_storage_key
        )

        if not source.is_file():
            raise FileNotFoundError(
                source_storage_key
            )

        target = self._path_for(
            target_storage_key
        )

        target.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        shutil.copy2(
            source,
            target,
        )

        sha256 = hashlib.sha256()
        size = 0

        with target.open("rb") as stream:
            while True:
                chunk = stream.read(
                    1024 * 1024
                )

                if not chunk:
                    break

                sha256.update(chunk)
                size += len(chunk)

        return (
            size,
            sha256.hexdigest(),
        )

    def delete(
        self,
        storage_key: str,
    ) -> bool:

        path = self._path_for(
            storage_key
        )

        if not path.is_file():
            return False

        path.unlink()

        return True
