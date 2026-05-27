### FILE: models.py
```python
from pydantic import BaseModel, Field
from enum import Enum


class AppointmentStatus(str, Enum):
    """Appointment status enumeration per Confluence spec"""
    booked = "booked"
    cancelled = "cancelled"
    completed = "completed"
    confirmed = "confirmed"


class AppointmentStatusUpdate(BaseModel):
    """Request model for PATCH /appointments/{id}/status endpoint (KAN-22)"""
    status: AppointmentStatus = Field(..., description="Appointment status")

    class Config:
        schema_extra = {
            "example": {
                "status": "confirmed"
            }
        }


class AppointmentResponse(BaseModel):
    """Response model for appointment endpoints per Confluence spec"""
    id: int
    user: str
    time: str
    status: AppointmentStatus

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "user": "John Doe",
                "time": "2024-04-07T10:00:00Z",
                "status": "booked"
            }
        }


class ErrorResponse(BaseModel):
    """Error response model per Confluence spec"""
    detail: str

    class Config:
        schema_extra = {
            "example": {
                "detail": "Appointment not found"
            }
        }
```

### FILE: routes/appointments.py
```python
from fastapi import APIRouter, status
from app.models import AppointmentStatusUpdate, AppointmentResponse, ErrorResponse
from app.services.booking_service import patch_booking_status

router = APIRouter(prefix="/appointments", tags=["Appointment"])


# Patch an appointment's status by ID (KAN-22)
@router.patch("/{appointment_id}/status",
              response_model=AppointmentResponse,
              status_code=status.HTTP_200_OK,
              responses={
                  404: {"model": ErrorResponse, "description": "Appointment not found"},
                  400: {"model": ErrorResponse, "description": "Invalid status transition"},
              })
def patch_appointment_status(appointment_id: int, req: AppointmentStatusUpdate):
    """
    Patch an appointment's status by ID.

    - **appointment_id**: The appointment ID (path parameter)
    - **Request body**: {status} field to update
        - Example: {"status": "confirmed"}
    - Returns: Updated appointment object
    - Raises HTTP 404 if appointment is not found
    - Raises HTTP 400 for invalid status transition
    """
    return patch_booking_status(appointment_id, req)
```

### FILE: services/booking_service.py
```python
from app.db_client import get_appointment_by_id, update_appointment
from fastapi import HTTPException
from requests.exceptions import HTTPError
from app.models import AppointmentStatusUpdate, AppointmentStatus


def patch_booking_status(appointment_id: int, req: AppointmentStatusUpdate):
    try:
        appointment = get_appointment_by_id(appointment_id)
    except HTTPError as e:
        status_code = e.response.status_code if e.response else 500
        if status_code == 404:
            raise HTTPException(status_code=404, detail="Appointment not found")
        raise HTTPException(status_code=status_code, detail="Error querying appointment")

    new_status = req.status

    # Validate status transition rules
    if appointment["status"] == AppointmentStatus.booked and new_status not in [AppointmentStatus.confirmed, AppointmentStatus.cancelled]:
        raise HTTPException(status_code=400, detail="Invalid status transition from 'booked'")
    elif appointment["status"] == AppointmentStatus.confirmed and new_status not in [AppointmentStatus.completed, AppointmentStatus.cancelled]:
        raise HTTPException(status_code=400, detail="Invalid status transition from 'confirmed'")
    elif appointment["status"] in [AppointmentStatus.cancelled, AppointmentStatus.completed]:
        raise HTTPException(status_code=400, detail=f"Invalid status transition from '{appointment['status']}'")

    # Ensure only updated fields are sent
    update_data = req.dict(exclude_unset=True)

    try:
        updated_appointment = update_appointment(appointment_id, update_data)
    except HTTPError as e:
        status_code = e.response.status_code if e.response else 500
        raise HTTPException(status_code=status_code, detail="Error updating appointment")

    return updated_appointment
```

### FILE: db_client.py
```python
import requests
from app.config import DB_SERVICE_URL


def get_appointment_by_id(appointment_id: int):
    response = requests.get(f"{DB_SERVICE_URL}/appointments/{appointment_id}")
    response.raise_for_status()
    return response.json()


def update_appointment(appointment_id: int, data: dict):
    response = requests.patch(
        f"{DB_SERVICE_URL}/appointments/{appointment_id}",
        json=data
    )
    response.raise_for_status()
    return response.json()
```