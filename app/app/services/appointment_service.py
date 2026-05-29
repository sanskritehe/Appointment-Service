from sqlalchemy.exc import SQLAlchemyError
from app.db.db_client import DBClient
from app.models.appointment import Appointment

class AppointmentService:
    def __init__(self, db_client: DBClient):
        self.db_client = db_client

    async def get_by_id(self, id: int) -> Appointment | None:
        """
        Fetch an appointment by its ID.

        Args:
            id (int): The ID of the appointment to retrieve.

        Returns:
            Appointment | None: The retrieved appointment object, or None if not found.
        """
        try:
            query = self.db_client.query(Appointment).filter(Appointment.id == id)
            result = await self.db_client.execute(query)
            return result.scalar_one_or_none()
        except SQLAlchemyError as e:
            raise RuntimeError(f"Database query error: {e}")

    async def delete_by_id(self, id: int) -> int:
        """
        Delete an appointment by its ID (hard delete).

        Args:
            id (int): The ID of the appointment to delete.

        Returns:
            int: The number of rows deleted.
        """
        try:
            query = self.db_client.query(Appointment).filter(Appointment.id == id).delete()
            result = await self.db_client.execute(query)
            await self.db_client.commit()
            return result.rowcount
        except SQLAlchemyError as e:
            raise RuntimeError(f"Database deletion error: {e}")
