from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, Optional


@dataclass
class CreationJob:
    job_id: str
    creation_type: str
    prompt: str
    provider: Optional[str] = None
    model: Optional[str] = None
    status: str = "QUEUED"
    output_url: Optional[str] = None
    metadata: Dict = field(default_factory=dict)
    created_at: str = field(
        default_factory=lambda:
        datetime.now(timezone.utc).isoformat()
    )

    def to_dict(self):
        return {
            "job_id": self.job_id,
            "creation_type": self.creation_type,
            "prompt": self.prompt,
            "provider": self.provider,
            "model": self.model,
            "status": self.status,
            "output_url": self.output_url,
            "metadata": self.metadata,
            "created_at": self.created_at,
        }
