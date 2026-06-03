import requests
from fastapi import HTTPException
from app.config import DB_SERVICE_URL


def get_appointment_by_id(appointment_id: int):
    try:
        response = requests.get(f"{DB_SERVICE_URL}/appointments/{appointment_id}")
        response.raise_for_status()
        data = response.json()
        if "id" not in data or "user" not in data or "time" not in data or "status" not in data:
            raise HTTPException(status_code=500, detail="Invalid data format received from the database service")
        return data
    except requests.exceptions.HTTPError:
        if response.status_code == 404:
            raise HTTPException(status_code=404, detail="Appointment not found")
        raise HTTPException(status_code=500, detail="Database error while fetching appointment")
