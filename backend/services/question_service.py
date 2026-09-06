from typing import List

from fastapi import HTTPException
from sqlalchemy.orm import Session

from models import Question, User, UserAnswer
from repositories import question_repository
from schemas import (
    AnswerHistoryItem,
    AnswerHistoryResponse,
    AnswerSubmitRequest,
    AnswerSubmitResponse,
    MessageResponse,
    QuestionListResponse,
    QuestionResponse,
    WrongQuestionItem,
    WrongQuestionListResponse,
)


def list_questions(
    db: Session,
    category: str = None,
    difficulty: str = None,
) -> QuestionListResponse:
    items = question_repository.get_questions(db, category, difficulty)
    return QuestionListResponse(
        items=[QuestionResponse.model_validate(q) for q in items],
        total=len(items),
    )


def get_question(db: Session, question_id: int) -> QuestionResponse:
    question = question_repository.get_question(db, question_id)
    if not question:
        raise HTTPException(status_code=404, detail="题目不存在")
    return QuestionResponse.model_validate(question)


def _judge_choice(options: List[str], answer: str, user_answer: str) -> bool:
    ua = user_answer.strip()
    if ua.upper() == answer.upper():
        return True
    idx = ord(answer.upper()) - ord("A")
    if options and 0 <= idx < len(options) and ua == options[idx]:
        return True
    return False


def _judge(question: Question, user_answer: str) -> bool:
    if question.question_type == "选择":
        return _judge_choice(question.options or [], question.answer or "", user_answer)
    # 简答题：按回答长度粗判（>= 20 字视为正确），模拟判断
    return len(user_answer.strip()) >= 20


def submit_answer(
    db: Session,
    current_user: User,
    data: AnswerSubmitRequest,
) -> AnswerSubmitResponse:
    question = question_repository.get_question(db, data.question_id)
    if not question:
        raise HTTPException(status_code=404, detail="题目不存在")

    is_correct = _judge(question, data.user_answer)

    user_answer = UserAnswer(
        user_id=current_user.id,
        question_id=question.id,
        user_answer=data.user_answer,
        is_correct=is_correct,
    )
    question_repository.create_user_answer(db, user_answer)

    if not is_correct:
        question_repository.add_wrong_question(db, current_user.id, question.id)

    return AnswerSubmitResponse(
        question_id=question.id,
        is_correct=is_correct,
        correct_answer=question.answer or "",
        analysis=question.analysis or "",
    )


def list_wrong_questions(db: Session, current_user: User) -> WrongQuestionListResponse:
    items = question_repository.get_wrong_questions_by_user(db, current_user.id)
    return WrongQuestionListResponse(
        items=[
            WrongQuestionItem(
                question_id=w.question_id,
                created_at=w.created_at,
                question=QuestionResponse.model_validate(w.question),
            )
            for w in items
        ],
        total=len(items),
    )


def list_answer_history(db: Session, current_user: User) -> AnswerHistoryResponse:
    items = question_repository.get_user_answers_by_user(db, current_user.id)
    return AnswerHistoryResponse(
        items=[
            AnswerHistoryItem(
                id=a.id,
                question_id=a.question_id,
                user_answer=a.user_answer or "",
                is_correct=a.is_correct,
                created_at=a.created_at,
                question=QuestionResponse.model_validate(a.question),
            )
            for a in items
        ],
        total=len(items),
    )


def delete_wrong_question(
    db: Session,
    current_user: User,
    question_id: int,
) -> MessageResponse:
    removed = question_repository.delete_wrong_question(db, current_user.id, question_id)
    if not removed:
        raise HTTPException(status_code=404, detail="该题目不在错题本中")
    return MessageResponse(detail="已从错题本移除")
