### FILE: app/db_client.py
```python
from typing import Optional, List, Tuple, Dict
import sqlite3

# Database connection settings
DATABASE_PATH = "data/appointments.db"

DEFAULT_LIMIT = 10
MAX_LIMIT = 100

def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row  # To return results as dictionaries
    return conn

async def get_appointment_by_id(appointment_id: int) -> Optional[dict]:
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM appointments WHERE id = ?", (appointment_id,))
        row = cursor.fetchone()
        return dict(row) if row else None
    finally:
        conn.close()

async def get_appointments_paginated(offset: int, limit: int) -> Tuple[List[Dict], int]:
    if offset < 0 or limit < 1 or limit > MAX_LIMIT:
        raise ValueError("Invalid pagination parameters. Offset must be >= 0, limit must be between 1 and 100.")

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Fetch paginated results
        cursor.execute("SELECT * FROM appointments LIMIT ? OFFSET ?", (limit, offset))
        rows = cursor.fetchall()

        # Fetch total count to calculate pagination
        cursor.execute("SELECT COUNT(*) FROM appointments")
        total_count = cursor.fetchone()[0]

        return [dict(row) for row in rows], total_count
    finally:
        conn.close()
```

### FILE: app/routes/appointments.py
```python
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from typing import List, Any
from app.services.appointment_service import get_paginated_appointments

router = APIRouter()

class AppointmentResponse(BaseModel):
    id: int
    status: str
    # Include other appointment fields as necessary

class PaginatedResponse(BaseModel):
    total: int
    page: int
    limit: int
    count: int
    data: List[AppointmentResponse]

@router.get("/appointments", response_model=PaginatedResponse)
async def get_appointments(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Number of items per page"),
):
    try:
        paginated_result = await get_paginated_appointments(page, limit)
        if not paginated_result["data"] and page > 1:
            raise HTTPException(status_code=404, detail="Page number out of range.")
        paginated_result["count"] = len(paginated_result["data"])
        return paginated_result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")
```