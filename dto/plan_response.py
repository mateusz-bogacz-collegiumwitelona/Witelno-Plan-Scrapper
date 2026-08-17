from typing import List

from pydantic import BaseModel

class PlanResponse(BaseModel):
    day: str
    hour: str
    group: str
    subject: str
    teacher: str
    classroom: str
