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
