from typing import List, Optional

from sqlalchemy import or_
from sqlalchemy.orm import Session, joinedload

from models import Job


def get_jobs(
    db: Session,
    company_id: Optional[int] = None,
    job_type: Optional[str] = None,
    keyword: Optional[str] = None,
) -> List[Job]:
    query = db.query(Job).options(joinedload(Job.company))

    if company_id is not None:
        query = query.filter(Job.company_id == company_id)
    if job_type:
        query = query.filter(Job.job_type == job_type)
    if keyword:
        like = f"%{keyword}%"
        query = query.filter(or_(Job.title.like(like), Job.requirement.like(like)))

    return query.order_by(Job.id).all()


def get_job(db: Session, job_id: int) -> Optional[Job]:
    return (
        db.query(Job)
        .options(joinedload(Job.company))
        .filter(Job.id == job_id)
        .first()
    )
