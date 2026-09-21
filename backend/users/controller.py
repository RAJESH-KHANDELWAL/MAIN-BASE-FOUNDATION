"""User controller layer."""

from backend.users.service import UserService


class UserController:
    """Coordinate API requests with UserService."""

    def __init__(self):
        self.service = UserService()

    def initialize(self):
        return self.service.initialize()

    def register(self, **kwargs):
        user = self.service.create_user(**kwargs)
        return self.service.save_user(user)

    def get(self, user_id):
        return self.service.get_user(user_id)

    def update(self, **kwargs):
        return self.service.update_user(**kwargs)

    def delete(self, user_id):
        return self.service.delete_user(user_id)

    def list(self):
        return self.service.get_all_users()

    def search(self, username):
        return self.service.search_user_by_username(username)

    def verify_password(self, username, password):
        return self.service.verify_user_password(
            username,
            password,
        )


__all__ = ["UserController"]
