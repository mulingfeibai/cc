from typing import List, Tuple

from fastapi import HTTPException
from sqlalchemy.orm import Session

from models import Application, User
from repositories import application_repository, job_repository, resume_repository
from schemas import (
    ApplicationAnalyzeResponse,
    ApplicationCreate,
    ApplicationListResponse,
    ApplicationResponse,
)


def list_applications(
    db: Session,
    current_user: User,
    status: str = None,
) -> ApplicationListResponse:
    items = application_repository.get_applications_by_user(db, current_user.id, status)
    return ApplicationListResponse(
        items=[ApplicationResponse.model_validate(a) for a in items],
        total=len(items),
    )


def create_application(
    db: Session,
    current_user: User,
    data: ApplicationCreate,
) -> ApplicationResponse:
    resume = resume_repository.get_resume(db, data.resume_id)
    if not resume or resume.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="简历不存在")
    if not job_repository.get_job(db, data.job_id):
        raise HTTPException(status_code=404, detail="岗位不存在")

    application = Application(
        user_id=current_user.id,
        resume_id=data.resume_id,
        job_id=data.job_id,
        status="待反馈",
    )
    application = application_repository.create_application(db, application)
    return ApplicationResponse.model_validate(application)


def _get_owned_application(db: Session, user_id: int, app_id: int) -> Application:
    application = application_repository.get_application(db, app_id)
    if not application or application.user_id != user_id:
        raise HTTPException(status_code=404, detail="投递记录不存在")
    return application


def get_application(db: Session, current_user: User, app_id: int) -> ApplicationResponse:
    application = _get_owned_application(db, current_user.id, app_id)
    return ApplicationResponse.model_validate(application)


def _suggestions_for_status(status: str) -> Tuple[str, List[str]]:
    if status == "面试中":
        return "当前已进入面试环节，重点做好面试准备。", [
            "针对岗位要求准备一份 1-2 分钟的自我介绍。",
            "复习简历中提到的项目细节，准备被追问。",
            "准备 2-3 个想问面试官的问题。",
        ]
    if status == "已通过":
        return "恭喜通过面试！请及时跟进后续流程。", [
            "确认入职时间、薪资待遇与合同细节。",
            "了解公司文化与团队情况，做好入职准备。",
            "保留好面试中的沟通记录。",
        ]
    if status == "已拒绝":
        return "本次投递未通过，建议复盘并针对性改进。", [
            "对照岗位要求分析自身差距，查漏补缺。",
            "优化简历，突出与目标岗位匹配的经历与技能。",
            "补充技能短板后再次投递，不要气馁。",
            "适当扩大投递范围，不要局限于单一岗位。",
        ]
    return "投递已提交，正在等待反馈。", [
        "投递后通常 3-7 个工作日会有反馈，请耐心等待。",
        "同步准备面试，复习岗位相关知识点。",
        "关注招聘平台的进度更新，必要时主动跟进。",
    ]


def analyze_application(
    db: Session,
    current_user: User,
    app_id: int,
) -> ApplicationAnalyzeResponse:
    application = _get_owned_application(db, current_user.id, app_id)
    analysis, suggestions = _suggestions_for_status(application.status)

    application.result_analysis = analysis
    application_repository.update_application(db, application)

    return ApplicationAnalyzeResponse(
        application_id=application.id,
        status=application.status,
        analysis=analysis,
        suggestions=suggestions,
    )
