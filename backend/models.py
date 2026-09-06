from datetime import datetime

from sqlalchemy import (
    JSON,
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    resumes = relationship("Resume", back_populates="user")
    applications = relationship("Application", back_populates="user")
    user_answers = relationship("UserAnswer", back_populates="user")
    wrong_questions = relationship("WrongQuestion", back_populates="user")


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    industry = Column(String, nullable=True)
    logo_url = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    jobs = relationship("Job", back_populates="company")


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    title = Column(String, nullable=False)
    job_type = Column(String, nullable=False)
    requirement = Column(Text, nullable=True)
    salary = Column(String, nullable=True)
    location = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    company = relationship("Company", back_populates="jobs")
    applications = relationship("Application", back_populates="job")


class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    target_job = Column(String, nullable=True)
    basic_info = Column(JSON, nullable=True)
    education = Column(JSON, nullable=True)
    experience = Column(JSON, nullable=True)
    projects = Column(JSON, nullable=True)
    skills = Column(Text, nullable=True)
    self_intro = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="resumes")
    applications = relationship("Application", back_populates="resume")


class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    resume_id = Column(Integer, ForeignKey("resumes.id"), nullable=False)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)
    # 状态：待反馈 / 面试中 / 已通过 / 已拒绝
    status = Column(String, default="待反馈", nullable=False)
    result_analysis = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="applications")
    resume = relationship("Resume", back_populates="applications")
    job = relationship("Job", back_populates="applications")
    interviews = relationship("Interview", back_populates="application")


class Interview(Base):
    __tablename__ = "interviews"

    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("applications.id"), nullable=False)
    interview_time = Column(DateTime, nullable=True)
    # 形式：电话 / 视频 / 现场
    form = Column(String, default="视频", nullable=False)
    interviewer = Column(String, nullable=True)
    questions = Column(JSON, nullable=True)
    notes = Column(Text, nullable=True)
    # 结果：待结果 / 已通过 / 未通过
    result = Column(String, default="待结果", nullable=False)
    review = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    application = relationship("Application", back_populates="interviews")


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    # 题型：选择 / 简答
    question_type = Column(String, nullable=False)
    # 分类：公共 / Java / 前端 / 算法 / 测试 / 产品
    category = Column(String, nullable=False)
    title = Column(Text, nullable=False)
    options = Column(JSON, nullable=True)
    answer = Column(Text, nullable=True)
    analysis = Column(Text, nullable=True)
    # 难度：简单 / 中等 / 困难
    difficulty = Column(String, default="简单", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user_answers = relationship("UserAnswer", back_populates="question")
    wrong_questions = relationship("WrongQuestion", back_populates="question")


class UserAnswer(Base):
    __tablename__ = "user_answers"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    user_answer = Column(Text, nullable=True)
    is_correct = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="user_answers")
    question = relationship("Question", back_populates="user_answers")


class WrongQuestion(Base):
    __tablename__ = "wrong_questions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="wrong_questions")
    question = relationship("Question", back_populates="wrong_questions")
