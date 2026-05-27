from app.db.db_client import DBClient

class AppointmentService:
    def __init__(self, db_client: DBClient = DBClient()):
        self.db_client = db_client

    async def get_appointment_by_id(self, appointment_id: int) -> dict:
        query = "SELECT * FROM appointments WHERE id = :id"
        result = await self.db_client.fetch_one(query, {"id": appointment_id})
        return result
