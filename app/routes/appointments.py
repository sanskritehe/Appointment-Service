from fastapi import APIRouter, status
from app.models import (
    AppointmentUpdate, AppointmentBookingCreate, AppointmentSimpleCreate, 
    AppointmentResponse, ErrorResponse
)
from app.services.booking_service import (
    list_appointments,
    get_appointment,
    update_booking,
    cancel_booking,
    validate_and_book_appointment,
    create_simple_appointment
)

router = APIRouter(prefix="/appointments", tags=["Appointment"])


# Book an appointment with simple request format (KAN-17)
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=AppointmentResponse)
def create_appointment_simple(req: AppointmentSimpleCreate):
    """Create a new appointment with user and time information. Returns 201 Created."""
    return create_simple_appointment(req.dict())


# Get all appointments
@router.get("/", response_model=list)
def get_appointments():
    """Retrieve all appointments."""
    return list_appointments()


# Get a single appointment by ID
@router.get("/{appointment_id}", response_model=AppointmentResponse, status_code=status.HTTP_200_OK,
            responses={404: {"model": ErrorResponse, "description": "Appointment not found"}})
def get_appointment_by_id(appointment_id: int):
    """
    Retrieve a single appointment by ID.
    
    - **appointment_id**: The appointment ID (path parameter)
    - Returns: Appointment object with id, user, time, status
    - Returns 404 if appointment not found
    """
    return get_appointment(appointment_id)


# Update an appointment by ID (KAN-17 - PUT endpoint per Confluence spec)
@router.put("/{appointment_id}", response_model=AppointmentResponse, status_code=status.HTTP_200_OK,
            responses={404: {"model": ErrorResponse, "description": "Appointment not found"}})
def update_appointment_by_id(appointment_id: int, req: AppointmentUpdate):
    """
    Update an appointment by ID per Confluence API spec.
    
    - **appointment_id**: The appointment ID (path parameter)
    - **Request body**: {time, status} fields to update
    - Returns: Updated appointment object with id, user, time, status
    - Returns 404 if appointment not found
    """
    return update_booking(appointment_id, req.dict())


# Cancel an appointment by ID
@router.delete("/{appointment_id}", status_code=status.HTTP_200_OK,
               responses={404: {"model": ErrorResponse, "description": "Appointment not found"}})
def cancel_appointment_by_id(appointment_id: int):
    """Cancel/delete an appointment by ID. Returns 404 if not found."""
    return cancel_booking(appointment_id)