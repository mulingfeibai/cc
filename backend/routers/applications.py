from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from schemas import (
    ApplicationAnalyzeResponse,
    ApplicationCreate,
    ApplicationListResponse,
    ApplicationResponse,
)
from services import application_service
from utils.security import get_current_user

router = APIRouter(prefix="/api/applications", tags=["投递管理"])


@router.get("", response_model=ApplicationListResponse)
def list_applications(
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return application_service.list_applications(db, current_user, status)


@router.post("", response_model=ApplicationResponse, status_code=201)
def create_application(
    data: ApplicationCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return application_service.create_application(db, current_user, data)


@router.get("/{app_id}", response_model=ApplicationResponse)
def get_application(
    app_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return application_service.get_application(db, current_user, app_id)


@router.post("/{app_id}/analyze", response_model=ApplicationAnalyzeResponse)
def analyze_application(
    app_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return application_service.analyze_application(db, current_user, app_id)
