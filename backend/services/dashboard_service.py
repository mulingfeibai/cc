from sqlalchemy.orm import Session

from models import User
from repositories import (
    application_repository,
    interview_repository,
    question_repository,
    resume_repository,
)
from schemas import DashboardStatsResponse


def get_stats(db: Session, current_user: User) -> DashboardStatsResponse:
    breakdown = application_repository.get_application_status_breakdown(
        db, current_user.id
    )

    total_applications = sum(breakdown.values())
    passed = breakdown.get("已通过", 0)
    pass_rate = round(passed / total_applications * 100, 1) if total_applications else 0.0

    return DashboardStatsResponse(
        total_resumes=resume_repository.count_resumes_by_user(db, current_user.id),
        total_applications=total_applications,
        total_interviews=interview_repository.count_interviews_by_user(db, current_user.id),
        pass_rate=pass_rate,
        total_questions_answered=question_repository.count_user_answers(db, current_user.id),
        total_wrong_questions=question_repository.count_wrong_questions(db, current_user.id),
        application_status_breakdown=breakdown,
    )
