from .service import CreationOrchestrator


class CreationOrchestratorController:

    def __init__(self):
        self.service = CreationOrchestrator()

    def submit(
        self,
        creation_type,
        prompt,
        provider=None,
        model=None,
        metadata=None,
    ):
        return self.service.submit(
            creation_type=creation_type,
            prompt=prompt,
            provider=provider,
            model=model,
            metadata=metadata,
        ).to_dict()

    def get(self, job_id):
        job = self.service.get(job_id)
        return job.to_dict() if job else None

    def list(self):
        return [
            job.to_dict()
            for job in self.service.list()
        ]

    def processing(self, job_id):
        job = self.service.processing(job_id)
        return job.to_dict() if job else None

    def complete(self, job_id, output_url):
        job = self.service.complete(
            job_id,
            output_url,
        )
        return job.to_dict() if job else None

    def fail(self, job_id):
        job = self.service.fail(job_id)
        return job.to_dict() if job else None
