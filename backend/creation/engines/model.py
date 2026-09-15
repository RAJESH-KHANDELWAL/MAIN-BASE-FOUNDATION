from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, Optional


@dataclass
class GenerationRequest:
    generation_id: str
    creation_type: str
    prompt: str
    provider: Optional[str] = None
    model: Optional[str] = None
    options: Dict = field(default_factory=dict)
    status: str = "QUEUED"
    output_url: Optional[str] = None
    created_at: str = field(
        default_factory=lambda:
        datetime.now(timezone.utc).isoformat()
    )

    def to_dict(self):
        return {
            "generation_id": self.generation_id,
            "creation_type": self.creation_type,
            "prompt": self.prompt,
            "provider": self.provider,
            "model": self.model,
            "options": self.options,
            "status": self.status,
            "output_url": self.output_url,
            "created_at": self.created_at,
        }
