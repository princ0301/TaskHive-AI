from pydantic import BaseModel
from datetime import datetime
from db.models import JobStatus

class StartJobRequest(BaseModel):
    topic: str

class JobResponse(BaseModel):
    id: str
    topic: str
    status: JobStatus
    report: str | None = None
    error: str | None = None
    created_at: datetime
    completed_at: datetime | None = None

    class Config:
        from_attributes = True


class JobListResponse(BaseModel):
    jobs: list[JobResponse]
    total: int