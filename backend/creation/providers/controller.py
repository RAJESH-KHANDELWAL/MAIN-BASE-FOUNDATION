from .service import ProviderService


class ProviderController:

    def __init__(self):
        self.service = ProviderService()

    def register(
        self,
        provider,
        capabilities,
        models,
        available=False,
    ):
        return self.service.register_provider(
            provider=provider,
            capabilities=capabilities,
            models=models,
            available=available,
        ).to_dict()

    def get(self, provider):
        item = self.service.get_provider(provider)
        return item.to_dict() if item else None

    def list(self):
        return [
            item.to_dict()
            for item in self.service.list_providers()
        ]

    def can_generate(
        self,
        provider,
        creation_type,
    ):
        return self.service.can_generate(
            provider,
            creation_type,
        )

    def result(
        self,
        provider,
        model,
        creation_type,
        status="READY",
        output_url=None,
        metadata=None,
    ):
        return self.service.generation_result(
            provider=provider,
            model=model,
            creation_type=creation_type,
            status=status,
            output_url=output_url,
            metadata=metadata,
        ).to_dict()
