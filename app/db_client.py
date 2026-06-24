appointments_db: dict[int, dict] = {}


def get_appointment(appointment_id: int):
    return appointments_db.get(appointment_id)


def remove_appointment(appointment_id: int):
    if appointment_id in appointments_db:
        del appointments_db[appointment_id]
