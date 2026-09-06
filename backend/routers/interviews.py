from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from schemas import InterviewListResponse, InterviewResponse, InterviewReviewResponse
from services import interview_service
from utils.security import get_current_user

router = APIRouter(prefix="/api/interviews", tags=["面试记录"])


@router.get("", response_model=InterviewListResponse)
def list_interviews(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return interview_service.list_interviews(db, current_user)


@router.get("/{interview_id}", response_model=InterviewResponse)
def get_interview(
    interview_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return interview_service.get_interview(db, current_user, interview_id)


@router.post("/{interview_id}/review", response_model=InterviewReviewResponse)
def review_interview(
    interview_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return interview_service.review_interview(db, current_user, interview_id)
