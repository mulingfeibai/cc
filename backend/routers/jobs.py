from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from schemas import JobListResponse, JobMatchRequest, JobMatchResponse, JobResponse
from services import job_service
from utils.security import get_current_user

router = APIRouter(prefix="/api/jobs", tags=["岗位"])


@router.get("", response_model=JobListResponse)
def list_jobs(
    company_id: Optional[int] = None,
    job_type: Optional[str] = None,
    keyword: Optional[str] = None,
    db: Session = Depends(get_db),
):
    return job_service.list_jobs(db, company_id, job_type, keyword)


@router.get("/{job_id}", response_model=JobResponse)
def get_job(job_id: int, db: Session = Depends(get_db)):
    return job_service.get_job(db, job_id)


@router.post("/{job_id}/match", response_model=JobMatchResponse)
def match(
    job_id: int,
    data: JobMatchRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return job_service.match_resume(db, current_user, job_id, data)
