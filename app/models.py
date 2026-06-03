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
    