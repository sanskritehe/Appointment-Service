from fastapi import APIRouter, HTTPException, Depends
from app.services.appointment_service import AppointmentService
from app.schemas.response import ErrorResponseModel

router = APIRouter()

@router.delete("/appointments/{id}", status_code=204, responses={
    404: {"model": ErrorResponseModel},
    500: {"model": ErrorResponseModel},
})
async def delete_appointment(id: int, appointment_service: AppointmentService = Depends()):
    """
    Cancel an appointment (hard delete) by ID.

    Args:
        id (int): The ID of the appointment to be deleted.
        appointment_service (AppointmentService): Service layer for managing appointments.

    Returns:
        None: Success without content.
    """
    if id <= 0:
        raise HTTPException(status_code=400, detail="ID must be a positive integer.")

    try:
        deleted_rows = await appointment_service.delete_by_id(id)
        if deleted_rows == 0:
            raise HTTPException(status_code=404, detail=f"Appointment with ID {id} not found.")
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
