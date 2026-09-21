from __future__ import annotations

from typing import Optional

from fastapi import (
    APIRouter,
    Depends,
    File,
    Header,
    HTTPException,
    UploadFile,
)
from fastapi.responses import FileResponse
from pydantic import BaseModel

from backend.auth.service import AuthenticationService
from backend.gallary_woult.service import GalleryWoultService

router = APIRouter(
    prefix="/gallary-woult",
    tags=["GALLARY WOULT"],
)

authentication_service = AuthenticationService()
gallary_woult_service = GalleryWoultService()


def require_actor(
    authorization: Optional[str] = Header(default=None),
) -> str:

    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="AUTHORIZATION_REQUIRED",
        )

    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="INVALID_AUTHORIZATION_HEADER",
        )

    token = authorization[
        len("Bearer "):
    ].strip()

    if not token:
        raise HTTPException(
            status_code=401,
            detail="EMPTY_AUTH_TOKEN",
        )

    result = (
        authentication_service
        .validate_token(token)
    )

    if not result.get("authenticated"):
        raise HTTPException(
            status_code=401,
            detail=result.get(
                "message",
                "INVALID_AUTHENTICATION_TOKEN",
            ),
        )

    username = result.get("username")

    if not username:
        raise HTTPException(
            status_code=401,
            detail="AUTHENTICATED_USERNAME_NOT_FOUND",
        )

    return username


class FolderRequest(BaseModel):
    name: str
    parent_id: Optional[str] = None


class RenameRequest(BaseModel):
    name: str


class MoveRequest(BaseModel):
    parent_id: Optional[str] = None


class CopyRequest(BaseModel):
    parent_id: Optional[str] = None


class LockRequest(BaseModel):
    locked: bool = True


@router.get("/status")
def status(
    actor_id: str = Depends(require_actor),
):
    return gallary_woult_service.status()


@router.post("/folders")
def create_folder(
    request: FolderRequest,
    actor_id: str = Depends(require_actor),
):

    try:

        return gallary_woult_service.create_folder(
            owner_id=actor_id,
            name=request.name,
            parent_id=request.parent_id,
        )

    except PermissionError as exc:

        raise HTTPException(
            status_code=403,
            detail=str(exc),
        )

    except ValueError as exc:

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )


@router.get("/files")
def list_files(
    parent_id: Optional[str] = None,
    include_trashed: bool = False,
    actor_id: str = Depends(require_actor),
):

    return gallary_woult_service.list_children(
        owner_id=actor_id,
        parent_id=parent_id,
        include_trashed=include_trashed,
    )


@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    parent_id: Optional[str] = None,
    content_class: str = "GENERAL",
    actor_id: str = Depends(require_actor),
):

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="FILE_NAME_REQUIRED",
        )

    try:

        return gallary_woult_service.upload(
            owner_id=actor_id,
            name=file.filename,
            stream=file.file,
            mime_type=file.content_type,
            parent_id=parent_id,
            content_class=content_class,
        )

    except PermissionError as exc:

        raise HTTPException(
            status_code=403,
            detail=str(exc),
        )

    except ValueError as exc:

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )


@router.patch("/{object_id}/rename")
def rename(
    object_id: str,
    request: RenameRequest,
    actor_id: str = Depends(require_actor),
):

    try:

        return gallary_woult_service.rename(
            owner_id=actor_id,
            object_id=object_id,
            name=request.name,
        )

    except FileNotFoundError as exc:

        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )

    except PermissionError as exc:

        raise HTTPException(
            status_code=403,
            detail=str(exc),
        )

    except ValueError as exc:

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )


@router.patch("/{object_id}/move")
def move(
    object_id: str,
    request: MoveRequest,
    actor_id: str = Depends(require_actor),
):

    try:

        return gallary_woult_service.move(
            owner_id=actor_id,
            object_id=object_id,
            parent_id=request.parent_id,
        )

    except FileNotFoundError as exc:

        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )

    except PermissionError as exc:

        raise HTTPException(
            status_code=403,
            detail=str(exc),
        )

    except ValueError as exc:

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )


@router.post("/{object_id}/copy")
def copy_object(
    object_id: str,
    request: CopyRequest,
    actor_id: str = Depends(require_actor),
):

    try:

        return gallary_woult_service.copy(
            owner_id=actor_id,
            object_id=object_id,
            parent_id=request.parent_id,
        )

    except FileNotFoundError as exc:

        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )

    except PermissionError as exc:

        raise HTTPException(
            status_code=403,
            detail=str(exc),
        )

    except ValueError as exc:

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )


@router.get("/{object_id}/download")
def download(
    object_id: str,
    actor_id: str = Depends(require_actor),
):

    try:

        path = (
            gallary_woult_service
            .download_path(
                owner_id=actor_id,
                object_id=object_id,
            )
        )

        return FileResponse(
            path=path,
            filename=None,
        )

    except FileNotFoundError as exc:

        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )

    except PermissionError as exc:

        raise HTTPException(
            status_code=403,
            detail=str(exc),
        )

    except ValueError as exc:

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )


@router.delete("/{object_id}")
def trash(
    object_id: str,
    actor_id: str = Depends(require_actor),
):

    try:

        return gallary_woult_service.trash(
            owner_id=actor_id,
            object_id=object_id,
        )

    except FileNotFoundError as exc:

        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )

    except PermissionError as exc:

        raise HTTPException(
            status_code=403,
            detail=str(exc),
        )


@router.post("/{object_id}/restore")
def restore(
    object_id: str,
    actor_id: str = Depends(require_actor),
):

    try:

        return gallary_woult_service.restore(
            owner_id=actor_id,
            object_id=object_id,
        )

    except FileNotFoundError as exc:

        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )


@router.post("/{object_id}/lock")
def lock(
    object_id: str,
    request: LockRequest,
    actor_id: str = Depends(require_actor),
):

    try:

        return gallary_woult_service.lock(
            owner_id=actor_id,
            object_id=object_id,
            locked=request.locked,
        )

    except FileNotFoundError as exc:

        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )
