from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from schemas import DashboardStatsResponse
from services import dashboard_service
from utils.security import get_current_user

router = APIRouter(prefix="/api/dashboard", tags=["仪表盘"])


@router.get("/stats", response_model=DashboardStatsResponse)
def stats(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return dashboard_service.get_stats(db, current_user)
