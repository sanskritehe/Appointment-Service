### FILE: services/booking_service.py
```python
from app.db_client import get_appointment_by_id, update_appointment
from fastapi import HTTPException
from requests.exceptions import HTTPError
from app.models import AppointmentStatus


def patch_booking_status(appointment_id: int, data: dict):
    """
    Patch the status of an appointment based on business rules.

    - **appointment_id**: The ID of the appointment to patch
    - **data**: Dict containing the new status field

    Throws:
    - HTTPException 404: If appointment is not found
    - HTTPException 400: If status transition is invalid
    - HTTPException 422: If the request input is invalid

    Returns:
    - Updated appointment object
    """
    try:
        appointment = get_appointment_by_id(appointment_id)
    except HTTPError as e:
        if e.response.status_code == 404:
            raise HTTPException(status_code=404, detail="Appointment not found")
        raise

    # Extract and validate new status
    new_status = data.get("status")
    if not new_status or new_status not in AppointmentStatus._value2member_map_:
        raise HTTPException(status_code=422, detail="Invalid status in request body")

    # Validate status transition rules
    current_status = appointment["status"]
    allowed_transitions = {
        "booked": ["confirmed", "cancelled"],
        "confirmed": ["completed", "cancelled"],
        "completed": ["completed"],
        "cancelled": []
    }

    if new_status not in allowed_transitions.get(current_status, []):
        raise HTTPException(
            status_code=400,
            detail=f"Invalid status transition from {current_status} to {new_status}"
        )

    # Update appointment status in the database
    return update_appointment(appointment_id, {"status": new_status})
```

### FILE: models.py
```python
from pydantic import BaseModel, Field, root_validator, ValidationError
from enum import Enum


class AppointmentStatus(str, Enum):
    """Appointment status enumeration per Confluence spec"""
    booked = "booked"
    confirmed = "confirmed"
    completed = "completed"
    cancelled = "cancelled"


class AppointmentCreate(BaseModel):
    user: str
    time: str


class AppointmentSimpleCreate(BaseModel):
    """Request model for POST /appointments endpoint (KAN-17)"""
    user: str
    time: str

    class Config:
        schema_extra = {
            "example": {
                "user": "John Doe",
                "time": "2024-04-07T10:00:00Z"
            }
        }


class AppointmentBookingCreate(BaseModel):
    patient_id: int
    doctor_id: int
    appointment_date: str
    time_slot: str


class AppointmentUpdate(BaseModel):
    """Request model for PUT /appointments/{id} endpoint (KAN-17)"""
    time: str = Field(..., description="Appointment time in ISO format")
    status: AppointmentStatus = Field(..., description="Appointment status")

    class Config:
        schema_extra = {
            "example": {
                "time": "2024-04-07T11:00:00Z",
                "status": "booked"
            }
        }


class AppointmentStatusUpdate(BaseModel):
    """Request model for PATCH /appointments/{id}/status"""
    status: AppointmentStatus = Field(..., description="Appointment status")

    @root_validator(pre=True)
    def validate_only_status_field(cls, values):
        if len(values) != 1 or 'status' not in values:
            raise ValueError("Invalid request body. Only 'status' field is allowed.")
        return values

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


class AppointmentDeleteResponse(BaseModel):
    """Response model for DELETE /appointments/{id} endpoint per Confluence spec"""
    message: str
    appointment_id: int

    class Config:
        schema_extra = {
            "example": {
                "message": "Appointment deleted successfully",
                "appointment_id": 1
            }
        }


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