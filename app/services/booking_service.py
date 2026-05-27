from app.db_client import get_appointment_by_id, update_appointment, get_paginated_appointments
from fastapi import HTTPException
from requests.exceptions import HTTPError
from app.models import AppointmentStatus


def patch_booking_status(appointment_id: int, data: dict):
    """
    Patch the status of an appointment based on business rules.

    - **appointment_id**: The ID of the appointment to patch
    - **data**: Dict containing the new status field

    Throws:
    - HTTPException 404: If appointment is not found
    - HTTPException 400: If status transition is invalid or request body contains extra fields

    Returns:
    - Updated appointment object
    """
    if len(data) != 1 or "status" not in data:
        raise HTTPException(status_code=400, detail="Invalid request body. Only 'status' field is allowed.")

    try:
        appointment = get_appointment_by_id(appointment_id)
    except HTTPError as e:
        if e.response.status_code == 404:
            raise HTTPException(status_code=404, detail="Appointment not found")
        raise

    # Extract and validate new status
    new_status = data["status"]
    if new_status not in AppointmentStatus._value2member_map_:
        raise HTTPException(status_code=400, detail="Invalid status value in request body")

    # Validate status transition rules
    current_status = appointment["status"]
    allowed_transitions = {
        "booked": ["confirmed", "cancelled"],
        "confirmed": ["completed", "cancelled"],
        "completed": ["completed"],
        "cancelled": []
    }

    if new_status not in allowed_transitions.get(current_status, []):
        raise HTTPException(
            status_code=400,
            detail=f"Invalid status transition from {current_status} to {new_status}"
        )

    # Update appointment status in the database
    return update_appointment(appointment_id, {"status": new_status})


def get_paginated_appointments_service(page: int, limit: int):
    """
    Fetch paginated appointments using page and limit parameters.

    - **page**: The current page number
    - **limit**: The number of items per page

    Returns:
    - JSON response with total, page, limit, and data fields
    """
    offset = (page - 1) * limit

    try:
        appointments = get_paginated_appointments(offset=offset, limit=limit)
    except HTTPError as e:
        raise HTTPException(status_code=400, detail="Error fetching appointments")

    # Explicit validation of returned data
    required_fields = ["total", "page", "limit", "data"]
    for field in required_fields:
        if field not in appointments:
            raise HTTPException(status_code=500, detail=f"Missing required field '{field}' in response")

    return {
        "total": appointments["total"],
        "page": page,
        "limit": limit,
        "data": appointments["data"]
    }
