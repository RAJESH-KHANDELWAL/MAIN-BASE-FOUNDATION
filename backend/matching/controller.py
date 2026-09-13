"""Controller for the matching engine."""

from backend.matching.model import MatchingProfile
from backend.matching.service import MatchingService


class MatchingController:

    def __init__(self):
        self.service = MatchingService()

    def match(self, profile: MatchingProfile):
        return self.service.find_matches(profile)
