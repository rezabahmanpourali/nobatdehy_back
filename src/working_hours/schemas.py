from pydantic import BaseModel
from typing import Optional, List
from datetime import time

class WorkingHoursBase(BaseModel):
    day_of_week: str
    start_time: time
    end_time: time

class WorkingHoursCreate(WorkingHoursBase):
    barber_id: Optional[int] = None
    shop_id: Optional[int] = None

class WorkingHoursUpdate(WorkingHoursBase):
    pass

class WorkingHours(WorkingHoursBase):
    id: int

    class Config:
        from_attributes = True
