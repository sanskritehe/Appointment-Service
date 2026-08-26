from pydantic import BaseModel
from typing import List

class AppointmentResponse(BaseModel):
    id: int
    user: str
    time: str
    status: str

class AppointmentsListResponse(BaseModel):
    data: List[AppointmentResponse]

