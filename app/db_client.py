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
