from typing import List, Tuple

from fastapi import HTTPException
from sqlalchemy.orm import Session

from models import Interview, User
from repositories import interview_repository
from schemas import (
    InterviewListResponse,
    InterviewResponse,
    InterviewReviewResponse,
)


def list_interviews(db: Session, current_user: User) -> InterviewListResponse:
    items = interview_repository.get_interviews_by_user(db, current_user.id)
    return InterviewListResponse(
        items=[InterviewResponse.model_validate(i) for i in items],
        total=len(items),
    )


def _get_owned_interview(db: Session, user_id: int, interview_id: int) -> Interview:
    interview = interview_repository.get_interview(db, interview_id)
    if not interview or interview.application.user_id != user_id:
        raise HTTPException(status_code=404, detail="面试记录不存在")
    return interview


def get_interview(db: Session, current_user: User, interview_id: int) -> InterviewResponse:
    interview = _get_owned_interview(db, current_user.id, interview_id)
    return InterviewResponse.model_validate(interview)


def _review_for_result(result: str) -> Tuple[str, List[str]]:
    if result == "已通过":
        return "面试表现良好，成功通过。继续保持并总结成功经验。", [
            "总结本次面试中被问到的重点问题，形成自己的答题模板。",
            "记录面试官的反馈，沉淀为个人面试笔记。",
            "为后续 HR 面或终面做好准备。",
        ]
    if result == "未通过":
        return "本次面试未通过，建议复盘并针对性改进。", [
            "回顾面试中答得不好的问题，补充相关知识点。",
            "加强表达的逻辑性，练习 STAR 法则回答行为类问题。",
            "针对薄弱环节做专项训练，如算法题、系统设计等。",
        ]
    return "面试已结束，结果待定。", [
        "记录面试中被问到的题目与自己的回答，便于复盘。",
        "保持耐心等待结果，必要时礼貌跟进。",
        "无论结果如何，持续准备其他机会。",
    ]


def review_interview(
    db: Session,
    current_user: User,
    interview_id: int,
) -> InterviewReviewResponse:
    interview = _get_owned_interview(db, current_user.id, interview_id)
    review, suggestions = _review_for_result(interview.result)

    interview.review = review
    interview_repository.update_interview(db, interview)

    return InterviewReviewResponse(
        interview_id=interview.id,
        result=interview.result,
        review=review,
        suggestions=suggestions,
    )
