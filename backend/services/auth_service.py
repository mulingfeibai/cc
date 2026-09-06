import base64

from fastapi import Depends, Header, HTTPException
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from database import get_db
from models import User
from schemas import TokenResponse, UserLogin, UserRegister

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def generate_token(user: User) -> str:
    """生成简单 token：base64 编码 "user_id:username"。"""
    raw = f"{user.id}:{user.username}"
    return base64.urlsafe_b64encode(raw.encode("utf-8")).decode("utf-8")


def decode_token(token: str) -> int:
    """解码 token，返回 user_id。"""
    try:
        raw = base64.urlsafe_b64decode(token.encode("utf-8")).decode("utf-8")
        return int(raw.split(":")[0])
    except Exception:
        raise HTTPException(status_code=401, detail="无效的 token")


def get_current_user(
    authorization: str = Header(default=None),
    db: Session = Depends(get_db),
) -> User:
    """从 Authorization: Bearer <token> 中解析当前登录用户。"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="未提供认证信息")
    token = authorization[len("Bearer "):]
    user_id = decode_token(token)
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="用户不存在")
    return user


def register(db: Session, data: UserRegister) -> TokenResponse:
    existing = db.query(User).filter(User.username == data.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="用户名已存在")

    user = User(
        username=data.username,
        password_hash=hash_password(data.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return TokenResponse(
        token=generate_token(user),
        username=user.username,
        user_id=user.id,
    )


def login(db: Session, data: UserLogin) -> TokenResponse:
    user = db.query(User).filter(User.username == data.username).first()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="用户名或密码错误")

    return TokenResponse(
        token=generate_token(user),
        username=user.username,
        user_id=user.id,
    )
