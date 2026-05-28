### FILE: app/db_client/appointment_db_client.py
```python
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.appointment_model import Appointment


class AppointmentDBClient:
    def __init__(self):
        pass

    async def get_by_id(self, db_session: AsyncSession, appointment_id: int) -> Optional[Appointment]:
        """
        Retrieve an appointment by its ID.
        """
        result = await db_session.execute(select(Appointment).where(Appointment.id == appointment_id))
        return result.scalars().first()

    async def save(self, db_session: AsyncSession, appointment: Appointment) -> None:
        """
        Save changes to an appointment.
        """
        db_session.add(appointment)
        await db_session.commit()
        await db_session.refresh(appointment)
```

### FILE: app/routes/appointments.py
```python
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
```

### FILE: app/services/appointment_service.py
```python
from typing import Optional
from datetime import datetime

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.db_client.appointment_db_client import AppointmentDBClient
from app.models.appointment_model import Appointment


class AppointmentService:
    def __init__(self, appointment_db_client: AppointmentDBClient = Depends()):
        self.appointment_db_client = appointment_db_client

    async def update_appointment(self, appointment_id: int, new_time: datetime, db_session: AsyncSession = Depends(get_db)) -> Optional[Appointment]:
        """
        Updates the time of an appointment if it exists.
        Returns the updated appointment object if successful, or None if not found.
        """
        appointment = await self.appointment_db_client.get_by_id(db_session, appointment_id)
        if appointment is None:
            return None

        # Update appointment time
        appointment.time = new_time
        await self.appointment_db_client.save(db_session, appointment)
        return appointment
```