### FILE: app/routes/appointments.py
```python
from fastapi import APIRouter, HTTPException
from app.models import AppointmentCreate, AppointmentUpdate
from app.services.booking_service import (
    book_appointment,
    list_appointments,
    update_booking,
    cancel_booking
)

router = APIRouter(prefix="/appointments", tags=["Appointment"])


# Create a new appointment
@router.post("/")
def create_appointment(req: AppointmentCreate):
    return book_appointment(req.dict())


# Get all appointments
@router.get("/")
def get_appointments():
    return list_appointments()


# Update an appointment by ID
@router.put("/{appointment_id}")
def update_appointment_by_id(appointment_id: int, req: AppointmentUpdate):
    return update_booking(appointment_id, req.dict())


# Cancel an appointment by ID
@router.delete("/{appointment_id}")
def cancel_appointment_by_id(appointment_id: int):
    try:
        cancel_booking(appointment_id)
        return {"message": "Appointment cancelled successfully"}
    except Exception as e:
        if "404" in str(e):
            raise HTTPException(status_code=404, detail="Appointment not found")
        else:
            raise HTTPException(status_code=500, detail="Failed to cancel appointment")
```

### FILE: app/services/booking_service.py
```python
from app.db_client import create_appointment, get_all_appointments, update_appointment, cancel_appointment


def book_appointment(data):
    # for adding Buissness rules
    return create_appointment(data)

def list_appointments():
    return get_all_appointments()

def update_booking(appointment_id: int, data):
    return update_appointment(appointment_id, data)

def cancel_booking(appointment_id: int):
    try:
        return cancel_appointment(appointment_id)
    except Exception as e:
        if "404" in str(e):
            raise Exception("404")
        else:
            raise Exception("Failed to cancel appointment")
```

### FILE: app/db_client.py
```python
import requests
from app.config import DB_SERVICE_URL

def create_appointment(data: dict):
    response = requests.post(
        f"{DB_SERVICE_URL}/appointments",
        params=data
    )
    response.raise_for_status()
    return response.json()

def get_all_appointments():
    response = requests.get(f"{DB_SERVICE_URL}/appointments")
    response.raise_for_status()
    return response.json()

def update_appointment(appointment_id: int, data: dict):
    response = requests.put(
        f"{DB_SERVICE_URL}/appointments/{appointment_id}",
        json=data
    )
    response.raise_for_status()
    return response.json()

def cancel_appointment(appointment_id: int):
    response = requests.delete(
        f"{DB_SERVICE_URL}/appointments/{appointment_id}"
    )
    response.raise_for_status()
    return response.json()
```