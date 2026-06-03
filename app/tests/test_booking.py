import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_create_appointment_success(mocker):
    mocker.patch("app.services.booking_service.check_slot_availability_client", return_value=True)
    mocker.patch("app.services.booking_service.create_appointment_client", return_value={
        "id": 123,
        "patient_id": 1,
        "doctor_id": 2,
        "appointment_date": "2024-04-07",
        "time_slot": "10:00 AM",
        "status": "booked"
    })

    request_body = {
        "patient_id": 1,
        "doctor_id": 2,
        "appointment_date": "2024-04-07",
        "time_slot": "10:00 AM"
    }

    response = client.post("/appointments", json=request_body)
    assert response.status_code == 201
    assert response.json() == {
        "id": 123,
        "patient_id": 1,
        "doctor_id": 2,
        "appointment_date": "2024-04-07",
        "time_slot": "10:00 AM",
        "status": "booked"
    }


def test_create_appointment_slot_unavailable(mocker):
    mocker.patch("app.services.booking_service.check_slot_availability_client", return_value=False)

    request_body = {
        "patient_id": 1,
        "doctor_id": 2,
        "appointment_date": "2024-04-07",
        "time_slot": "10:00 AM"
    }

    response = client.post("/appointments", json=request_body)
    assert response.status_code == 409
    assert response.json()["detail"] == "Requested time slot is already booked."


def test_create_appointment_invalid_date():
    request_body = {
        "patient_id": 1,
        "doctor_id": 2,
        "appointment_date": "07-04-2024",  # Invalid format
        "time_slot": "10:00 AM"
    }

    response = client.post("/appointments", json=request_body)
    assert response.status_code == 422
    assert "appointment_date must be in the format YYYY-MM-DD" in response.text


def test_create_appointment_missing_fields():
    request_body = {
        "patient_id": 1,
        "doctor_id": 2,
        "appointment_date": "2024-04-07"
        # Missing "time_slot"
    }

    response = client.post("/appointments", json=request_body)
    assert response.status_code == 422
    assert response.json()["detail"] == "Missing required fields in request body."
