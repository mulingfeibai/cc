from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from schemas import (
    MessageResponse,
    ResumeCreate,
    ResumeListResponse,
    ResumeOptimizeResponse,
    ResumeResponse,
    ResumeUpdate,
)
from services import resume_service
from utils.security import get_current_user

router = APIRouter(prefix="/api/resumes", tags=["简历"])


@router.get("", response_model=ResumeListResponse)
def list_resumes(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return resume_service.list_resumes(db, current_user)


@router.post("", response_model=ResumeResponse, status_code=201)
def create_resume(
    data: ResumeCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return resume_service.create_resume(db, current_user, data)


@router.get("/{resume_id}", response_model=ResumeResponse)
def get_resume(
    resume_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return resume_service.get_resume(db, current_user, resume_id)


@router.put("/{resume_id}", response_model=ResumeResponse)
def update_resume(
    resume_id: int,
    data: ResumeUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return resume_service.update_resume(db, current_user, resume_id, data)


@router.delete("/{resume_id}", response_model=MessageResponse)
def delete_resume(
    resume_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return resume_service.delete_resume(db, current_user, resume_id)


@router.post("/{resume_id}/optimize", response_model=ResumeOptimizeResponse)
def optimize_resume(
    resume_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return resume_service.optimize_resume(db, current_user, resume_id)
