from fastapi import APIRouter, Depends, HTTPException
from app.services.appointment_service import AppointmentService
from app.schemas.appointment import AppointmentsListResponse

router = APIRouter()

@router.get("/appointments", response_model=AppointmentsListResponse)
async def get_appointments(
    appointment_service: AppointmentService = Depends(AppointmentService)
):
    """
    Get a list of all appointments.
    """
    try:
        appointments = await appointment_service.get_all_appointments()
        return {"data": appointments}
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")
