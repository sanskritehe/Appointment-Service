from fastapi import APIRouter
from app.models import AppointmentCreate
from app.services.booking_service import (
    book_appointment,
    list_appointments
)

router = APIRouter(prefix="/appointments", tags=["Appointment"])

@router.post("/")
def create_appointment(req: AppointmentCreate):
    return book_appointment(req.dict())

@router.get("/")
def get_appointments():
    return list_appointments()