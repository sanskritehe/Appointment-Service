from fastapi import APIRouter, status, HTTPException, Path
from app.models import AppointmentResponse, ErrorResponse
from app.services.appointment_service import get_appointment

router = APIRouter(prefix="/appointments", tags=["Appointment-Service"])


# Get appointment by id (KAN-15)
@router.get("/{appointment_id}", status_code=status.HTTP_200_OK, response_model=AppointmentResponse, responses={
    404: {"model": ErrorResponse, "description": "Appointment not found"}
})
def get_appointment_by_id_endpoint(
    appointment_id: int = Path(..., title="Appointment ID", description="ID of the appointment", ge=1)
):
    """
    Get a single appointment by ID.

    - **Path parameter**: Appointment ID
    - Returns: Appointment object if found
    - Throws:
        - HTTPException 404: If the appointment does not exist
    """
    appointment = get_appointment(appointment_id)
    return AppointmentResponse(**appointment)
