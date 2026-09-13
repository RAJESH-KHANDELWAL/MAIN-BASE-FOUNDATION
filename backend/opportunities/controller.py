"""Controller for opportunity operations."""

from backend.opportunities.service import OpportunityService


class OpportunityController:
    def __init__(self):
        self.service = OpportunityService()

    def initialize(self):
        return self.service.initialize()

    def create(self, **kwargs):
        return self.service.create_opportunity(**kwargs)

    def get(self, opportunity_id):
        return self.service.get_opportunity(opportunity_id)

    def list(self):
        return self.service.get_all_opportunities()

    def live(self):
        return self.service.get_live_opportunities()

    def update_status(self, opportunity_id, status):
        return self.service.update_status(
            opportunity_id,
            status,
        )
