from fastapi import HTTPException
from requests.exceptions import HTTPError


def validate_and_book_appointment(data: dict, create_appointment_client, check_slot_availability_client):
    """
    Validate slot availability and create a new appointment.

    - **data**: Dict containing patient_id, doctor_id, appointment_date, time_slot
    - **create_appointment_client**: Dependency-injected database client to create appointments
    - **check_slot_availability_client**: Dependency-injected client to check slot availability

    Throws:
    - HTTPException 400: If any required field is missing
    - HTTPException 409: If requested slot is already booked

    Returns:
    - Dict with appointment_id and confirmation status
    """
    required_fields = {"patient_id", "doctor_id", "appointment_date", "time_slot"}
    if not required_fields.issubset(data.keys()):
        raise HTTPException(status_code=400, detail="Missing required fields in request body.")

    # Validate slot availability
    try:
        is_available = check_slot_availability_client(
            data["doctor_id"], data["appointment_date"], data["time_slot"]
        )
    except HTTPError:
        raise HTTPException(status_code=500, detail="Error checking slot availability.")

    if not is_available:
        raise HTTPException(status_code=409, detail="Requested time slot is already booked.")

    # Create appointment
    try:
        new_appointment = create_appointment_client(data)
    except HTTPError:
        raise HTTPException(status_code=500, detail="Error creating appointment record.")

    return {
        "id": new_appointment["id"],
        "patient_id": data["patient_id"],
        "doctor_id": data["doctor_id"],
        "appointment_date": data["appointment_date"],
        "time_slot": data["time_slot"],
        "status": "booked",
    }
