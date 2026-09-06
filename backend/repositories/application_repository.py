from typing import Dict, List, Optional

from sqlalchemy import func
from sqlalchemy.orm import Session

from models import Application

# 投递状态全集
APPLICATION_STATUSES = ["待反馈", "面试中", "已通过", "已拒绝"]


def get_applications_by_user(
    db: Session,
    user_id: int,
    status: Optional[str] = None,
) -> List[Application]:
    query = db.query(Application).filter(Application.user_id == user_id)
    if status:
        query = query.filter(Application.status == status)
    return query.order_by(Application.created_at.desc()).all()


def get_application(db: Session, app_id: int) -> Optional[Application]:
    return db.query(Application).filter(Application.id == app_id).first()


def create_application(db: Session, application: Application) -> Application:
    db.add(application)
    db.commit()
    db.refresh(application)
    return application


def update_application(db: Session, application: Application) -> Application:
    db.commit()
    db.refresh(application)
    return application


def count_applications_by_user(db: Session, user_id: int) -> int:
    return db.query(Application).filter(Application.user_id == user_id).count()


def get_application_status_breakdown(db: Session, user_id: int) -> Dict[str, int]:
    rows = (
        db.query(Application.status, func.count(Application.id))
        .filter(Application.user_id == user_id)
        .group_by(Application.status)
        .all()
    )
    result = {s: 0 for s in APPLICATION_STATUSES}
    for status, count in rows:
        result[status] = count
    return result
