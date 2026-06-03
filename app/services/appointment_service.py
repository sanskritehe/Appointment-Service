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
    # Directly fetch and return the appointment from the database client
    return get_appointment_by_id(appointment_id)
