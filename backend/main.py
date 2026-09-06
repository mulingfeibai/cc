from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import init_db
from seed import seed_data
from routers import (
    applications,
    auth,
    dashboard,
    interviews,
    jobs,
    questions,
    resumes,
)

# 启动时初始化数据库并预置种子数据
init_db()
seed_data()

app = FastAPI(title="AI求职辅助平台", version="1.0.0")

# CORS：允许前端开发服务器跨域访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(jobs.router)
app.include_router(resumes.router)
app.include_router(applications.router)
app.include_router(interviews.router)
app.include_router(questions.router)
app.include_router(dashboard.router)


@app.get("/")
def root():
    return {"message": "AI求职辅助平台后端服务运行中"}
