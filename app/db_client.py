import requests


def delete_appointment_from_db(appointment_id: int):
    response = requests.delete(f"http://localhost:8001/appointments/{appointment_id}")
    if response.status_code == 404:
        return None
    response.raise_for_status()
    return True
