### FILE: db_client.py
```python
import sqlite3


def delete_appointment(appointment_id: int):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM appointments WHERE id = ?", (appointment_id,))
    conn.commit()
    rows_affected = cursor.rowcount
    conn.close()
    if rows_affected == 0:
        return None
    return True

```

### FILE: routes/appointment_routes.py
```python
from fastapi import APIRouter, HTTPException
import services.appointment_service

router = APIRouter()


@router.delete("/appointments/{appointment_id}", response_model=dict)
async def delete_appointment(appointment_id: int):
    result = await services.appointment_service.delete_appointment(appointment_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return {
        "message": "Appointment deleted successfully",
        "appointment_id": appointment_id,
    }

```

### FILE: services/appointment_service.py
```python
import db_client


async def delete_appointment(appointment_id: int):
    return db_client.delete_appointment(appointment_id)

```