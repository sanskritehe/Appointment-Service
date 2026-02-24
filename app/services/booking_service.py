from app.db_client import create_appointment, get_all_appointments

def book_appointment(data):
    # for adding Buissness rules
    return create_appointment(data)

def list_appointments():
    return get_all_appointments()