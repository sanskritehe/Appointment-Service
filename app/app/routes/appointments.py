from fastapi import APIRouter, Depends, HTTPException, Path
from app.services.appointment_service import AppointmentService
from app.schemas.appointment import AppointmentResponse

router = APIRouter()

@router.get("/appointments/{id}", response_model=AppointmentResponse)
async def get_appointment(
    id: int = Path(..., title="Appointment ID", ge=1),
    appointment_service: AppointmentService = Depends()
):
    """
    Get a single appointment by ID.
    """
    appointment = await appointment_service.get_appointment_by_id(id)
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appointment
