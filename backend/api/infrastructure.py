"""
MAIN BASE FOUNDATION
Infrastructure Control Plane API

Public API facade for infrastructure inventory.
"""

from fastapi import APIRouter

from backend.infrastructure.domains.controller import DomainController
from backend.infrastructure.hosting.controller import HostingController
from backend.infrastructure.servers.controller import ServerController
from backend.infrastructure.ipam.controller import IPAMController
from backend.infrastructure.network.controller import NetworkController
from backend.infrastructure.dns.controller import DNSController


router = APIRouter(
    prefix="/infrastructure",
    tags=["Infrastructure Control Plane"],
)


domain_controller = DomainController()
hosting_controller = HostingController()
server_controller = ServerController()
ipam_controller = IPAMController()
network_controller = NetworkController()
dns_controller = DNSController()


def _safe_list(name, callback):
    try:
        data = callback()
        return {
            "status": "LIVE",
            "count": len(data),
            "data": data,
        }
    except Exception as exc:
        return {
            "status": "ERROR",
            "count": 0,
            "data": [],
            "error": f"{type(exc).__name__}: {exc}",
        }


@router.get("/")
def infrastructure_status():
    return {
        "project": "MAIN BASE FOUNDATION",
        "system": "INFRASTRUCTURE CONTROL PLANE",
        "status": "RUNNING",
        "modules": {
            "domains": "READY",
            "hosting": "READY",
            "servers": "READY",
            "ipam": "READY",
            "network": "READY",
            "dns": "READY",
        },
    }


@router.get("/domains")
def list_domains():
    return domain_controller.list()


@router.get("/hosting")
def list_hosting():
    return hosting_controller.list()


@router.get("/servers")
def list_servers():
    return server_controller.list()


@router.get("/ipam")
def list_ip_addresses():
    return ipam_controller.list()


@router.get("/network")
def list_networks():
    return network_controller.list()


@router.get("/dns/zones")
def list_dns_zones():
    return dns_controller.list_zones()


@router.get("/dns/records")
def list_dns_records():
    return dns_controller.list_records()


@router.get("/summary")
def infrastructure_summary():

    modules = {
        "domains": _safe_list(
            "domains",
            domain_controller.list,
        ),
        "hosting": _safe_list(
            "hosting",
            hosting_controller.list,
        ),
        "servers": _safe_list(
            "servers",
            server_controller.list,
        ),
        "ip_addresses": _safe_list(
            "ip_addresses",
            ipam_controller.list,
        ),
        "networks": _safe_list(
            "networks",
            network_controller.list,
        ),
        "dns_zones": _safe_list(
            "dns_zones",
            dns_controller.list_zones,
        ),
        "dns_records": _safe_list(
            "dns_records",
            dns_controller.list_records,
        ),
    }

    live_modules = [
        name
        for name, result in modules.items()
        if result["status"] == "LIVE"
    ]

    error_modules = [
        name
        for name, result in modules.items()
        if result["status"] == "ERROR"
    ]

    overall_status = (
        "LIVE"
        if not error_modules
        else "PARTIAL_ERROR"
    )

    return {
        "project": "MAIN BASE FOUNDATION",
        "system": "INFRASTRUCTURE CONTROL PLANE",
        "status": overall_status,
        "total_modules": len(modules),
        "live_modules": len(live_modules),
        "error_modules": len(error_modules),
        "counts": {
            name: result["count"]
            for name, result in modules.items()
        },
        "modules": modules,
    }
