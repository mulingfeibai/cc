from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from schemas import (
    AnswerSubmitRequest,
    AnswerSubmitResponse,
    HistoryResponse,
    InterviewReportResponse,
    InterviewStartRequest,
    InterviewStartResponse,
    QuestionResponse,
)
from services import auth_service, interview_service

router = APIRouter(prefix="/api/interview", tags=["interview"])


@router.post("/start", response_model=InterviewStartResponse)
def start_interview(
    data: InterviewStartRequest,
    db: Session = Depends(get_db),
    current_user=Depends(auth_service.get_current_user),
):
    return interview_service.start_interview(db, current_user, data)


@router.get("/history", response_model=HistoryResponse)
def get_history(
    db: Session = Depends(get_db),
    current_user=Depends(auth_service.get_current_user),
):
    return interview_service.get_history(db, current_user)


@router.get("/{session_id}/question", response_model=QuestionResponse)
def get_question(
    session_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(auth_service.get_current_user),
):
    return interview_service.get_next_question(db, current_user, session_id)


@router.post("/{session_id}/answer", response_model=AnswerSubmitResponse)
def submit_answer(
    session_id: int,
    data: AnswerSubmitRequest,
    db: Session = Depends(get_db),
    current_user=Depends(auth_service.get_current_user),
):
    return interview_service.submit_answer(db, current_user, session_id, data)


@router.get("/{session_id}/report", response_model=InterviewReportResponse)
def get_report(
    session_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(auth_service.get_current_user),
):
    return interview_service.get_report(db, current_user, session_id)
