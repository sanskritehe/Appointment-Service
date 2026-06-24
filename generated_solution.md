### FILE: db_client.py
```python
import requests


def delete_appointment_from_db(appointment_id: int):
    response = requests.delete(f"http://localhost:8001/appointments/{appointment_id}")
    if response.status_code == 404:
        return None
    response.raise_for_status()
    return True

```

### FILE: routes/appointments.py
```python
from fastapi import APIRouter, HTTPException
from services.appointment_service import delete_appointment

router = APIRouter()


@router.delete("/appointments/{id}", response_description="Delete an appointment")
async def remove_appointment(id: int):
    try:
        response = delete_appointment(id)
        return response
    except HTTPException as e:
        raise e

```

### FILE: services/appointment_service.py
```python
from fastapi import HTTPException
from db_client import delete_appointment_from_db


def delete_appointment(appointment_id: int):
    result = delete_appointment_from_db(appointment_id)
    if not result:
        raise HTTPException(status_code=404, detail="Appointment not found")

    return {
        "message": "Appointment deleted successfully",
        "appointment_id": appointment_id,
    }

```