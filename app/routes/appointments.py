from fastapi import APIRouter, status, HTTPException, Depends
from app.models import AppointmentStatusUpdate, AppointmentResponse
from app.services.appointment_service import update_appointment_status as update_status_service

router = APIRouter(prefix="/appointments", tags=["Appointment-Service"])

# Update appointment status (KAN-22)
@router.patch("/{appointment_id}/status", status_code=status.HTTP_200_OK, response_model=AppointmentResponse)
def update_appointment_status_endpoint(
    appointment_id: int,
    req: AppointmentStatusUpdate,
):
    """
    Update the status of an existing appointment.

    - **Path parameter**: Appointment ID
    - **Req body**: {"status": "string"}
    - **Allowed transitions**:
        - booked → confirmed → completed
        - booked → cancelled
        - confirmed → cancelled
    - Returns: Updated appointment object

    Throws:
    - HTTPException 400: If status transition is invalid
    - HTTPException 404: If the appointment does not exist
    """
    updated_appointment = update_status_service(appointment_id, req.dict())
    return AppointmentResponse(**updated_appointment)
