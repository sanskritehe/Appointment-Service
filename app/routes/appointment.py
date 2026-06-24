from fastapi import APIRouter, HTTPException
import services.appointment_service

router = APIRouter()


@router.delete("/appointments/{appointment_id}", response_model=dict)
async def delete_appointment(appointment_id: int):
    try:
        services.appointment_service.delete_appointment(appointment_id)
        return {
            "message": "Appointment deleted successfully",
            "appointment_id": appointment_id,
        }
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
