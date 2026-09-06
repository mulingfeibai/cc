from typing import List, Optional

from sqlalchemy.orm import Session

from models import Resume


def get_resumes_by_user(db: Session, user_id: int) -> List[Resume]:
    return (
        db.query(Resume)
        .filter(Resume.user_id == user_id)
        .order_by(Resume.created_at.desc())
        .all()
    )


def get_resume(db: Session, resume_id: int) -> Optional[Resume]:
    return db.query(Resume).filter(Resume.id == resume_id).first()


def create_resume(db: Session, resume: Resume) -> Resume:
    db.add(resume)
    db.commit()
    db.refresh(resume)
    return resume


def update_resume(db: Session, resume: Resume, data: dict) -> Resume:
    for key, value in data.items():
        if value is not None:
            setattr(resume, key, value)
    db.commit()
    db.refresh(resume)
    return resume


def delete_resume(db: Session, resume: Resume) -> None:
    db.delete(resume)
    db.commit()


def count_resumes_by_user(db: Session, user_id: int) -> int:
    return db.query(Resume).filter(Resume.user_id == user_id).count()
