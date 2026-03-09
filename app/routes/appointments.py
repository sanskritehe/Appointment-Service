from fastapi import APIRouter
from app.models import AppointmentCreate
from app.services.booking_service import (
    book_appointment,
    list_appointments,
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


# Cancel an appointment by ID
@router.delete("/{appointment_id}")
def cancel_appointment_by_id(appointment_id: int):
    return cancel_booking(appointment_id)