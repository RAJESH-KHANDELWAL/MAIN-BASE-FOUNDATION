from dataclasses import dataclass, field
from typing import Dict, Optional


@dataclass
class ProviderCapability:
    provider: str
    capabilities: list[str] = field(default_factory=list)
    models: list[str] = field(default_factory=list)
    available: bool = False

    def to_dict(self):
        return {
            "provider": self.provider,
            "capabilities": self.capabilities,
            "models": self.models,
            "available": self.available,
        }


@dataclass
class ProviderGenerationResult:
    provider: str
    model: str
    creation_type: str
    status: str
    output_url: Optional[str] = None
    metadata: Dict = field(default_factory=dict)

    def to_dict(self):
        return {
            "provider": self.provider,
            "model": self.model,
            "creation_type": self.creation_type,
            "status": self.status,
            "output_url": self.output_url,
            "metadata": self.metadata,
        }
