from .service import AICreationService


class AICreationController:

    def __init__(self):
        self.service = AICreationService()

    def create(
        self,
        creation_type,
        prompt,
        options=None,
    ):
        request, result = self.service.create_request(
            creation_type=creation_type,
            prompt=prompt,
            options=options,
        )

        return {
            "request": request.to_dict(),
            "result": result.to_dict(),
        }

    def get_request(self, request_id):
        request = self.service.get_request(request_id)
        return request.to_dict() if request else None

    def get_result(self, request_id):
        result = self.service.get_result(request_id)
        return result.to_dict() if result else None
