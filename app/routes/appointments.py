from fastapi import APIRouter, status, HTTPException, Query, Depends
from app.models import (
    AppointmentStatusUpdate, AppointmentBookingCreate, AppointmentResponse, ErrorResponse,
    AppointmentDeleteResponse
)
from app.services.booking_service import validate_and_book_appointment
from app.services.db_client import create_appointment, check_slot_availability

router = APIRouter(prefix="/appointments", tags=["Appointment-Service"])


# Book an appointment with detailed request format (KAN-19)
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=AppointmentResponse)
def create_appointment(
    req: AppointmentBookingCreate,
    create_appointment_client=Depends(create_appointment),
    check_slot_availability_client=Depends(check_slot_availability)
):
    """
    Create a new appointment record for a patient.

    - **Req body**: patient_id, doctor_id, appointment_date, time_slot
    - Validates that the requested time slot is not already booked
    - Returns: {id, patient_id, doctor_id, appointment_date, time_slot, status}

    Throws:
    - HTTPException 400: If any validation fails
    - HTTPException 409: If the requested time slot is already booked
    """
    appointment = validate_and_book_appointment(
        req.dict(),
        create_appointment_client=create_appointment_client,
        check_slot_availability_client=check_slot_availability_client
    )
    return AppointmentResponse(**appointment)
