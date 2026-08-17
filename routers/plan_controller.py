from fastapi import APIRouter, HTTPException
from services.scrape_services import get_plan_async, get_plans_list_async

router = APIRouter(prefix="/api/plan")

@router.get("/list")
async def get_available_majors_async():
    try:
        return await get_plans_list_async()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@router.get("/")
async def get_major_plan_endpoint(major: str):
    try:
        return await get_plan_async(major)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")