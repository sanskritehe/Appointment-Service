### FILE: app/routes/appointments.py
```python
from fastapi import APIRouter, Depends, HTTPException
from app.services.appointment_service import AppointmentService

router = APIRouter()

@router.get("/appointments/{id}", response_model=dict)
async def get_appointment_by_id(
    id: int,
    appointment_service: AppointmentService = Depends(AppointmentService),
):
    """
    Endpoint to retrieve a single appointment by its ID.
    """
    appointment = await appointment_service.get_appointment_by_id(id)
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appointment
```

### FILE: app/services/appointment_service.py
```python
from app.db.db_client import DBClient

class AppointmentService:
    def __init__(self, db_client: DBClient = DBClient()):
        self.db_client = db_client

    async def get_appointment_by_id(self, appointment_id: int) -> dict:
        query = "SELECT * FROM appointments WHERE id = :id"
        result = await self.db_client.fetch_one(query, {"id": appointment_id})
        return result
```

### FILE: app/db/db_client.py
```python
import databases
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")
database = databases.Database(DATABASE_URL)

class DBClient:
    def __init__(self):
        self.database = database

    async def fetch_one(self, query: str, values: dict) -> dict:
        """
        Fetch a single record matching the query from the database.
        """
        return await self.database.fetch_one(query=query, values=values)
```