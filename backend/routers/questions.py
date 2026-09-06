from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from schemas import (
    AnswerHistoryResponse,
    AnswerSubmitRequest,
    AnswerSubmitResponse,
    MessageResponse,
    QuestionListResponse,
    QuestionResponse,
    WrongQuestionListResponse,
)
from services import question_service
from utils.security import get_current_user

router = APIRouter(prefix="/api/questions", tags=["题库"])


@router.post("/answer", response_model=AnswerSubmitResponse)
def submit_answer(
    data: AnswerSubmitRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return question_service.submit_answer(db, current_user, data)


@router.get("/wrong", response_model=WrongQuestionListResponse)
def list_wrong_questions(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return question_service.list_wrong_questions(db, current_user)


@router.get("/history", response_model=AnswerHistoryResponse)
def list_answer_history(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return question_service.list_answer_history(db, current_user)


@router.delete("/wrong/{question_id}", response_model=MessageResponse)
def delete_wrong_question(
    question_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return question_service.delete_wrong_question(db, current_user, question_id)


@router.get("", response_model=QuestionListResponse)
def list_questions(
    category: Optional[str] = None,
    difficulty: Optional[str] = None,
    db: Session = Depends(get_db),
):
    return question_service.list_questions(db, category, difficulty)


@router.get("/{question_id}", response_model=QuestionResponse)
def get_question(question_id: int, db: Session = Depends(get_db)):
    return question_service.get_question(db, question_id)
