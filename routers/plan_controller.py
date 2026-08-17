from fastapi import APIRouter, HTTPException
from services.scrape_services import get_plan, get_plans_list

router = APIRouter(prefix="/api/plan")

@router.get("/list")
async def get_available_majors():
    try:
        return await get_plans_list()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@router.get("/")
def get_plan_endpoint(major: str):
    try:
        return get_plan(major)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")