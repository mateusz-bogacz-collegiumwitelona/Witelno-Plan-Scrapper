from fastapi import APIRouter, HTTPException
from services.scrape_services import get_plan

router = APIRouter(prefix="/api/plan")

@router.get("/")
def get_plan_endpoint(major: str):
    try:
        return get_plan(major)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")