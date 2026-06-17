from app.db_client import create_appointment, get_all_appointments, update_appointment, cancel_appointment


def book_appointment(data):
    # for adding Buissness rules
    return create_appointment(data)

def list_appointments():
    return get_all_appointments()

def update_booking(appointment_id: int, data):
    return update_appointment(appointment_id, data)

def cancel_booking(appointment_id: int):
    try:
        return cancel_appointment(appointment_id)
    except Exception as e:
        if "404" in str(e):
            raise Exception("404")
        else:
            raise Exception("Failed to cancel appointment")
