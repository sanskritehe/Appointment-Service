from fastapi import HTTPException
from app.db_client import RecordNotFoundException, get_appointment_by_id, update_appointment
from app.models import AppointmentStatus


VALID_TRANSITIONS = {
    "booked": {"confirmed", "cancelled"},
    "confirmed": {"completed", "cancelled"},
    "completed": set(),
    "cancelled": set()
}


def update_appointment_status(
    appointment_id: int,
    status_update: dict,
):
    """
    Updates the status of an appointment while validating status transitions.

    - **appointment_id**: ID of the appointment to update
    - **status_update**: Dict containing the new status

    Throws:
    - HTTPException 400: If an invalid transition is detected
    - HTTPException 404: If the appointment does not exist
    """

    # Fetch existing appointment
    try:
        appointment = get_appointment_by_id(appointment_id)
    except RecordNotFoundException:
        raise HTTPException(status_code=404, detail="Appointment not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error while fetching appointment: {str(e)}")

    current_status = appointment["status"]
    new_status = status_update.get("status")

    # Validate the state transition
    allowed_transitions = VALID_TRANSITIONS.get(current_status, set())
    if new_status not in allowed_transitions:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid status transition. Cannot transition from '{current_status}' to '{new_status}'. "
                   f"Allowed transitions: {list(allowed_transitions)}"
        )

    # Update the status in the database
    try:
        updated_appointment = update_appointment(appointment_id, status_update)
    except RecordNotFoundException:
        raise HTTPException(status_code=404, detail="Appointment not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error while updating appointment: {str(e)}")

    return updated_appointment
