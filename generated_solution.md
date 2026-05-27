### FILE: routes/appointments.py
```python
from fastapi import APIRouter, status, HTTPException, Query, Depends
from app.models import (
    AppointmentStatusUpdate, AppointmentBookingCreate, AppointmentResponse, ErrorResponse,
    AppointmentDeleteResponse
)
from app.services.booking_service import validate_and_book_appointment
from app.services.db_client import create_appointment, check_slot_availability

router = APIRouter(prefix="/appointments", tags=["Appointment-Service"])


# Book an appointment with detailed request format (KAN-19)
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=AppointmentResponse)
def create_appointment(
    req: AppointmentBookingCreate,
    create_appointment_client=Depends(create_appointment),
    check_slot_availability_client=Depends(check_slot_availability)
):
    """
    Create a new appointment record for a patient.

    - **Req body**: patient_id, doctor_id, appointment_date, time_slot
    - Validates that the requested time slot is not already booked
    - Returns: {id, patient_id, doctor_id, appointment_date, time_slot, status}

    Throws:
    - HTTPException 400: If any validation fails
    - HTTPException 409: If the requested time slot is already booked
    """
    appointment = validate_and_book_appointment(
        req.dict(),
        create_appointment_client=create_appointment_client,
        check_slot_availability_client=check_slot_availability_client
    )
    return AppointmentResponse(**appointment)
```

---

### FILE: services/booking_service.py
```python
from fastapi import HTTPException
from requests.exceptions import HTTPError


def validate_and_book_appointment(data: dict, create_appointment_client, check_slot_availability_client):
    """
    Validate slot availability and create a new appointment.

    - **data**: Dict containing patient_id, doctor_id, appointment_date, time_slot
    - **create_appointment_client**: Dependency-injected database client to create appointments
    - **check_slot_availability_client**: Dependency-injected client to check slot availability

    Throws:
    - HTTPException 400: If any required field is missing
    - HTTPException 409: If requested slot is already booked

    Returns:
    - Dict with appointment_id and confirmation status
    """
    required_fields = {"patient_id", "doctor_id", "appointment_date", "time_slot"}
    if not required_fields.issubset(data.keys()):
        raise HTTPException(status_code=400, detail="Missing required fields in request body.")

    # Validate slot availability
    try:
        is_available = check_slot_availability_client(
            data["doctor_id"], data["appointment_date"], data["time_slot"]
        )
    except HTTPError:
        raise HTTPException(status_code=500, detail="Error checking slot availability.")

    if not is_available:
        raise HTTPException(status_code=409, detail="Requested time slot is already booked.")

    # Create appointment
    try:
        new_appointment = create_appointment_client(data)
    except HTTPError:
        raise HTTPException(status_code=500, detail="Error creating appointment record.")

    return {
        "id": new_appointment["id"],
        "patient_id": data["patient_id"],
        "doctor_id": data["doctor_id"],
        "appointment_date": data["appointment_date"],
        "time_slot": data["time_slot"],
        "status": "booked",
    }
```

---

### FILE: models.py
```python
from pydantic import BaseModel, Field, root_validator, HTTPException, validator
from enum import Enum
from datetime import datetime


class AppointmentStatus(str, Enum):
    """Appointment status enumeration per Confluence spec"""
    booked = "booked"
    confirmed = "confirmed"
    completed = "completed"
    cancelled = "cancelled"


class AppointmentBookingCreate(BaseModel):
    """Request model for POST /appointments endpoint"""
    patient_id: int
    doctor_id: int
    appointment_date: str
    time_slot: str

    @validator("appointment_date")
    def validate_date_format(cls, value):
        try:
            datetime.strptime(value, "%Y-%m-%d")
        except ValueError:
            raise ValueError("appointment_date must be in the format YYYY-MM-DD")
        return value

    class Config:
        schema_extra = {
            "example": {
                "patient_id": 1,
                "doctor_id": 2,
                "appointment_date": "2024-04-07",
                "time_slot": "10:00 AM"
            }
        }


class AppointmentResponse(BaseModel):
    """Response model for appointment endpoints per Confluence spec"""
    id: int
    patient_id: int
    doctor_id: int
    appointment_date: str
    time_slot: str
    status: AppointmentStatus

    class Config:
        schema_extra = {
            "example": {
                "id": 123,
                "patient_id": 1,
                "doctor_id": 2,
                "appointment_date": "2024-04-07",
                "time_slot": "10:00 AM",
                "status": "booked"
            }
        }
```

---

### FILE: tests/test_booking.py
```python
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_create_appointment_success(mocker):
    mocker.patch("app.services.booking_service.check_slot_availability_client", return_value=True)
    mocker.patch("app.services.booking_service.create_appointment_client", return_value={
        "id": 123,
        "patient_id": 1,
        "doctor_id": 2,
        "appointment_date": "2024-04-07",
        "time_slot": "10:00 AM",
        "status": "booked"
    })

    request_body = {
        "patient_id": 1,
        "doctor_id": 2,
        "appointment_date": "2024-04-07",
        "time_slot": "10:00 AM"
    }

    response = client.post("/appointments", json=request_body)
    assert response.status_code == 201
    assert response.json() == {
        "id": 123,
        "patient_id": 1,
        "doctor_id": 2,
        "appointment_date": "2024-04-07",
        "time_slot": "10:00 AM",
        "status": "booked"
    }


def test_create_appointment_slot_unavailable(mocker):
    mocker.patch("app.services.booking_service.check_slot_availability_client", return_value=False)

    request_body = {
        "patient_id": 1,
        "doctor_id": 2,
        "appointment_date": "2024-04-07",
        "time_slot": "10:00 AM"
    }

    response = client.post("/appointments", json=request_body)
    assert response.status_code == 409
    assert response.json()["detail"] == "Requested time slot is already booked."


def test_create_appointment_invalid_date():
    request_body = {
        "patient_id": 1,
        "doctor_id": 2,
        "appointment_date": "07-04-2024",  # Invalid format
        "time_slot": "10:00 AM"
    }

    response = client.post("/appointments", json=request_body)
    assert response.status_code == 422
    assert "appointment_date must be in the format YYYY-MM-DD" in response.text


def test_create_appointment_missing_fields():
    request_body = {
        "patient_id": 1,
        "doctor_id": 2,
        "appointment_date": "2024-04-07"
        # Missing "time_slot"
    }

    response = client.post("/appointments", json=request_body)
    assert response.status_code == 422
    assert response.json()["detail"] == "Missing required fields in request body."
```