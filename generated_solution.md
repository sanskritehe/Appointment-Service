### FILE: app/db/db_client.py
```python
import databases
from sqlalchemy import create_engine, MetaData

DATABASE_URL = "sqlite:///./test.db"  # Update this if your database is not SQLite

database = databases.Database(DATABASE_URL)
metadata = MetaData()

class DatabaseClient:
    def __init__(self, database_instance=None):
        self.database = database_instance or database

    async def connect(self):
        """
        Connect to the database. Should be called during application startup.
        """
        await self.database.connect()

    async def disconnect(self):
        """
        Disconnect from the database. Should be called during application shutdown.
        """
        await self.database.disconnect()

    async def fetch_one(self, query: str, values: dict):
        """
        Fetch a single record from the database using a query and values.
        """
        return await self.database.fetch_one(query=query, values=values)
    
    async def fetch_all(self, query: str, values: dict = None):
        """
        Fetch multiple records from the database using a query and values.
        """
        return await self.database.fetch_all(query=query, values=values or {})

```

### FILE: app/routes/appointments.py
```python
from fastapi import APIRouter, Depends, HTTPException
from app.services.appointment_service import AppointmentService
from app.schemas.appointment import AppointmentsListResponse

router = APIRouter()

@router.get("/appointments", response_model=AppointmentsListResponse)
async def get_appointments(
    appointment_service: AppointmentService = Depends(AppointmentService)
):
    """
    Get a list of all appointments.
    """
    try:
        appointments = await appointment_service.get_all_appointments()
        return {"data": appointments}
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")
```

### FILE: app/services/appointment_service.py
```python
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
```