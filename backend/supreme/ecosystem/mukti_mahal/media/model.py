"""
MUKTI MAHAL MEDIA ASSET MODEL
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class MuktiMahalMediaAsset:
    asset_id: str
    mahal_id: str
    project_id: Optional[str]
    division_id: Optional[str]
    title: str
    asset_type: str
    description: str = ""
    file_url: Optional[str] = None
    storage_key: Optional[str] = None
    mime_type: Optional[str] = None
    file_size: int = 0
    status: str = "DRAFT"
    created_at: str = ""
    updated_at: str = ""
