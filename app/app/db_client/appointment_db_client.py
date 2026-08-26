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
