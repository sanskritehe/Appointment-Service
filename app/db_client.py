appointments_db = {
    1: {"id": 1, "subject": "Meeting"},
    2: {"id": 2, "subject": "Conference"},
}


def get_appointment(appointment_id: int):
    return appointments_db.get(appointment_id)


def delete_appointment(appointment_id: int):
    if appointment_id in appointments_db:
        del appointments_db[appointment_id]
