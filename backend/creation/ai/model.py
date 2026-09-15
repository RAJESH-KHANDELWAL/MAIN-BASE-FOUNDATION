from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, Optional


@dataclass
class AICreationRequest:
    request_id: str
    creation_type: str
    prompt: str
    options: Dict = field(default_factory=dict)
    created_at: str = field(
        default_factory=lambda:
        datetime.now(timezone.utc).isoformat()
    )

    def to_dict(self):
        return {
            "request_id": self.request_id,
            "creation_type": self.creation_type,
            "prompt": self.prompt,
            "options": self.options,
            "created_at": self.created_at,
        }


@dataclass
class AICreationResult:
    request_id: str
    status: str
    output_type: str
    output_url: Optional[str] = None
    metadata: Dict = field(default_factory=dict)

    def to_dict(self):
        return {
            "request_id": self.request_id,
            "status": self.status,
            "output_type": self.output_type,
            "output_url": self.output_url,
            "metadata": self.metadata,
        }
