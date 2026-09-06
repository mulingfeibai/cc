from typing import List, Optional

from sqlalchemy.orm import Session, joinedload

from models import Application, Interview


def get_interviews_by_user(db: Session, user_id: int) -> List[Interview]:
    return (
        db.query(Interview)
        .join(Application, Interview.application_id == Application.id)
        .filter(Application.user_id == user_id)
        .order_by(Interview.created_at.desc())
        .all()
    )


def get_interview(db: Session, interview_id: int) -> Optional[Interview]:
    return (
        db.query(Interview)
        .options(joinedload(Interview.application))
        .filter(Interview.id == interview_id)
        .first()
    )


def update_interview(db: Session, interview: Interview) -> Interview:
    db.commit()
    db.refresh(interview)
    return interview


def count_interviews_by_user(db: Session, user_id: int) -> int:
    return (
        db.query(Interview)
        .join(Application, Interview.application_id == Application.id)
        .filter(Application.user_id == user_id)
        .count()
    )
