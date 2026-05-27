from app.db_client import create_appointment, get_all_appointments, get_appointment_by_id, update_appointment, soft_delete_appointment, check_slot_availability
from fastapi import HTTPException
from requests.exceptions import HTTPError
from app.models import AppointmentStatus


def create_simple_appointment(data):
    """Create appointment with simple format (user, time) - KAN-17"""
    if not data.get("user") or not data.get("time"):
        raise HTTPException(status_code=400, detail="Missing required fields: user, time")
    return create_appointment(data)


def validate_and_book_appointment(data):
    doctor_id = data.get("doctor_id")
    appointment_date = data.get("appointment_date")
    time_slot = data.get("time_slot")

    # Check if time slot is available
    if not check_slot_availability(doctor_id, appointment_date, time_slot):
        raise HTTPException(status_code=409, detail="Time slot already booked")

    # Create appointment if slot is available
    return create_appointment(data)


def list_appointments():
    return get_all_appointments()


def get_appointment(appointment_id: int):
    try:
        return get_appointment_by_id(appointment_id)
    except HTTPError as e:
        if e.response.status_code == 404:
            raise HTTPException(status_code=404, detail="Appointment not found")
        raise


def update_booking(appointment_id: int, data: dict):
    try:
        appointment = get_appointment_by_id(appointment_id)
    except HTTPError as e:
        if e.response.status_code == 404:
            raise HTTPException(status_code=404, detail="Appointment not found")
        raise

    if appointment["status"] == "booked" and data.get("status") not in ["confirmed", "cancelled"]:
        raise HTTPException(status_code=400, detail="Invalid status transition from booked")
    elif appointment["status"] == "confirmed" and data.get("status") not in ["completed", "cancelled"]:
        raise HTTPException(status_code=400, detail="Invalid status transition from confirmed")
    elif appointment["status"] == "cancelled":
        raise HTTPException(status_code=400, detail="Invalid status transition from cancelled")
    elif appointment["status"] == "completed" and data.get("status") != "completed":
        raise HTTPException(status_code=400, detail="Invalid status transition from completed")

    return update_appointment(appointment_id, data)


def cancel_booking(appointment_id: int):
    try:
        appointment = get_appointment_by_id(appointment_id)  # Explicitly check for appointment existence
        soft_delete_appointment(appointment_id)
    except HTTPError as e:
        if e.response.status_code == 404:
            raise HTTPException(status_code=404, detail="Appointment not found")
        raise


def patch_booking_status(appointment_id: int, data: dict):
    try:
        appointment = get_appointment_by_id(appointment_id)
    except HTTPError as e:
        if e.response.status_code == 404:
            raise HTTPException(status_code=404, detail="Appointment not found")
        raise

    new_status = data.get("status")
    if not new_status or new_status not in AppointmentStatus._value2member_map_:
        raise HTTPException(status_code=422, detail="Invalid status in request body")

    if appointment["status"] == "booked" and new_status not in ["confirmed", "cancelled"]:
        raise HTTPException(status_code=400, detail="Invalid status transition from booked")
    elif appointment["status"] == "confirmed" and new_status not in ["completed", "cancelled"]:
        raise HTTPException(status_code=400, detail="Invalid status transition from confirmed")
    elif appointment["status"] == "cancelled":
        raise HTTPException(status_code=400, detail="Invalid status transition from cancelled")
    elif appointment["status"] == "completed" and new_status != "completed":
        raise HTTPException(status_code=400, detail="Invalid status transition from completed")

    return update_appointment(appointment_id, {"status": new_status})
