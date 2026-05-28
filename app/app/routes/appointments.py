from fastapi import APIRouter, HTTPException, Path
from pydantic import BaseModel, Field
from app.services.appointment_service import update_appointment_status

router = APIRouter()

class StatusUpdateRequest(BaseModel):
    status: str = Field(..., description="The new status of the appointment", min_length=1)

@router.patch("/appointments/{id}/status")
async def patch_appointment_status(
    id: int = Path(..., description="The ID of the appointment to update"),
    status_update: StatusUpdateRequest,
):
    try:
        updated_appointment = await update_appointment_status(id, status_update.status)
        return updated_appointment
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
