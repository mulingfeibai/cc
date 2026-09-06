import base64

from fastapi import Depends, Header, HTTPException
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from database import get_db
from models import User
from repositories.user_repository import get_user_by_id

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
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=401, detail="用户不存在")
    return user
