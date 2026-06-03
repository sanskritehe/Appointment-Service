### FILE: db_client.py
```python
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
```

### FILE: services/appointment_service.py
```python
from fastapi import HTTPException
from app.db_client import get_appointment_by_id


def get_appointment(appointment_id: int):
    """
    Fetch a single appointment by ID.

    - **appointment_id**: ID of the appointment to fetch

    Throws:
    - HTTPException 404: If the appointment does not exist

    Returns:
    - Appointment object
    """
    try:
        appointment = get_appointment_by_id(appointment_id)
        return appointment
    except HTTPException as e:
        if e.status_code == 404:
            raise HTTPException(status_code=404, detail="Appointment not found")
        raise HTTPException(status_code=500, detail="Database error while fetching appointment")
```

### FILE: tests/test_appointments.py
```python
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_get_appointment_success(mocker):
    mocker.patch("app.db_client.get_appointment_by_id", return_value={
        "id": 1,
        "user": "John Doe",
        "time": "2023-12-01T10:00:00",
        "status": "booked"
    })

    response = client.get("/appointments/1")
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "user": "John Doe",
        "time": "2023-12-01T10:00:00",
        "status": "booked"
    }


def test_get_appointment_not_found(mocker):
    mocker.patch("app.db_client.get_appointment_by_id", side_effect=HTTPException(status_code=404, detail="Appointment not found"))

    response = client.get("/appointments/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Appointment not found"}


def test_get_appointment_invalid_id():
    response = client.get("/appointments/abc")
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "value is not a valid integer"


def test_get_appointment_negative_id():
    response = client.get("/appointments/-5")
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "ensure this value is greater than or equal to 1"
```