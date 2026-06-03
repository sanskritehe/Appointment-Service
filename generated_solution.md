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
    """Updated Response model for appointment endpoints per Confluence spec"""
    id: int
    user: str
    time: str
    status: str

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "user": "string",
                "time": "string",
                "status": "booked"
            }
        }


class AppointmentStatusUpdate(BaseModel):
    status: AppointmentStatus

    class Config:
        schema_extra = {
            "example": {
                "status": "confirmed"
            }
        }


class ErrorResponse(BaseModel):
    detail: str

    class Config:
        schema_extra = {
            "example": {
                "detail": "Error message detailing what went wrong"
            }
        }
    
```

### FILE: db_client.py
```python
import requests
from fastapi import HTTPException
from app.config import DB_SERVICE_URL


def get_appointment_by_id(appointment_id: int):
    try:
        response = requests.get(f"{DB_SERVICE_URL}/appointments/{appointment_id}")
        response.raise_for_status()
        data = response.json()
        if "id" not in data or "user" not in data or "time" not in data or "status" not in data:
            raise HTTPException(status_code=500, detail="Invalid data format received from the database service")
        return data
    except requests.exceptions.HTTPError:
        if response.status_code == 404:
            raise HTTPException(status_code=404, detail="Appointment not found")
        raise HTTPException(status_code=500, detail="Database error while fetching appointment")
```

### FILE: services/appointment_service.py
```python
from app.db_client import get_appointment_by_id


def get_appointment(appointment_id: int):
    """
    Fetch a single appointment by ID.

    - **appointment_id**: ID of the appointment to fetch

    Throws:
    - HTTPException 404: If the appointment does not exist

    Returns:
    - Appointment object
    """
    # Directly fetch and return the appointment from the database client
    return get_appointment_by_id(appointment_id)
```

### FILE: routes/appointments.py
```python
from fastapi import APIRouter, status, HTTPException, Path
from app.models import AppointmentResponse, ErrorResponse
from app.services.appointment_service import get_appointment

router = APIRouter(prefix="/appointments", tags=["Appointment-Service"])


# Get appointment by id (KAN-15)
@router.get("/{appointment_id}", status_code=status.HTTP_200_OK, response_model=AppointmentResponse, responses={
    404: {"model": ErrorResponse, "description": "Appointment not found"}
})
def get_appointment_by_id_endpoint(
    appointment_id: int = Path(..., title="Appointment ID", description="ID of the appointment", ge=1)
):
    """
    Get a single appointment by ID.

    - **Path parameter**: Appointment ID
    - Returns: Appointment object if found
    - Throws:
        - HTTPException 404: If the appointment does not exist
    """
    appointment = get_appointment(appointment_id)
    return appointment
```

### FILE: tests/test_appointments.py
```python
import pytest
from fastapi.testclient import TestClient
from fastapi import HTTPException
from app.main import app

client = TestClient(app)


def test_get_appointment_success(mocker):
    mocker.patch("app.db_client.get_appointment_by_id", return_value={
        "id": 1,
        "user": "John Doe",
        "time": "2024-04-07T10:00:00",
        "status": "booked"
    })

    response = client.get("/appointments/1")
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "user": "John Doe",
        "time": "2024-04-07T10:00:00",
        "status": "booked"
    }


def test_get_appointment_not_found(mocker):
    mocker.patch("app.db_client.get_appointment_by_id", side_effect=HTTPException(status_code=404, detail="Appointment not found"))

    response = client.get("/appointments/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Appointment not found"}


def test_get_appointment_invalid_id():
    response = client.get("/appointments/abc")
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "value is not a valid integer"


def test_get_appointment_negative_id():
    response = client.get("/appointments/-5")
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "ensure this value is greater than or equal to 1"
```