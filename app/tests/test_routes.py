from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app

client = TestClient(app)

def test_create_appointment_success():
    test_data = {
        "user": "John Doe",
        "time": "2023-10-25T10:00:00"
    }
    test_response = {
        "id": 1,
        "user": "John Doe",
        "time": "2023-10-25T10:00:00",
        "status": "Scheduled"
    }
    with patch("app.services.booking_service.book_appointment", return_value=test_response):
        response = client.post("/appointments/", json=test_data)
        assert response.status_code == 201
        assert response.json() == test_response

def test_create_appointment_invalid_data():
    test_data = {
        "user": "John Doe"
        # Missing "time"
    }
    response = client.post("/appointments/", json=test_data)
    assert response.status_code == 422  # Automatic validation failure

def test_get_all_appointments_success():
    test_response = [
        {
            "id": 1,
            "user": "John Doe",
            "time": "2023-10-25T10:00:00",
            "status": "Scheduled"
        },
        {
            "id": 2,
            "user": "Jane Doe",
            "time": "2023-10-26T11:00:00",
            "status": "Scheduled"
        }
    ]
    with patch("app.services.booking_service.list_appointments", return_value=test_response):
        response = client.get("/appointments/?skip=0&limit=10")
        assert response.status_code == 200
        assert response.json() == test_response

def test_get_all_appointments_empty():
    with patch("app.services.booking_service.list_appointments", return_value=[]):
        response = client.get("/appointments/?skip=0&limit=10")
        assert response.status_code == 200
        assert response.json() == []

def test_get_all_appointments_invalid_pagination():
    response = client.get("/appointments/?skip=-1&limit=10")
    assert response.status_code == 422
    assert "detail" in response.json()
    assert response.json()["detail"][0]["msg"] == "ensure this value is greater than or equal to 0"

def test_delete_appointment_success():
    test_id = 1
    with patch("app.services.booking_service.delete_appointment_by_id", return_value=None):
        response = client.delete(f"/appointments/{test_id}")
        assert response.status_code == 204
        assert response.text == ""

def test_delete_appointment_not_found():
    test_id = 999
    with patch("app.services.booking_service.delete_appointment_by_id", return_value=None):
        response = client.delete(f"/appointments/{test_id}")
        assert response.status_code == 404
        assert response.json() == {"detail": "Appointment not found"}

def test_delete_appointment_invalid_id():
    test_id = -1  # Invalid ID
    response = client.delete(f"/appointments/{test_id}")
    assert response.status_code == 422  # Validation failure due to negative ID
    assert "detail" in response.json()
    assert response.json()["detail"][0]["msg"] == "ensure this value is greater than or equal to 1"
