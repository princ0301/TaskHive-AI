from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from db import get_db, create_job, get_job, get_all_jobs, update_job_running, update_job_completed, update_job_failed
from db.database import SessionLocal
from api.schemas import StartJobRequest, JobResponse, JobListResponse
from crew.research_crew import run_research_crew

router = APIRouter(prefix="/api", tags=["Research"])

def run_crew_background(job_id: str, topic: str):
    db = SessionLocal()
    try:
        update_job_running(db, job_id)
        result = run_research_crew(topic)
        update_job_completed(db, job_id, result["report"])
    except Exception as e:
        update_job_failed(db, job_id, str(e))
    finally:
        db.close()

@router.post("/jobs", response_model=JobResponse, status_code=201)
def start_research_job(
    request: StartJobRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    
    if not request.topic.strip():
        raise HTTPException(status_code=400, detail="Topic cannot be empty")
    
    job = create_job(db, request.topic.strip())

    background_tasks.add_task(run_crew_background, job.id, job.topic)

    return job

@router.get("/jobs/{job_id}", response_model=JobResponse)
def get_research_job(job_id: str, db: Session = Depends(get_db)):
    job = get_job(db, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

@router.get("/jobs", response_model=JobListResponse)
def list_research_jobs(db: Session = Depends(get_db)):
    jobs = get_all_jobs(db)
    return JobListResponse(jobs=jobs, total=len(jobs))

@router.delete("/jobs/{job_id}", status_code=204)
def delete_job(job_id: str, db: Session = Depends(get_db)):
    job = get_job(db, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    db.delete(job)
    db.commit()
