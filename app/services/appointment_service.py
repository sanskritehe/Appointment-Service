from fastapi import HTTPException
from app.db_client import get_appointment_by_id


def get_appointment(appointment_id: int):
    """
    Fetch a single appointment by ID.

    - **appointment_id**: ID of the appointment to fetch

    Throws:
    - HTTPException 404: If the appointment does not exist

    Returns:
    - Appointment object
    """
    try:
        appointment = get_appointment_by_id(appointment_id)
        return appointment
    except HTTPException as e:
        if e.status_code == 404:
            raise HTTPException(status_code=404, detail="Appointment not found")
        raise HTTPException(status_code=500, detail="Database error while fetching appointment")
