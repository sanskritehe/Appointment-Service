from fastapi import APIRouter, Depends
from app.services.appointment_service import AppointmentService
from app.models.appointment import Appointment

router = APIRouter()

@router.get("/appointments", response_model=list[Appointment])
async def get_appointments(service: AppointmentService = Depends()):
    """
    GET /appointments
    Fetch all appointments from the database.
    Returns:
        List of appointments or an empty list if no appointments exist.
    """
    return await service.get_all_appointments()
