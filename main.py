from fastapi import FastAPI
import uvicorn
from routers.plan_controller import router as plan_router

app = FastAPI(title="Plan PWSZ API")

app.include_router(plan_router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)