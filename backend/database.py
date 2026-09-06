from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import declarative_base, sessionmaker

# SQLite 数据库文件路径（相对当前运行目录）
SQLALCHEMY_DATABASE_URL = "sqlite:///./interview.db"

# check_same_thread=False 允许 FastAPI 多线程环境下访问 SQLite
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def init_db():
    """初始化数据库：若检测到旧版表结构（如 users 缺少 email 列）则自动重建。"""
    inspector = inspect(engine)
    tables = inspector.get_table_names()

    if "users" in tables:
        columns = {c["name"] for c in inspector.get_columns("users")}
        if "email" not in columns:
            Base.metadata.drop_all(bind=engine)

    Base.metadata.create_all(bind=engine)


def get_db():
    """FastAPI 依赖：提供数据库会话，请求结束后自动关闭。"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
