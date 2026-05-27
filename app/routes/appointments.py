from fastapi import APIRouter, status, HTTPException, Query
from app.models import (
    AppointmentStatusUpdate, AppointmentBookingCreate, AppointmentSimpleCreate,
    AppointmentResponse, ErrorResponse, AppointmentDeleteResponse
)
from app.services.booking_service import (
    get_paginated_appointments_service,
    get_appointment,
    update_booking,
    validate_and_book_appointment,
    create_simple_appointment,
    patch_booking_status,
)

router = APIRouter(prefix="/appointments", tags=["Appointment-Service"])


# Book an appointment with simple request format (KAN-17)
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=AppointmentResponse)
def create_appointment_simple(req: AppointmentSimpleCreate):
    """Create a new appointment with user and time information. Returns 201 Created."""
    return create_simple_appointment(req.dict())


# Get all appointments with optional pagination (KAN-20)
@router.get("/", response_model=dict, status_code=status.HTTP_200_OK,
            responses={400: {"model": ErrorResponse, "description": "Invalid pagination parameters"}})
def get_appointments(
    page: int = Query(1, ge=1, description="The page number to fetch"),
    limit: int = Query(10, ge=1, le=100, description="The number of items per page")
):
    """
    Retrieve all appointments with optional pagination.

    - **page**: The page number (default: 1)
    - **limit**: The number of items per page (default: 10, max: 100)
    - Returns: JSON object with total, page, limit, and data fields
    - Returns 400 if pagination params are invalid
    """
    return get_paginated_appointments_service(page, limit)


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


# Patch an appointment's status by ID (KAN-22 - PATCH endpoint per Confluence spec)
@router.patch("/{appointment_id}/status", response_model=AppointmentResponse, status_code=status.HTTP_200_OK,
               responses={404: {"model": ErrorResponse, "description": "Appointment not found"},
                          400: {"model": ErrorResponse, "description": "Invalid status transition or request body"}})
def patch_appointment_status(appointment_id: int, req: AppointmentStatusUpdate):
    """
    Patch an appointment's status by ID per Confluence API spec.

    - **appointment_id**: The appointment ID (path parameter)
    - **Request body**: {status} field to update
    - Returns: Updated appointment object with id, user, time, status
    - Returns 404 if appointment not found
    - Returns 400 with {"detail": "Invalid status transition"} if transition is not allowed
    """
    return patch_booking_status(appointment_id, req.dict())
