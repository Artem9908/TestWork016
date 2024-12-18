from fastapi import APIRouter, Depends
from app.api.security import verify_api_key
from app.schemas import StatisticsOut
from app.services.statistics import get_statistics

router = APIRouter()

@router.get("/statistics", response_model=StatisticsOut)
def get_stats(_=Depends(verify_api_key)):
    return get_statistics()
