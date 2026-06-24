import db_client
from fastapi import HTTPException


def delete_appointment(appointment_id: int):
    appointment = db_client.get_appointment(appointment_id)
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    db_client.remove_appointment(appointment_id)
