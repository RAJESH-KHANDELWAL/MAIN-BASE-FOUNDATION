"""Authentication controller layer."""

from backend.auth.service import AuthenticationService


class AuthenticationController:
    """Coordinate authentication API requests."""

    def __init__(self):
        self.service = AuthenticationService()

    def initialize(self):
        return self.service.initialize()

    def authenticate(self, master_id):
        return self.service.authenticate(
            master_id
        )

    def login(
        self,
        master_id=None,
        username=None,
        password=None,
    ):
        return self.service.login(
            master_id=master_id,
            username=username,
            password=password,
        )

    def validate_token(self, token):
        return self.service.validate_token(
            token
        )

    def logout(
        self,
        token=None,
        session_id=None,
    ):
        return self.service.logout(
            token=token,
            session_id=session_id,
        )


__all__ = ["AuthenticationController"]
