from typing import Dict

from .model import AICreationRequest, AICreationResult


class AICreationService:

    def __init__(self):
        self._requests: Dict[str, AICreationRequest] = {}
        self._results: Dict[str, AICreationResult] = {}
        self._counter = 0

    def _next_id(self):
        self._counter += 1
        return f"AI-{self._counter:06d}"

    def create_request(
        self,
        creation_type: str,
        prompt: str,
        options: dict | None = None,
    ):
        request = AICreationRequest(
            request_id=self._next_id(),
            creation_type=creation_type,
            prompt=prompt,
            options=options or {},
        )

        self._requests[request.request_id] = request

        result = AICreationResult(
            request_id=request.request_id,
            status="QUEUED",
            output_type=creation_type,
            metadata={
                "message": (
                    "Creation request accepted. "
                    "Generation engine can process this request."
                )
            },
        )

        self._results[request.request_id] = result

        return request, result

    def get_request(self, request_id):
        return self._requests.get(request_id)

    def get_result(self, request_id):
        return self._results.get(request_id)
