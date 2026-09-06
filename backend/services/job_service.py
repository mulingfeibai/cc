from typing import List

from fastapi import HTTPException
from sqlalchemy.orm import Session

from models import User
from repositories import job_repository, resume_repository
from schemas import (
    JobListResponse,
    JobMatchRequest,
    JobMatchResponse,
    JobResponse,
)

# 用于匹配的技能关键词
SKILL_KEYWORDS = [
    "Java", "Python", "JavaScript", "TypeScript", "HTML", "CSS", "Vue", "React",
    "Node", "Spring", "MySQL", "Redis", "SQL", "数据库", "算法", "数据结构",
    "机器学习", "深度学习", "测试", "自动化测试", "Linux", "Git", "Docker",
    "Kubernetes", "分布式", "网络", "操作系统", "前端", "后端", "微服务", "消息队列",
]


def list_jobs(
    db: Session,
    company_id: int = None,
    job_type: str = None,
    keyword: str = None,
) -> JobListResponse:
    jobs = job_repository.get_jobs(db, company_id, job_type, keyword)
    return JobListResponse(
        items=[JobResponse.model_validate(j) for j in jobs],
        total=len(jobs),
    )


def get_job(db: Session, job_id: int) -> JobResponse:
    job = job_repository.get_job(db, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="岗位不存在")
    return JobResponse.model_validate(job)


def _resume_to_text(resume) -> str:
    parts = [resume.skills or "", resume.self_intro or "", resume.target_job or ""]
    for field in (resume.education, resume.experience, resume.projects):
        if field:
            parts.append(str(field))
    return " ".join(parts)


def _build_match_analysis(score: float, matched: List[str], missing: List[str]) -> str:
    if score >= 80:
        head = "你的技能与岗位高度匹配，具备较强的竞争力，建议尽快投递。"
    elif score >= 60:
        head = "你的技能与岗位基本匹配，但仍有提升空间。"
    else:
        head = "你的技能与岗位匹配度较低，建议先补齐核心技能后再投递。"

    parts = [head]
    if matched:
        parts.append(f"已匹配技能：{'、'.join(matched)}。")
    if missing:
        parts.append(f"技能差距：{'、'.join(missing)}，建议通过学习或项目实践补齐。")
    return "".join(parts)


def match_resume(
    db: Session,
    current_user: User,
    job_id: int,
    data: JobMatchRequest,
) -> JobMatchResponse:
    job = job_repository.get_job(db, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="岗位不存在")

    resume = resume_repository.get_resume(db, data.resume_id)
    if not resume or resume.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="简历不存在")

    job_text = f"{job.title} {job.requirement or ''}"
    resume_text = _resume_to_text(resume)

    required = [k for k in SKILL_KEYWORDS if k.lower() in job_text.lower()]
    matched = [k for k in required if k.lower() in resume_text.lower()]
    missing = [k for k in required if k not in matched]

    match_score = round(len(matched) / len(required) * 100, 1) if required else 0.0

    return JobMatchResponse(
        job_id=job.id,
        resume_id=resume.id,
        match_score=match_score,
        matched_skills=matched,
        missing_skills=missing,
        analysis=_build_match_analysis(match_score, matched, missing),
    )
