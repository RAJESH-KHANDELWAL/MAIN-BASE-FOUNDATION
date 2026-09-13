"""Email infrastructure controller."""

from .service import EmailService


class EmailController:
    def __init__(self):
        self.service = EmailService()

    def create(self, **kwargs) -> dict:
        email = self.service.create(**kwargs)
        return email.to_dict()

    def get(self, email_id: str) -> dict | None:
        email = self.service.get(email_id)

        if not email:
            return None

        return email.to_dict()

    def list(self) -> list[dict]:
        return [
            email.to_dict()
            for email in self.service.list_all()
        ]

    def update_status(
        self,
        email_id: str,
        status: str,
    ) -> dict | None:

        email = self.service.update_status(
            email_id,
            status,
        )

        if not email:
            return None

        return email.to_dict()

    def delete(self, email_id: str) -> bool:
        return self.service.delete(email_id)
