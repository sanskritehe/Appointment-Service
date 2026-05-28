### FILE: app/routes/appointments.py
```python
from fastapi import APIRouter, HTTPException, Path
from pydantic import BaseModel, Field
from app.services.appointment_service import update_appointment_status

router = APIRouter()

class StatusUpdateRequest(BaseModel):
    status: str = Field(..., description="The new status of the appointment", min_length=1)

@router.patch("/appointments/{id}/status")
async def patch_appointment_status(
    id: int = Path(..., description="The ID of the appointment to update"),
    status_update: StatusUpdateRequest,
):
    try:
        updated_appointment = await update_appointment_status(id, status_update.status)
        return updated_appointment
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
```

### FILE: app/db_client.py
```python
from typing import Optional
import sqlite3

# Database connection settings
DATABASE_PATH = "data/appointments.db"

def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row  # To return results as dictionaries
    return conn

async def get_appointment_by_id(appointment_id: int) -> Optional[dict]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM appointments WHERE id = ?", (appointment_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

async def update_appointment_in_db(appointment_id: int, updates: dict) -> Optional[dict]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE appointments SET status = ? WHERE id = ?", (updates["status"], appointment_id))
    conn.commit()

    # Fetch the updated record to return
    cursor.execute("SELECT * FROM appointments WHERE id = ?", (appointment_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None
```

### FILE: app/services/appointment_service.py
```python
from fastapi import HTTPException
from app.db_client import update_appointment_in_db, get_appointment_by_id
from app.constants import VALID_TRANSITIONS

ALLOWED_STATUSES = {"booked", "confirmed", "completed", "cancelled"}

async def update_appointment_status(appointment_id: int, new_status: str):
    if new_status not in ALLOWED_STATUSES:
        raise HTTPException(
            status_code=400,
            detail="Invalid status value. Allowed values are: 'booked', 'confirmed', 'completed', 'cancelled'."
        )

    appointment = await get_appointment_by_id(appointment_id)
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")

    current_status = appointment["status"]
    if current_status not in VALID_TRANSITIONS or new_status not in VALID_TRANSITIONS[current_status]:
        raise HTTPException(
            status_code=400,
            detail="Invalid status transition"
        )

    updated_appointment = await update_appointment_in_db(appointment_id, {"status": new_status})
    if not updated_appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
        
    return updated_appointment
```