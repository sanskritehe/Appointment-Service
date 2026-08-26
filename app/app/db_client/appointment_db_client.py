from typing import List
from app.models.appointment import Appointment

class AppointmentDBClient:
    def __init__(self, database):
        self.database = database

    async def fetch_all_appointments(self) -> List[Appointment]:
        """
        Fetch all appointments from the database.

        Returns:
            List of Appointment objects.
        """
        query = "SELECT * FROM appointments"
        rows = await self.database.fetch_all(query=query)
        return [Appointment(**row) for row in rows]
