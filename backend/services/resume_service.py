from fastapi import HTTPException
from sqlalchemy.orm import Session

from models import Resume, User
from repositories import resume_repository
from schemas import (
    MessageResponse,
    ResumeCreate,
    ResumeListResponse,
    ResumeOptimizeResponse,
    ResumeResponse,
    ResumeUpdate,
)


def _get_owned_resume(db: Session, user_id: int, resume_id: int) -> Resume:
    resume = resume_repository.get_resume(db, resume_id)
    if not resume or resume.user_id != user_id:
        raise HTTPException(status_code=404, detail="简历不存在")
    return resume


def list_resumes(db: Session, current_user: User) -> ResumeListResponse:
    resumes = resume_repository.get_resumes_by_user(db, current_user.id)
    return ResumeListResponse(
        items=[ResumeResponse.model_validate(r) for r in resumes],
        total=len(resumes),
    )


def create_resume(db: Session, current_user: User, data: ResumeCreate) -> ResumeResponse:
    resume = Resume(
        user_id=current_user.id,
        name=data.name,
        target_job=data.target_job,
        basic_info=data.basic_info,
        education=data.education,
        experience=data.experience,
        projects=data.projects,
        skills=data.skills,
        self_intro=data.self_intro,
    )
    resume = resume_repository.create_resume(db, resume)
    return ResumeResponse.model_validate(resume)


def get_resume(db: Session, current_user: User, resume_id: int) -> ResumeResponse:
    resume = _get_owned_resume(db, current_user.id, resume_id)
    return ResumeResponse.model_validate(resume)


def update_resume(
    db: Session,
    current_user: User,
    resume_id: int,
    data: ResumeUpdate,
) -> ResumeResponse:
    resume = _get_owned_resume(db, current_user.id, resume_id)
    resume = resume_repository.update_resume(
        db, resume, data.model_dump(exclude_unset=True)
    )
    return ResumeResponse.model_validate(resume)


def delete_resume(db: Session, current_user: User, resume_id: int) -> MessageResponse:
    resume = _get_owned_resume(db, current_user.id, resume_id)
    resume_repository.delete_resume(db, resume)
    return MessageResponse(detail="简历删除成功")


def optimize_resume(
    db: Session,
    current_user: User,
    resume_id: int,
) -> ResumeOptimizeResponse:
    resume = _get_owned_resume(db, current_user.id, resume_id)

    suggestions = []
    if not resume.projects:
        suggestions.append("缺少项目经历，建议补充 2-3 个能体现技术能力的项目。")
    if not resume.experience:
        suggestions.append("缺少实习/工作经历描述，建议补充相关经历。")
    if not resume.skills or len(resume.skills) < 20:
        suggestions.append("技能列表过于简略，建议列出具体技术栈（语言、框架、工具）。")
    if not resume.self_intro or len(resume.self_intro) < 50:
        suggestions.append("自我介绍过于简短，建议补充个人亮点与求职意向。")
    if not resume.target_job:
        suggestions.append("缺少目标岗位，建议明确求职方向。")
    if not resume.education:
        suggestions.append("缺少教育背景，建议补充学校、专业、学历信息。")

    experience_text = str(resume.experience or "") + str(resume.projects or "")
    if experience_text and not any(ch.isdigit() for ch in experience_text):
        suggestions.append("经历描述缺少量化数据，建议用具体数字体现成果（如性能提升 30%）。")

    issue_count = len(suggestions)
    if issue_count == 0:
        suggestions.append("简历整体完整度较高，继续保持并及时更新最新经历。")

    score = max(0, 100 - 12 * issue_count)

    return ResumeOptimizeResponse(
        resume_id=resume.id,
        score=score,
        suggestions=suggestions,
    )
