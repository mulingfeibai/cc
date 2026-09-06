from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


# ================= 通用 =================

class MessageResponse(BaseModel):
    detail: str


# ================= 认证 =================

class UserRegister(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6, max_length=128)
    email: str = Field(..., pattern=r"^\S+@\S+\.\S+$")


class UserLogin(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    token: str
    username: str
    user_id: int


# ================= 公司 / 岗位 =================

class CompanyResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: Optional[str] = None
    industry: Optional[str] = None
    logo_url: Optional[str] = None
    created_at: datetime


class JobResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    company_id: int
    title: str
    job_type: str
    requirement: Optional[str] = None
    salary: Optional[str] = None
    location: Optional[str] = None
    created_at: datetime
    company: Optional[CompanyResponse] = None


class JobListResponse(BaseModel):
    items: List[JobResponse]
    total: int


class JobMatchRequest(BaseModel):
    resume_id: int


class JobMatchResponse(BaseModel):
    job_id: int
    resume_id: int
    match_score: float
    matched_skills: List[str]
    missing_skills: List[str]
    analysis: str


# ================= 简历 =================

class ResumeCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    target_job: Optional[str] = None
    basic_info: Optional[Dict[str, Any]] = None
    education: Optional[List[Any]] = None
    experience: Optional[List[Any]] = None
    projects: Optional[List[Any]] = None
    skills: Optional[str] = None
    self_intro: Optional[str] = None


class ResumeUpdate(BaseModel):
    name: Optional[str] = None
    target_job: Optional[str] = None
    basic_info: Optional[Dict[str, Any]] = None
    education: Optional[List[Any]] = None
    experience: Optional[List[Any]] = None
    projects: Optional[List[Any]] = None
    skills: Optional[str] = None
    self_intro: Optional[str] = None


class ResumeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    name: str
    target_job: Optional[str] = None
    basic_info: Optional[Dict[str, Any]] = None
    education: Optional[List[Any]] = None
    experience: Optional[List[Any]] = None
    projects: Optional[List[Any]] = None
    skills: Optional[str] = None
    self_intro: Optional[str] = None
    created_at: datetime


class ResumeListResponse(BaseModel):
    items: List[ResumeResponse]
    total: int


class ResumeOptimizeResponse(BaseModel):
    resume_id: int
    score: int
    suggestions: List[str]


# ================= 投递管理 =================

class ApplicationCreate(BaseModel):
    resume_id: int
    job_id: int


class ApplicationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    resume_id: int
    job_id: int
    status: str
    result_analysis: Optional[str] = None
    created_at: datetime


class ApplicationListResponse(BaseModel):
    items: List[ApplicationResponse]
    total: int


class ApplicationAnalyzeResponse(BaseModel):
    application_id: int
    status: str
    analysis: str
    suggestions: List[str]


# ================= 面试记录 =================

class InterviewResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    application_id: int
    interview_time: Optional[datetime] = None
    form: str
    interviewer: Optional[str] = None
    questions: Optional[List[Any]] = None
    notes: Optional[str] = None
    result: str
    review: Optional[str] = None
    created_at: datetime


class InterviewListResponse(BaseModel):
    items: List[InterviewResponse]
    total: int


class InterviewReviewResponse(BaseModel):
    interview_id: int
    result: str
    review: str
    suggestions: List[str]


# ================= 题库 =================

class QuestionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    question_type: str
    category: str
    title: str
    options: Optional[List[Any]] = None
    answer: Optional[str] = None
    analysis: Optional[str] = None
    difficulty: str
    created_at: datetime


class QuestionListResponse(BaseModel):
    items: List[QuestionResponse]
    total: int


class AnswerSubmitRequest(BaseModel):
    question_id: int
    user_answer: str


class AnswerSubmitResponse(BaseModel):
    question_id: int
    is_correct: bool
    correct_answer: str
    analysis: str


class WrongQuestionItem(BaseModel):
    question_id: int
    created_at: datetime
    question: QuestionResponse


class WrongQuestionListResponse(BaseModel):
    items: List[WrongQuestionItem]
    total: int


class AnswerHistoryItem(BaseModel):
    id: int
    question_id: int
    user_answer: str
    is_correct: bool
    created_at: datetime
    question: QuestionResponse


class AnswerHistoryResponse(BaseModel):
    items: List[AnswerHistoryItem]
    total: int


# ================= 仪表盘 =================

class DashboardStatsResponse(BaseModel):
    total_resumes: int
    total_applications: int
    total_interviews: int
    pass_rate: float
    total_questions_answered: int
    total_wrong_questions: int
    application_status_breakdown: Dict[str, int]
