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
