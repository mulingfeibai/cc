import random
from typing import Tuple

from fastapi import HTTPException
from sqlalchemy.orm import Session

from models import InterviewQuestion, InterviewSession, User
from schemas import (
    AnswerSubmitRequest,
    AnswerSubmitResponse,
    HistoryItem,
    HistoryResponse,
    InterviewReportResponse,
    InterviewStartRequest,
    InterviewStartResponse,
    QuestionResponse,
    ReportItem,
)

# 每场面试的题目数量
MAX_QUESTIONS = 5

# 模拟题库（占位符 {job_type} / {difficulty} 会替换为实际值）
MOCK_QUESTIONS = [
    "请简单介绍一下你自己，以及你在{job_type}方向的相关经验。",
    "请描述一个你在{job_type}方向最具挑战性的项目，并说明你的具体贡献。",
    "在{difficulty}难度要求下，你通常如何规划并拆解一项复杂任务？",
    "请谈谈你在{job_type}岗位中最擅长的一项技能，以及如何将其应用到实际工作中。",
    "当你面对一个陌生的技术难题时，你的排查与解决思路是什么？",
    "请分享一次你在团队协作中处理意见分歧的经历。",
    "你平时如何保持技术学习，跟进{job_type}领域的最新动态？",
    "对于{job_type}岗位，你认为自己最大的优势和不足分别是什么？",
]


def _get_session(db: Session, user: User, session_id: int) -> InterviewSession:
    """获取当前用户拥有的面试会话，不存在则抛 404。"""
    session = (
        db.query(InterviewSession)
        .filter(
            InterviewSession.id == session_id,
            InterviewSession.user_id == user.id,
        )
        .first()
    )
    if not session:
        raise HTTPException(status_code=404, detail="面试会话不存在")
    return session


def call_deepseek(question: str, answer: str):
    """
    预留接口：接入 DeepSeek 大模型，对回答进行真实 AI 评估。

    后续在此实现：
    1. 读取环境变量中的 API Key（如 DEEPSEEK_API_KEY）
    2. 调用 DeepSeek Chat Completions 接口
    3. 解析返回的结构化评估结果（分数 + 评语）

    当前直接返回 None，由 evaluate_answer 回退到模拟数据。
    """
    return None


def evaluate_answer(question: str, answer: str) -> Tuple[float, str]:
    """评估回答：优先走真实 AI，未接入时返回模拟数据。"""
    result = call_deepseek(question, answer)
    if result:
        return float(result["score"]), str(result["evaluation"])

    score = round(random.uniform(60, 95), 1)
    evaluation = (
        f"【模拟评估】针对问题「{question}」，你的回答内容较为完整、"
        f"逻辑清晰，能够结合要点展开说明。本次模拟得分 {score} 分。"
        f"（当前为模拟评估，接入 DeepSeek 后将返回更真实的 AI 分析。）"
    )
    return score, evaluation


def start_interview(
    db: Session,
    user: User,
    data: InterviewStartRequest,
) -> InterviewStartResponse:
    session = InterviewSession(
        user_id=user.id,
        job_type=data.job_type,
        difficulty=data.difficulty,
        status="in_progress",
    )
    db.add(session)
    db.commit()
    db.refresh(session)

    return InterviewStartResponse(
        session_id=session.id,
        job_type=session.job_type,
        difficulty=session.difficulty,
        status=session.status,
    )


def get_next_question(
    db: Session,
    user: User,
    session_id: int,
) -> QuestionResponse:
    session = _get_session(db, user, session_id)

    # 若存在未回答的题目，直接返回
    unanswered = (
        db.query(InterviewQuestion)
        .filter(
            InterviewQuestion.session_id == session.id,
            InterviewQuestion.answer.is_(None),
        )
        .first()
    )
    if unanswered:
        return QuestionResponse(id=unanswered.id, question=unanswered.question)

    answered_count = (
        db.query(InterviewQuestion)
        .filter(
            InterviewQuestion.session_id == session.id,
            InterviewQuestion.answer.isnot(None),
        )
        .count()
    )

    # 已答满全部题目，标记会话完成
    if answered_count >= MAX_QUESTIONS:
        session.status = "completed"
        db.commit()
        raise HTTPException(status_code=400, detail="面试已完成，请查看面试报告")

    question_text = MOCK_QUESTIONS[answered_count % len(MOCK_QUESTIONS)].format(
        job_type=session.job_type,
        difficulty=session.difficulty,
    )
    question = InterviewQuestion(
        session_id=session.id,
        question=question_text,
    )
    db.add(question)
    db.commit()
    db.refresh(question)

    return QuestionResponse(id=question.id, question=question.question)


def submit_answer(
    db: Session,
    user: User,
    session_id: int,
    data: AnswerSubmitRequest,
) -> AnswerSubmitResponse:
    session = _get_session(db, user, session_id)

    question = (
        db.query(InterviewQuestion)
        .filter(
            InterviewQuestion.id == data.question_id,
            InterviewQuestion.session_id == session.id,
        )
        .first()
    )
    if not question:
        raise HTTPException(status_code=404, detail="面试题目不存在")
    if question.answer is not None:
        raise HTTPException(status_code=400, detail="该题目已提交过回答")

    score, evaluation = evaluate_answer(question.question, data.answer)

    question.answer = data.answer
    question.evaluation = evaluation
    question.score = score
    db.commit()
    db.refresh(question)

    _update_session_score(db, session)

    return AnswerSubmitResponse(
        question_id=question.id,
        score=score,
        evaluation=evaluation,
    )


def _update_session_score(db: Session, session: InterviewSession) -> None:
    """根据已答题目更新会话平均分，并判断是否完成。"""
    answered = (
        db.query(InterviewQuestion)
        .filter(
            InterviewQuestion.session_id == session.id,
            InterviewQuestion.answer.isnot(None),
        )
        .all()
    )
    if answered:
        session.score = round(
            sum(q.score or 0 for q in answered) / len(answered),
            1,
        )
    if len(answered) >= MAX_QUESTIONS:
        session.status = "completed"
    db.commit()


def get_report(
    db: Session,
    user: User,
    session_id: int,
) -> InterviewReportResponse:
    session = _get_session(db, user, session_id)

    questions = (
        db.query(InterviewQuestion)
        .filter(InterviewQuestion.session_id == session.id)
        .order_by(InterviewQuestion.id)
        .all()
    )

    report_items = [
        ReportItem(
            id=q.id,
            question=q.question,
            answer=q.answer or "",
            evaluation=q.evaluation or "",
            score=q.score or 0,
        )
        for q in questions
    ]

    return InterviewReportResponse(
        session_id=session.id,
        job_type=session.job_type,
        difficulty=session.difficulty,
        status=session.status,
        total_score=session.score,
        questions=report_items,
    )


def get_history(db: Session, user: User) -> HistoryResponse:
    sessions = (
        db.query(InterviewSession)
        .filter(InterviewSession.user_id == user.id)
        .order_by(InterviewSession.created_at.desc())
        .all()
    )

    items = [
        HistoryItem(
            id=s.id,
            job_type=s.job_type,
            difficulty=s.difficulty,
            status=s.status,
            score=s.score,
            created_at=s.created_at,
        )
        for s in sessions
    ]
    return HistoryResponse(sessions=items)
