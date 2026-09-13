"""Controller for universal profiles."""

from backend.profiles.service import ProfileService


class ProfileController:

    def __init__(self):
        self.service = ProfileService()

    def initialize(self):
        return self.service.initialize()

    def create(self, **kwargs):
        return self.service.create_profile(**kwargs)

    def get(self, profile_id):
        return self.service.get_profile(profile_id)

    def list_for_identity(self, master_id):
        return self.service.get_profiles_for_identity(master_id)

    def list_by_type(self, profile_type):
        return self.service.get_profiles_by_type(profile_type)

    def update_status(self, profile_id, status):
        return self.service.update_status(
            profile_id,
            status,
        )
