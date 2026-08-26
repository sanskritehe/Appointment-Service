### FILE: app/routes/appointment_routes.py
```python
from fastapi import APIRouter, Depends
from app.services.appointment_service import AppointmentService
from app.models.appointment import Appointment

router = APIRouter()

@router.get("/appointments", response_model=list[Appointment])
async def get_appointments(service: AppointmentService = Depends()):
    """
    GET /appointments
    Fetch all appointments from the database.
    Returns:
        List of appointments or an empty list if no appointments exist.
    """
    return await service.get_all_appointments()
```

### FILE: app/services/appointment_service.py
```python
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
```

### FILE: app/db_client/appointment_db_client.py
```python
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
```

### FILE: app/models/appointment.py
```python
from pydantic import BaseModel
from datetime import datetime

class Appointment(BaseModel):
    id: int
    user_id: int
    title: str
    description: str
    scheduled_time: datetime
    created_at: datetime
    updated_at: datetime
```