from app.db.db_client import DatabaseClient

class AppointmentService:
    def __init__(self, db_client: DatabaseClient = DatabaseClient()):
        self.db_client = db_client

    async def get_appointment_by_id(self, appointment_id: int) -> dict:
        """
        Retrieve a single appointment by its ID from the database.
        """
        if not isinstance(appointment_id, int) or appointment_id <= 0:
            raise ValueError("Invalid appointment ID. Must be a positive integer.")
        
        query = "SELECT id, user, time, status FROM appointments WHERE id = :id"
        result = await self.db_client.fetch_one(query, {"id": appointment_id})
        if result:
            return {"id": result["id"], "user": result["user"], "time": result["time"], "status": result["status"]}
        return None
