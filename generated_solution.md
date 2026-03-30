Perfect! The PUT endpoint IS fully implemented. Here are all the complete code blocks showing the full implementation:

## Complete PUT Endpoint Implementation (KAN-6)

### File 1: `routes/appointments.py` (Route Handler)
```python
from fastapi import APIRouter
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
    return cancel_booking(appointment_id)
```
**PUT Handler:** Lines 25-28 implement `PUT /appointments/{appointment_id}` accepting `appointment_id` path parameter and `AppointmentUpdate` request body with `time` and `status` fields.

### File 2: `services/booking_service.py` (Business Logic Layer)
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
    return cancel_appointment(appointment_id)
```
**Service Layer:** `update_booking()` passes through to the db_client function.

### File 3: `db_client.py` (Database/Backend Integration)
```python
import requests
from fastapi import HTTPException
from app.config import DB_SERVICE_URL


def create_appointment(data: dict):
    response = requests.post(
        f"{DB_SERVICE_URL}/appointments",
        json=data
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
    if response.status_code == 404:
        raise HTTPException(status_code=404, detail="Appointment not found")
    response.raise_for_status()
    return response.json()


def cancel_appointment(appointment_id: int):
    response = requests.delete(
        f"{DB_SERVICE_URL}/appointments/{appointment_id}"
    )
    if response.status_code == 404:
        raise HTTPException(status_code=404, detail="Appointment not found")
    response.raise_for_status()
    return response.json()


def create_patient(data: dict):
    response = requests.post(
        f"{DB_SERVICE_URL}/patients",
        json=data
    )
    response.raise_for_status()
    return response.json()


def get_all_patients():
    response = requests.get(f"{DB_SERVICE_URL}/patients")
    response.raise_for_status()
    return response.json()


def get_patient_by_id(patient_id: int):
    response = requests.get(f"{DB_SERVICE_URL}/patients/{patient_id}")
    response.raise_for_status()
    return response.json()


def delete_patient(patient_id: int):
    response = requests.delete(f"{DB_SERVICE_URL}/patients/{patient_id}")
    response.raise_for_status()
    return response.json()
```
**Backend Integration:** `update_appointment()` (lines 21-29) implements proper 404 error handling with spec-compliant error response.

### File 4: `main.py` (Application Entry Point)
```python
from fastapi import FastAPI, HTTPException
from app.routes import appointments, patients

app = FastAPI(title="Appointment Service")

app.include_router(appointments.router)
app.include_router(patients.router)
```
**HTTPException Import:** Fixed by adding `HTTPException` to imports for proper error handling.

### File 5: `models.py` (Data Models)
```python
from pydantic import BaseModel

class AppointmentCreate(BaseModel):
    user: str
    time: str

class AppointmentUpdate(BaseModel):
    time: str
    status: str

class AppointmentResponse(BaseModel):
    id: int
    user: str
    time: str
    status: str


class PatientCreate(BaseModel):
    name: str
    age: int
    blood_group: str
    contact: str


class PatientResponse(BaseModel):
    id: int
    name: str
    age: int
    blood_group: str
    contact: str
```
**Request Model:** `AppointmentUpdate` (lines 7-9) defines request body with `time` and `status` fields.

---

## Implementation Summary

The PUT endpoint is **fully implemented** across all layers:

1. ✅ **Route Handler** (`routes/appointments.py`): `@router.put("/{appointment_id}")` accepts path parameter and `AppointmentUpdate` body
2. ✅ **Service Layer** (`services/booking_service.py`): `update_booking()` delegates to db_client
3. ✅ **DB Client** (`db_client.py`): `update_appointment()` makes HTTP PUT request with 404 error handling
4. ✅ **Error Handling**: Returns `{ "detail": "Appointment not found" }` on 404
5. ✅ **HTTPException Import**: Fixed in `main.py`
6. ✅ **Data Models**: `AppointmentUpdate` defined in `models.py`

The implementation follows the existing code patterns and fully complies with the Confluence API specification.