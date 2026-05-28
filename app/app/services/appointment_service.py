from app.db_client.appointment_db_client import AppointmentDBClient
from app.models.appointment import Appointment

class AppointmentService:
    def __init__(self, db_client: AppointmentDBClient):
        self.db_client = db_client

    async def get_all_appointments(self) -> list[Appointment]:
        """
        Fetch all appointments using db client.

        Returns:
            List of Appointment objects or empty list.
        """
        return await self.db_client.fetch_all_appointments()
