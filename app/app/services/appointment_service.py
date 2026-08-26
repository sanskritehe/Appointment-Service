from app.db.db_client import DatabaseClient
from fastapi import Depends

class AppointmentService:
    def __init__(self, db_client: DatabaseClient = Depends(DatabaseClient)):
        self.db_client = db_client

    async def get_all_appointments(self) -> list:
        """
        Retrieve all appointments from the database.
        """
        query = "SELECT id, user, time, status FROM appointments WHERE TRUE"
        result = await self.db_client.fetch_all(query=query, values={})
        return [
            {"id": row["id"], "user": row["user"], "time": row["time"], "status": row["status"]}
            for row in result
        ]
