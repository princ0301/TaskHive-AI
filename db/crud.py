from sqlalchemy.orm import Session
from db.models import ResearchJob, JobStatus
from datetime import datetime
import uuid

def create_job(db: Session, topic: str) -> ResearchJob:
    job = ResearchJob(
        id=str(uuid.uuid4()),
        topic=topic,
        status=JobStatus.PENDING
    )
    db.add(job)
    db.commit()
    db.refresh(job)
    return job

def get_job(db: Session, job_id: str) -> ResearchJob | None:
    return db.query(ResearchJob).filter(ResearchJob.id == job_id).first()

def get_all_jobs(db: Session, limit: int = 20) -> list[ResearchJob]:
    return db.query(ResearchJob).order_by(
        ResearchJob.created_at.desc()
    ).limit(limit).all()

def update_job_running(db: Session, job_id: str):
    job = get_job(db, job_id)
    if job:
        job.status = JobStatus.RUNNING
        db.commit()

def update_job_completed(db: Session, job_id: str, report: str):
    job = get_job(db, job_id)
    if job:
        job.status = JobStatus.COMPLETED
        job.report = report
        job.completed_at = datetime.utcnow()
        db.commit()

def update_job_failed(db: Session, job_id: str, error: str):
    job = get_job(db, job_id)
    if job:
        job.status = JobStatus.FAILED
        job.error = error
        job.completed_at = datetime.utcnow()
        db.commit()