from typing import Dict, List, Optional

from .model import CreationJob


class CreationOrchestrator:

    def __init__(self):
        self._jobs: Dict[str, CreationJob] = {}
        self._counter = 0

    def _next_id(self):
        self._counter += 1
        return f"JOB-{self._counter:06d}"

    def submit(
        self,
        creation_type: str,
        prompt: str,
        provider: Optional[str] = None,
        model: Optional[str] = None,
        metadata: Optional[dict] = None,
    ):

        job = CreationJob(
            job_id=self._next_id(),
            creation_type=creation_type.upper(),
            prompt=prompt,
            provider=provider,
            model=model,
            metadata=metadata or {},
        )

        self._jobs[job.job_id] = job
        return job

    def get(self, job_id: str):
        return self._jobs.get(job_id)

    def list(self) -> List[CreationJob]:
        return list(self._jobs.values())

    def processing(self, job_id: str):
        job = self.get(job_id)

        if job is None:
            return None

        job.status = "PROCESSING"
        return job

    def complete(
        self,
        job_id: str,
        output_url: str,
    ):
        job = self.get(job_id)

        if job is None:
            return None

        job.status = "COMPLETED"
        job.output_url = output_url
        return job

    def fail(self, job_id: str):
        job = self.get(job_id)

        if job is None:
            return None

        job.status = "FAILED"
        return job
