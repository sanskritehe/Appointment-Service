### FILE: app/db/db_client.py
```python
import databases
from sqlalchemy import create_engine, MetaData

DATABASE_URL = "sqlite:///./test.db"  # Update this if your database is not SQLite

database = databases.Database(DATABASE_URL)
metadata = MetaData()

class DatabaseClient:
    def __init__(self):
        self.database = database

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
```

---

### FILE: app/routes/appointments.py
```python
from fastapi import APIRouter, Depends, HTTPException, Path
from app.services.appointment_service import AppointmentService
from app.schemas.appointment import AppointmentResponse

router = APIRouter()

@router.get("/appointments/{id}", response_model=AppointmentResponse)
async def get_appointment(
    id: int = Path(..., title="Appointment ID", ge=1),
    appointment_service: AppointmentService = Depends()
):
    """
    Get a single appointment by ID.
    """
    appointment = await appointment_service.get_appointment_by_id(id)
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appointment
```

---

### FILE: app/services/appointment_service.py
```python
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
```

---

### FILE: app/schemas/appointment.py
```python
from pydantic import BaseModel

class AppointmentResponse(BaseModel):
    id: int
    user: str
    time: str
    status: str
```

---

### FILE: app/main.py
```python
from fastapi import FastAPI
from app.db.db_client import database
from app.routes import appointments

app = FastAPI()

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

app.include_router(appointments.router)
```