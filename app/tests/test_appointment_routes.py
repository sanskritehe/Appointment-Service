from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient
from unittest.mock import patch
from routes.appointment_routes import router

app = FastAPI()
app.include_router(router)
client = TestClient(app)


def test_delete_appointment_success():
    appointment_id = 1
    with patch("services.appointment_service.delete_appointment", return_value=True):
        response = client.delete(f"/appointments/{appointment_id}")
        assert response.status_code == 200
        assert response.json() == {
            "message": "Appointment deleted successfully",
            "appointment_id": appointment_id,
        }


def test_delete_appointment_not_found():
    appointment_id = 999
    with patch("services.appointment_service.delete_appointment", return_value=None):
        response = client.delete(f"/appointments/{appointment_id}")
        assert response.status_code == 404
        assert response.json() == {"detail": "Appointment not found"}

