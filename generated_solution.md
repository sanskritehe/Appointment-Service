### FILE: db_client.py
```python
appointments_db = {
    1: {"id": 1, "subject": "Meeting"},
    2: {"id": 2, "subject": "Conference"},
}


def get_appointment(appointment_id: int):
    return appointments_db.get(appointment_id)


def delete_appointment(appointment_id: int):
    if appointment_id in appointments_db:
        del appointments_db[appointment_id]

```

### FILE: routes/appointment_routes.py
```python
from fastapi import APIRouter, HTTPException
from services.appointment_service import delete_appointment

router = APIRouter()


@router.delete("/appointments/{id}", response_model=dict)
async def delete_appointment_endpoint(id: int):
    try:
        result = delete_appointment(id)
        return result
    except HTTPException as e:
        raise e

```

### FILE: services/appointment_service.py
```python
from fastapi import HTTPException
import db_client


def delete_appointment(appointment_id: int) -> dict:
    appointment = db_client.get_appointment(appointment_id)
    if appointment is None:
        raise HTTPException(status_code=404, detail="Appointment not found")

    db_client.delete_appointment(appointment_id)
    return {
        "message": "Appointment deleted successfully",
        "appointment_id": appointment_id,
    }

```