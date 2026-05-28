import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db_client import RecordNotFoundException

client = TestClient(app)


def test_update_status_success(mocker):
    mock_get = mocker.patch("app.db_client.get_appointment_by_id", return_value={
        "id": 1,
        "patient_id": 1,
        "doctor_id": 1,
        "appointment_date": "2023-12-01",
        "time_slot": "10:00 AM",
        "status": "booked"
    })
    mock_update = mocker.patch("app.db_client.update_appointment", return_value={
        "id": 1,
        "patient_id": 1,
        "doctor_id": 1,
        "appointment_date": "2023-12-01",
        "time_slot": "10:00 AM",
        "status": "confirmed"
    })

    response = client.patch("/appointments/1/status", json={"status": "confirmed"})
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "patient_id": 1,
        "doctor_id": 1,
        "appointment_date": "2023-12-01",
        "time_slot": "10:00 AM",
        "status": "confirmed"
    }
    mock_get.assert_called_once_with(1)
    mock_update.assert_called_once_with(1, {"status": "confirmed"})


def test_update_status_invalid_transition(mocker):
    mocker.patch("app.db_client.get_appointment_by_id", return_value={
        "id": 1,
        "patient_id": 1,
        "doctor_id": 1,
        "appointment_date": "2023-12-01",
        "time_slot": "10:00 AM",
        "status": "completed"
    })

    response = client.patch("/appointments/1/status", json={"status": "booked"})
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Invalid status transition. Cannot transition from 'completed' to 'booked'. Allowed transitions: []"
    }


def test_update_status_not_found(mocker):
    mocker.patch("app.db_client.get_appointment_by_id", side_effect=RecordNotFoundException)

    response = client.patch("/appointments/999/status", json={"status": "confirmed"})
    assert response.status_code == 404
    assert response.json() == {"detail": "Appointment not found"}


def test_update_status_missing_field():
    response = client.patch("/appointments/1/status", json={})
    assert response.status_code == 422
    response_json = response.json()
    assert response_json["detail"][0]["loc"] == ["body", "status"]
    assert response_json["detail"][0]["msg"] == "field required"


def test_update_status_invalid_enum_value():
    response = client.patch("/appointments/1/status", json={"status": "invalid_status"})
    assert response.status_code == 422
    assert "value is not a valid enumeration" in response.text


def test_update_status_database_error_get_appointment(mocker):
    mocker.patch("app.db_client.get_appointment_by_id", side_effect=Exception("Database error while fetching appointment"))

    response = client.patch("/appointments/1/status", json={"status": "confirmed"})
    assert response.status_code == 500
    assert response.json() == {"detail": "Database error while fetching appointment: Database error while fetching appointment"}


def test_update_status_database_error_update_appointment(mocker):
    mocker.patch("app.db_client.get_appointment_by_id", return_value={
        "id": 1,
        "patient_id": 1,
        "doctor_id": 1,
        "appointment_date": "2023-12-01",
        "time_slot": "10:00 AM",
        "status": "booked"
    })
    mocker.patch("app.db_client.update_appointment", side_effect=Exception("Database error while updating appointment"))

    response = client.patch("/appointments/1/status", json={"status": "confirmed"})
    assert response.status_code == 500
    assert response.json() == {"detail": "Database error while updating appointment: Database error while updating appointment"}


def test_update_status_invalid_appointment_id():
    response = client.patch("/appointments/abc/status", json={"status": "confirmed"})
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "value is not a valid integer"


def test_update_status_malformed_json():
    response = client.patch("/appointments/1/status", data="{'status': 'confirmed'")  # Malformed JSON
    assert response.status_code == 422
    assert "Expecting property name enclosed in double quotes" in response.text
