### FILE: db_client.py
```python
appointments_db: dict[int, dict] = {}


def get_appointment(appointment_id: int):
    return appointments_db.get(appointment_id)


def remove_appointment(appointment_id: int):
    if appointment_id in appointments_db:
        del appointments_db[appointment_id]

```

### FILE: routes/appointment.py
```python
from fastapi import APIRouter, HTTPException
import services.appointment_service

router = APIRouter()


@router.delete("/appointments/{appointment_id}", response_model=dict)
async def delete_appointment(appointment_id: int):
    try:
        services.appointment_service.delete_appointment(appointment_id)
        return {
            "message": "Appointment deleted successfully",
            "appointment_id": appointment_id,
        }
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

```

### FILE: services/appointment_service.py
```python
import db_client
from fastapi import HTTPException


def delete_appointment(appointment_id: int):
    appointment = db_client.get_appointment(appointment_id)
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    db_client.remove_appointment(appointment_id)

```