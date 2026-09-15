from typing import Dict

from .model import (
    ProviderCapability,
    ProviderGenerationResult,
)


class ProviderService:

    def __init__(self):
        self._providers: Dict[str, ProviderCapability] = {}

    def register_provider(
        self,
        provider: str,
        capabilities: list[str],
        models: list[str],
        available: bool = False,
    ):
        item = ProviderCapability(
            provider=provider,
            capabilities=capabilities,
            models=models,
            available=available,
        )

        self._providers[provider] = item
        return item

    def get_provider(self, provider: str):
        return self._providers.get(provider)

    def list_providers(self):
        return list(self._providers.values())

    def can_generate(
        self,
        provider: str,
        creation_type: str,
    ):
        item = self.get_provider(provider)

        if item is None:
            return False

        return (
            item.available
            and creation_type.upper()
            in [x.upper() for x in item.capabilities]
        )

    def generation_result(
        self,
        provider: str,
        model: str,
        creation_type: str,
        status: str = "READY",
        output_url=None,
        metadata=None,
    ):
        return ProviderGenerationResult(
            provider=provider,
            model=model,
            creation_type=creation_type,
            status=status,
            output_url=output_url,
            metadata=metadata or {},
        )
