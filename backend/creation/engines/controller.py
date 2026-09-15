from .service import GenerationEngineService


class GenerationEngineController:

    def __init__(self):
        self.service = GenerationEngineService()

    def create(
        self,
        creation_type,
        prompt,
        provider=None,
        model=None,
        options=None,
    ):
        return self.service.create(
            creation_type=creation_type,
            prompt=prompt,
            provider=provider,
            model=model,
            options=options,
        ).to_dict()

    def get(self, generation_id):
        item = self.service.get(generation_id)
        return item.to_dict() if item else None

    def list(self):
        return [
            item.to_dict()
            for item in self.service.list()
        ]

    def processing(self, generation_id):
        item = self.service.mark_processing(generation_id)
        return item.to_dict() if item else None

    def completed(self, generation_id, output_url):
        item = self.service.mark_completed(
            generation_id,
            output_url,
        )
        return item.to_dict() if item else None

    def failed(self, generation_id):
        item = self.service.mark_failed(generation_id)
        return item.to_dict() if item else None
