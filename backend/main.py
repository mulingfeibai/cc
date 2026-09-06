from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import Base, engine
from models import InterviewQuestion, InterviewSession, User  # noqa: F401
from routers import auth, interview

# 启动时自动建表
Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI面试系统", version="0.1.0")

# CORS：允许前端开发服务器跨域访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(interview.router)


@app.get("/")
def root():
    return {"message": "AI面试系统后端服务运行中"}
