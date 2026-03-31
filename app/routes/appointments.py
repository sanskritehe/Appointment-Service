from fastapi import APIRouter
from app.models import AppointmentUpdate, AppointmentBookingCreate
from app.services.booking_service import (
    list_appointments,
    get_appointment,
    update_booking,
    cancel_booking,
    validate_and_book_appointment
)

router = APIRouter(prefix="/appointments", tags=["Appointment"])


# Book an appointment with time slot validation (KAN-9)
@router.post("/")
def create_appointment(req: AppointmentBookingCreate):
    return validate_and_book_appointment(req.dict())


# Get all appointments
@router.get("/")
def get_appointments():
    return list_appointments()


# Get a single appointment by ID (KAN-15)
@router.get("/{appointment_id}")
def get_appointment_by_id(appointment_id: int):
    return get_appointment(appointment_id)


# Update an appointment by ID
@router.put("/{appointment_id}")
def update_appointment_by_id(appointment_id: int, req: AppointmentUpdate):
    return update_booking(appointment_id, req.dict())


# Cancel an appointment by ID
@router.delete("/{appointment_id}")
def cancel_appointment_by_id(appointment_id: int):
    return cancel_booking(appointment_id)