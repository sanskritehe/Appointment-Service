### FILE: config.py
```python
DB_SERVICE_URL = "http://localhost:8001"  # Default URL for connecting to the Appointment Database Service
```

### FILE: db_client.py
```python
import requests
from app.config import DB_SERVICE_URL


def get_appointment_by_id(appointment_id: int):
    response = requests.get(f"{DB_SERVICE_URL}/appointments/{appointment_id}")
    response.raise_for_status()
    return response.json()


def update_appointment(appointment_id: int, data: dict):
    response = requests.patch(
        f"{DB_SERVICE_URL}/appointments/{appointment_id}",
        json=data
    )
    response.raise_for_status()
    return response.json()


def get_paginated_appointments(offset: int, limit: int):
    if offset < 0 or limit <= 0 or limit > 100:
        raise HTTPException(status_code=400, detail="Invalid pagination parameters. Offset must be >= 0 and limit between 1 and 100.")

    response = requests.get(
        f"{DB_SERVICE_URL}/appointments",
        params={"offset": offset, "limit": limit}
    )
    response.raise_for_status()
    response_data = response.json()

    # Explicit validation of response format
    required_fields = {"total", "page", "limit", "data"}
    if not required_fields.issubset(response_data.keys()):
        raise HTTPException(status_code=500, detail="Invalid response from Appointment Database Service")

    return response_data
```

### FILE: routes/appointments.py
```python
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
```

### FILE: services/booking_service.py
```python
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
```

### FILE: tests/test_pagination.py
```python
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_pagination_defaults():
    response = client.get("/appointments")
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["page"] == 1
    assert response_data["limit"] == 10
    assert "total" in response_data
    assert "data" in response_data


def test_invalid_page_param():
    response = client.get("/appointments?page=0&limit=10")
    assert response.status_code == 400
    assert response.json()["detail"] == "Page must be 1 or greater."


def test_invalid_limit_param():
    response = client.get("/appointments?page=1&limit=101")
    assert response.status_code == 400
    assert response.json()["detail"] == "Limit must be between 1 and 100."


def test_empty_result():
    # Assuming an empty database for this test
    response = client.get("/appointments?page=2&limit=10")
    assert response.status_code == 200
    assert response.json()["data"] == []
```