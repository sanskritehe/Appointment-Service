import requests
from fastapi import HTTPException
from app.config import DB_SERVICE_URL


def get_appointment_by_id(appointment_id: int):
    try:
        response = requests.get(f"{DB_SERVICE_URL}/appointments/{appointment_id}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError:
        if response.status_code == 404:
            raise HTTPException(status_code=404, detail="Appointment not found")
        raise HTTPException(status_code=500, detail="Database error while fetching appointment")
