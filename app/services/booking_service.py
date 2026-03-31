from app.db_client import create_appointment, get_all_appointments, get_appointment_by_id, update_appointment, cancel_appointment, check_slot_availability
from fastapi import HTTPException
from requests.exceptions import HTTPError


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

def update_booking(appointment_id: int, data):
    try:
        return update_appointment(appointment_id, data)
    except HTTPError as e:
        if e.response.status_code == 404:
            raise HTTPException(status_code=404, detail="Appointment not found")
        raise

def cancel_booking(appointment_id: int):
    return cancel_appointment(appointment_id)