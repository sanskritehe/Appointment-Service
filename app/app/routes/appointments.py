from fastapi import APIRouter, HTTPException, Depends, Path
from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime

from app.services.appointment_service import AppointmentService

router = APIRouter()

# Request and Response Models
class AppointmentUpdateRequest(BaseModel):
    time: datetime = Field(..., description="The new time for the appointment", example="2026-03-01T11:00:00")

    @validator("time")
    def validate_time_format(cls, value: datetime):
        if not isinstance(value, datetime):
            raise ValueError("Invalid date/time format")
        return value

class AppointmentResponse(BaseModel):
    id: int
    user: str
    time: datetime


@router.put('/appointments/{appointment_id}', response_model=AppointmentResponse, name="update_appointment", status_code=200)
async def update_appointment(
    appointment_id: int = Path(..., description="The ID of the appointment to update", gt=0),
    update_data: AppointmentUpdateRequest = ...,
    appointment_service: AppointmentService = Depends()
):
    """
    Update the scheduled time of an existing appointment.
    
    Parameters:
        - appointment_id: The ID of the appointment to update
        - update_data: New appointment time
        
    Returns:
        - Updated appointment details
        - 404 error if the appointment is not found

    Response Codes:
        - 200: Success, appointment updated
        - 404: Appointment not found
    """
    updated_appointment = await appointment_service.update_appointment(appointment_id, update_data.time)
    if updated_appointment is None:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return AppointmentResponse(
        id=updated_appointment.id,
        user=updated_appointment.user,
        time=updated_appointment.time
    )
