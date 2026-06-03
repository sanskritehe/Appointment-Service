### FILE: app/routes/appointments.py
```python
from fastapi import APIRouter, Depends, HTTPException, Path
from app.services.appointment_service import AppointmentService
from app.schemas.appointment import AppointmentResponse

router = APIRouter()

@router.get(
    "/appointments/{id}",
    response_model=AppointmentResponse,
    responses={
        404: {"description": "Appointment not found", "content": {"application/json": {"example": {"detail": "Appointment not found"}}}},
    },
)
async def get_appointment_by_id(
    id: int = Path(..., gt=0, description="The ID of the appointment (must be a positive integer)"),
    appointment_service: AppointmentService = Depends(AppointmentService),
):
    """
    Get a single appointment by ID.
    """
    appointment = await appointment_service.get_appointment_by_id(id)
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appointment
```

### FILE: app/schemas/appointment.py
```python
from pydantic import BaseModel

class AppointmentResponse(BaseModel):
    id: int
    user: str
    time: str
    status: str
```

### FILE: app/services/appointment_service.py
```python
from app.db.db_client import DatabaseClient
from fastapi import Depends

class AppointmentService:
    def __init__(self, db_client: DatabaseClient = Depends(DatabaseClient)):
        self.db_client = db_client

    async def get_appointment_by_id(self, appointment_id: int) -> dict:
        """
        Retrieve a single appointment by its ID from the database.
        """
        query = "SELECT id, user, time, status FROM appointments WHERE id = :id"
        values = {"id": appointment_id}
        row = await self.db_client.fetch_one(query=query, values=values)
        if row:
            return {"id": row["id"], "user": row["user"], "time": row["time"], "status": row["status"]}
        return None
```