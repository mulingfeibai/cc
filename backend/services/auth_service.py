from fastapi import HTTPException
from sqlalchemy.orm import Session

from models import User
from repositories import user_repository
from schemas import TokenResponse, UserLogin, UserRegister
from utils.security import generate_token, hash_password, verify_password


def register(db: Session, data: UserRegister) -> TokenResponse:
    if user_repository.get_user_by_username(db, data.username):
        raise HTTPException(status_code=400, detail="用户名已存在")
    if user_repository.get_user_by_email(db, data.email):
        raise HTTPException(status_code=400, detail="邮箱已被注册")

    user = User(
        username=data.username,
        email=data.email,
        password_hash=hash_password(data.password),
    )
    user = user_repository.create_user(db, user)

    return TokenResponse(
        token=generate_token(user),
        username=user.username,
        user_id=user.id,
    )


def login(db: Session, data: UserLogin) -> TokenResponse:
    user = user_repository.get_user_by_username(db, data.username)
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="用户名或密码错误")

    return TokenResponse(
        token=generate_token(user),
        username=user.username,
        user_id=user.id,
    )
