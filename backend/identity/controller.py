"""Identity controller layer."""

from backend.identity.service import IdentityService


class IdentityController:
    """Coordinate identity API requests with the service."""

    def __init__(self):
        self.service = IdentityService()

    def initialize(self):
        return self.service.initialize()

    def create(self, **kwargs):
        identity = self.service.create_identity(**kwargs)
        return self.service.save_identity(identity)

    def get(self, master_id):
        return self.service.get_identity(master_id)

    def list(self):
        return self.service.list_identity()

    def update(self, master_id, **kwargs):
        return self.service.update_identity(
            master_id,
            **kwargs,
        )

    def delete(self, master_id):
        return self.service.delete_identity(master_id)

    def search(self, keyword):
        return self.service.search_identities(keyword)

    def verify(self, master_id):
        return self.service.verify_identity(master_id)

    def exists(self, master_id):
        return self.service.identity_exists(master_id)


__all__ = ["IdentityController"]
