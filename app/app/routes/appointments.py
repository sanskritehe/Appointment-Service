from fastapi import APIRouter, Depends, HTTPException
from app.services.appointment_service import AppointmentService

router = APIRouter()

@router.get("/appointments/{id}", response_model=dict)
async def get_appointment_by_id(
    id: int,
    appointment_service: AppointmentService = Depends(AppointmentService),
):
    """
    Endpoint to retrieve a single appointment by its ID.
    """
    appointment = await appointment_service.get_appointment_by_id(id)
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appointment
