from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


# ---------- 认证相关 ----------

class UserRegister(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6, max_length=128)


class UserLogin(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    token: str
    username: str
    user_id: int


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    created_at: datetime


# ---------- 面试相关 ----------

class InterviewStartRequest(BaseModel):
    job_type: str = Field(..., min_length=1, max_length=100)
    difficulty: str = Field(..., min_length=1, max_length=20)


class InterviewStartResponse(BaseModel):
    session_id: int
    job_type: str
    difficulty: str
    status: str


class QuestionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    question: str


class AnswerSubmitRequest(BaseModel):
    question_id: int
    answer: str = Field(..., min_length=1)


class AnswerSubmitResponse(BaseModel):
    question_id: int
    score: float
    evaluation: str


class ReportItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    question: str
    answer: str
    evaluation: str
    score: float


class InterviewReportResponse(BaseModel):
    session_id: int
    job_type: str
    difficulty: str
    status: str
    total_score: Optional[float] = None
    questions: List[ReportItem]


class HistoryItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    job_type: str
    difficulty: str
    status: str
    score: Optional[float] = None
    created_at: datetime


class HistoryResponse(BaseModel):
    sessions: List[HistoryItem]
