from pydantic import BaseModel
from datetime import datetime

class Appointment(BaseModel):
    id: int
    user_id: int
    title: str
    description: str
    scheduled_time: datetime
    created_at: datetime
    updated_at: datetime
