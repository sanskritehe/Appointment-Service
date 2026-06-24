from fastapi import APIRouter, HTTPException
import services.appointment_service

router = APIRouter()


@router.delete("/appointments/{appointment_id}", response_model=dict)
async def delete_appointment(appointment_id: int):
    result = await services.appointment_service.delete_appointment(appointment_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return {
        "message": "Appointment deleted successfully",
        "appointment_id": appointment_id,
    }
