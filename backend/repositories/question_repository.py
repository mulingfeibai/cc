from typing import List, Optional

from sqlalchemy.orm import Session, joinedload

from models import Question, UserAnswer, WrongQuestion


def get_questions(
    db: Session,
    category: Optional[str] = None,
    difficulty: Optional[str] = None,
) -> List[Question]:
    query = db.query(Question)
    if category:
        query = query.filter(Question.category == category)
    if difficulty:
        query = query.filter(Question.difficulty == difficulty)
    return query.order_by(Question.id).all()


def get_question(db: Session, question_id: int) -> Optional[Question]:
    return db.query(Question).filter(Question.id == question_id).first()


def create_user_answer(db: Session, user_answer: UserAnswer) -> UserAnswer:
    db.add(user_answer)
    db.commit()
    db.refresh(user_answer)
    return user_answer


def get_user_answers_by_user(db: Session, user_id: int) -> List[UserAnswer]:
    return (
        db.query(UserAnswer)
        .options(joinedload(UserAnswer.question))
        .filter(UserAnswer.user_id == user_id)
        .order_by(UserAnswer.created_at.desc())
        .all()
    )


def add_wrong_question(db: Session, user_id: int, question_id: int) -> WrongQuestion:
    existing = (
        db.query(WrongQuestion)
        .filter(
            WrongQuestion.user_id == user_id,
            WrongQuestion.question_id == question_id,
        )
        .first()
    )
    if existing:
        return existing

    wrong = WrongQuestion(user_id=user_id, question_id=question_id)
    db.add(wrong)
    db.commit()
    db.refresh(wrong)
    return wrong


def get_wrong_questions_by_user(db: Session, user_id: int) -> List[WrongQuestion]:
    return (
        db.query(WrongQuestion)
        .options(joinedload(WrongQuestion.question))
        .filter(WrongQuestion.user_id == user_id)
        .order_by(WrongQuestion.created_at.desc())
        .all()
    )


def delete_wrong_question(db: Session, user_id: int, question_id: int) -> bool:
    wrong = (
        db.query(WrongQuestion)
        .filter(
            WrongQuestion.user_id == user_id,
            WrongQuestion.question_id == question_id,
        )
        .first()
    )
    if not wrong:
        return False
    db.delete(wrong)
    db.commit()
    return True


def count_user_answers(db: Session, user_id: int) -> int:
    return db.query(UserAnswer).filter(UserAnswer.user_id == user_id).count()


def count_wrong_questions(db: Session, user_id: int) -> int:
    return db.query(WrongQuestion).filter(WrongQuestion.user_id == user_id).count()
