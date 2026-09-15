from typing import Dict

from .model import GenerationRequest


class GenerationEngineService:

    SUPPORTED_TYPES = {
        "MOVIE",
        "VIDEO",
        "PHOTO",
        "MUSIC",
        "GAME",
        "DESIGN",
        "SOFTWARE",
    }

    def __init__(self):
        self._requests: Dict[str, GenerationRequest] = {}
        self._counter = 0

    def _next_id(self):
        self._counter += 1
        return f"GEN-{self._counter:06d}"

    def create(
        self,
        creation_type: str,
        prompt: str,
        provider=None,
        model=None,
        options=None,
    ):
        creation_type = creation_type.upper()

        if creation_type not in self.SUPPORTED_TYPES:
            raise ValueError(
                f"Unsupported creation type: {creation_type}"
            )

        request = GenerationRequest(
            generation_id=self._next_id(),
            creation_type=creation_type,
            prompt=prompt,
            provider=provider,
            model=model,
            options=options or {},
        )

        self._requests[request.generation_id] = request

        return request

    def get(self, generation_id):
        return self._requests.get(generation_id)

    def list(self):
        return list(self._requests.values())

    def mark_processing(self, generation_id):
        request = self.get(generation_id)

        if request is None:
            return None

        request.status = "PROCESSING"
        return request

    def mark_completed(
        self,
        generation_id,
        output_url,
    ):
        request = self.get(generation_id)

        if request is None:
            return None

        request.status = "COMPLETED"
        request.output_url = output_url

        return request

    def mark_failed(self, generation_id):
        request = self.get(generation_id)

        if request is None:
            return None

        request.status = "FAILED"
        return request
