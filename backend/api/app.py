from pathlib import Path
from typing import Dict, Optional

from fastapi import FastAPI, Header, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from backend.api.users import router as users_router
from backend.api.businesses import router as businesses_router
from backend.api.projects import router as projects_router
from backend.api.supreme import router as supreme_router
from backend.api.identity import router as identity_router
from backend.api.auth import router as auth_router
from backend.api.roles import router as roles_router
from backend.api.matching import router as matching_router
from backend.api.profiles import router as profiles_router

from backend.api.connectivity import ConnectivityAPI
from backend.api.cloud import CloudAPI
from backend.api.integrations import IntegrationsAPI
from backend.api.integration_connections import (
    IntegrationConnectionsAPI,
)

from backend.api.ecosystem import EcosystemAPI
from backend.api.storage import StorageAPI
from backend.api.opportunities import router as opportunities_router
from backend.api.dns import router as dns_router
from backend.api.infrastructure import router as infrastructure_router
from backend.api.mukti_mahal import router as mukti_mahal_router
from backend.api.mukti_mahal_media import (
    router as mukti_mahal_media_router
)
from backend.api.mukti_mahal_creation import (
    router as mukti_mahal_creation_router
)


# =========================================================
# APPLICATION
# =========================================================

app = FastAPI(
    title="MAIN BASE FOUNDATION API",
    version="1.0.0",
)


# =========================================================
# CORE APIS
# =========================================================

connectivity_api = ConnectivityAPI()

cloud_api = CloudAPI()

integrations_api = IntegrationsAPI()

integration_connections_api = (
    IntegrationConnectionsAPI()
)

ecosystem_api = EcosystemAPI()

storage_api = StorageAPI()


# =========================================================
# ROUTERS
# =========================================================

app.include_router(users_router)
app.include_router(businesses_router)
app.include_router(projects_router)
app.include_router(supreme_router)
app.include_router(identity_router)
app.include_router(auth_router)
app.include_router(roles_router)
app.include_router(opportunities_router)
app.include_router(matching_router)
app.include_router(profiles_router)
app.include_router(dns_router)
app.include_router(infrastructure_router)
app.include_router(mukti_mahal_router)
app.include_router(mukti_mahal_media_router)
app.include_router(
    mukti_mahal_creation_router
)


# =========================================================
# CONNECTIVITY
# =========================================================

@app.get("/connectivity")
def connectivity_status():
    """Return unified connectivity status."""
    return connectivity_api.status()


@app.get("/connectivity/health")
def connectivity_health():
    """Return connectivity health."""
    return connectivity_api.health()


@app.get("/connectivity/networks")
def connectivity_networks():
    """Return safely discoverable visible networks."""
    return connectivity_api.networks()


@app.get("/connectivity/servers")
def connectivity_servers():
    """Return configured server health information."""
    return connectivity_api.servers()


@app.get("/connectivity/satellite")
def connectivity_satellite():
    """Return satellite connectivity status."""
    return connectivity_api.satellite()


@app.post("/connectivity/satellite/ingest")
def connectivity_satellite_ingest(
    data: Dict[str, object],
):
    """Ingest approved satellite telemetry."""
    return connectivity_api.ingest_satellite(
        data
    )


@app.post("/connectivity/start")
def connectivity_start():
    """Start the connectivity engine."""
    return connectivity_api.start()


@app.post("/connectivity/stop")
def connectivity_stop():
    """Stop the connectivity engine."""
    return connectivity_api.stop()


@app.post("/connectivity/restart")
def connectivity_restart():
    """Restart the connectivity engine."""
    return connectivity_api.restart()


# =========================================================
# CLOUD
# =========================================================

@app.get("/cloud")
def cloud_status():
    """Return unified cloud status."""
    return cloud_api.status()


@app.get("/cloud/health")
def cloud_health():
    """Return cloud infrastructure health."""
    return cloud_api.health()


@app.get("/cloud/security")
def cloud_security():
    """Return cloud integration security."""
    return cloud_api.security()


@app.get("/cloud/providers")
def cloud_providers():
    """Return registered cloud providers."""
    return cloud_api.providers()


@app.get("/cloud/providers/{name}")
def cloud_provider(
    name: str,
):
    """Return one registered cloud provider."""
    return cloud_api.provider(name)


@app.get("/cloud/summary")
def cloud_summary():
    """Return compact cloud summary."""
    return cloud_api.summary()


@app.get("/cloud/services/{provider}")
def cloud_services(
    provider: str,
):
    """Return services registered for a provider."""
    return cloud_api.services(provider)


@app.post("/cloud/configure")
def cloud_configure(
    provider: str,
    region: str | None = None,
):
    """Register cloud provider configuration."""
    return cloud_api.configure(
        provider=provider,
        region=region,
    )


@app.post("/cloud/authorize")
def cloud_authorize(
    provider: str,
):
    """Record authorization from an approved flow."""
    return cloud_api.authorize(
        provider=provider,
    )


@app.post("/cloud/telemetry")
def cloud_telemetry(
    provider: str,
    online: bool,
    latency_ms: float | None = None,
):
    """Update provider availability telemetry."""
    return cloud_api.set_online(
        provider=provider,
        online=online,
        latency_ms=latency_ms,
    )


@app.post("/cloud/start")
def cloud_start():
    """Start cloud monitoring."""
    return cloud_api.start()


@app.post("/cloud/stop")
def cloud_stop():
    """Stop cloud monitoring."""
    return cloud_api.stop()


@app.post("/cloud/restart")
def cloud_restart():
    """Restart cloud monitoring."""
    return cloud_api.restart()


# =========================================================
# GLOBAL INTEGRATIONS
# =========================================================

@app.get("/integrations")
def integrations_definitions():
    """Return registered global integrations."""
    return integrations_api.definitions()


@app.get("/integrations/status")
def integrations_status():
    """Return safe integration readiness status."""
    return integrations_api.statuses()


@app.get("/integrations/health")
def integrations_health():
    """Return global integrations health."""
    return integrations_api.health()


@app.get("/integrations/{provider}/authorization")
def integration_authorization(
    provider: str,
):
    """Return authorization requirements."""
    return integrations_api.authorization_requirements(
        provider
    )


@app.get("/integrations/{provider}")
def integration_status(
    provider: str,
):
    """Return status for one integration provider."""
    return integrations_api.status(
        provider
    )


# =========================================================
# INTEGRATION CONNECTIONS
# =========================================================

@app.get("/integration-connections")
def integration_connections_statuses():
    """Return all provider connection states."""
    return integration_connections_api.statuses()


@app.get("/integration-connections/health")
def integration_connections_health():
    """Return provider connection health."""
    return integration_connections_api.health()


@app.get("/integration-connections/{provider}")
def integration_connection_status(
    provider: str,
):
    """Return one provider connection state."""
    return integration_connections_api.status(
        provider
    )


@app.post(
    "/integration-connections/{provider}/connect"
)
def integration_connection_connect(
    provider: str,
):
    """Connect an explicitly authorized provider."""
    return integration_connections_api.connect(
        provider
    )


@app.post(
    "/integration-connections/{provider}/disconnect"
)
def integration_connection_disconnect(
    provider: str,
):
    """Disconnect a provider."""
    return integration_connections_api.disconnect(
        provider
    )


# =========================================================
# SUPREME ECOSYSTEM
# =========================================================

@app.get("/ecosystem")
def ecosystem_status():
    """Return Supreme Ecosystem status."""
    return ecosystem_api.status()


@app.get("/ecosystem/health")
def ecosystem_health():
    """Return Supreme Ecosystem health."""
    return ecosystem_api.health()


@app.get("/ecosystem/names")
def ecosystem_names():
    """Return registered ecosystem names."""
    return ecosystem_api.names()


@app.get("/ecosystem/list")
def ecosystem_list():
    """Return all registered ecosystems."""
    return ecosystem_api.list()


@app.get("/ecosystem/{ecosystem_id}")
def ecosystem_get(
    ecosystem_id: str,
):
    """Return one registered ecosystem."""
    return ecosystem_api.get(
        ecosystem_id
    )


# =========================================================
# STORAGE
# =========================================================

@app.get("/storage")
def storage_status():
    """Return storage status."""
    return storage_api.status()


@app.get("/storage/health")
def storage_health():
    """Return storage health."""
    return storage_api.health()


@app.get("/storage/configuration")
def storage_configuration():
    """Return safe storage configuration."""
    return storage_api.configuration()


@app.post("/storage/connect")
def storage_connect():
    """Connect to the storage layer."""
    return storage_api.connect()


@app.post("/storage/disconnect")
def storage_disconnect():
    """Disconnect from the storage layer."""
    return storage_api.disconnect()


# =========================================================
# CENTRAL AI STORE AUTHORIZATION BRIDGE
# =========================================================

def _require_ai_store_actor(
    authorization: Optional[str],
) -> str:
    """
    Resolve the authenticated actor from the authorization header.

    This layer requires a Bearer token.

    IMPORTANT:
    The current project auth system already exposes
    /auth/validate. The final production implementation
    should resolve the token through that canonical auth
    validation/session layer instead of trusting the token
    string itself as the actor ID.
    """

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

    # Temporary bridge.
    #
    # DO NOT treat the raw token as the permanent
    # application actor identity.
    #
    # The next authentication integration layer will
    # resolve:
    #
    # token -> session -> authenticated user -> actor_id
    #
    return token


# =========================================================
# CENTRAL AI STORE MODELS
# =========================================================

class AIStoreAssetRequest(BaseModel):
    area_id: str
    title: str
    asset_type: str = "FILE"
    workspace_id: Optional[str] = None
    mime_type: Optional[str] = None
    storage_key: Optional[str] = None
    file_url: Optional[str] = None
    content_class: Optional[str] = None
    metadata: str = ""


class AIStoreAccessRequest(BaseModel):
    principal_id: str
    action: str


class AIStoreMoveRequest(BaseModel):
    target_area: str


class AIStoreLockRequest(BaseModel):
    locked: bool


# =========================================================
# CENTRAL AI STORE
# =========================================================

@app.post("/storage/assets")
def create_ai_store_asset(
    request: AIStoreAssetRequest,
    authorization: Optional[str] = Header(
        default=None
    ),
):
    """
    Create a central AI Store asset.

    Owner identity is derived from the authenticated
    authorization context, not from the request body.
    """

    actor_id = _require_ai_store_actor(
        authorization
    )

    return storage_api.register_asset(
        owner_id=actor_id,
        area_id=request.area_id,
        title=request.title,
        asset_type=request.asset_type,
        workspace_id=request.workspace_id,
        mime_type=request.mime_type,
        storage_key=request.storage_key,
        file_url=request.file_url,
        content_class=request.content_class,
        metadata=request.metadata,
    )


@app.get("/storage/assets/{asset_id}")
def get_ai_store_asset(
    asset_id: str,
    authorization: Optional[str] = Header(
        default=None
    ),
):
    """
    Get one central AI Store asset.

    Authentication is required before asset access.
    """

    _require_ai_store_actor(
        authorization
    )

    asset = storage_api.get_asset(
        asset_id
    )

    if not asset:
        return {
            "success": False,
            "error": "ASSET_NOT_FOUND",
        }

    return {
        "success": True,
        "asset": asset,
    }


@app.post("/storage/assets/{asset_id}/access")
def grant_ai_store_access(
    asset_id: str,
    request: AIStoreAccessRequest,
    authorization: Optional[str] = Header(
        default=None
    ),
):
    """
    Grant an authorized principal access to an asset.

    The granting actor comes from authentication,
    not from the request body.
    """

    actor_id = _require_ai_store_actor(
        authorization
    )

    return storage_api.grant_access(
        asset_id=asset_id,
        principal_id=request.principal_id,
        action=request.action,
        granted_by=actor_id,
    )


@app.post("/storage/assets/{asset_id}/move")
def move_ai_store_asset(
    asset_id: str,
    request: AIStoreMoveRequest,
    authorization: Optional[str] = Header(
        default=None
    ),
):
    """Move an asset to another authorized area."""

    actor_id = _require_ai_store_actor(
        authorization
    )

    return storage_api.move_asset(
        asset_id=asset_id,
        target_area=request.target_area,
        actor_id=actor_id,
    )


@app.post("/storage/assets/{asset_id}/lock")
def lock_ai_store_asset(
    asset_id: str,
    request: AIStoreLockRequest,
    authorization: Optional[str] = Header(
        default=None
    ),
):
    """Lock or unlock an AI Store asset."""

    actor_id = _require_ai_store_actor(
        authorization
    )

    return storage_api.set_lock(
        asset_id=asset_id,
        locked=request.locked,
        actor_id=actor_id,
    )


@app.delete("/storage/assets/{asset_id}")
def delete_ai_store_asset(
    asset_id: str,
    authorization: Optional[str] = Header(
        default=None
    ),
):
    """Soft-delete an AI Store asset."""

    actor_id = _require_ai_store_actor(
        authorization
    )

    return storage_api.delete_asset(
        asset_id=asset_id,
        actor_id=actor_id,
    )


@app.post("/storage/assets/{asset_id}/restore")
def restore_ai_store_asset(
    asset_id: str,
    authorization: Optional[str] = Header(
        default=None
    ),
):
    """Restore a previously deleted AI Store asset."""

    actor_id = _require_ai_store_actor(
        authorization
    )

    return storage_api.restore_asset(
        asset_id=asset_id,
        actor_id=actor_id,
    )


# =========================================================
# HOME
# =========================================================

@app.get("/")
def home():
    """Return MAIN BASE FOUNDATION API status."""

    return {
        "project": "MAIN BASE FOUNDATION",
        "version": "1.0.0",
        "status": "RUNNING",
    }


# =========================================================
# PUBLIC FRONTEND
# =========================================================

FRONTEND_DIR = (
    Path(__file__).resolve().parents[2]
    / "frontend"
)


app.mount(
    "/frontend",
    StaticFiles(
        directory=FRONTEND_DIR,
        html=True,
    ),
    name="frontend",
)
