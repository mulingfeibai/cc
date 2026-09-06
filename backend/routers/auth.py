from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from schemas import TokenResponse, UserLogin, UserRegister
from services import auth_service

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", response_model=TokenResponse)
def register(data: UserRegister, db: Session = Depends(get_db)):
    return auth_service.register(db, data)


@router.post("/login", response_model=TokenResponse)
def login(data: UserLogin, db: Session = Depends(get_db)):
    return auth_service.login(db, data)
