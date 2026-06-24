from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient
from unittest.mock import patch
import routes.appointment

app = FastAPI()
app.include_router(routes.appointment.router)
client = TestClient(app)

def test_delete_appointment_success():
    with patch('db_client.get_appointment') as mock_get, patch('db_client.remove_appointment') as mock_remove:
        mock_get.return_value = {"id": 1, "name": "Test Appointment"}
        
        response = client.delete("/appointments/1")
        
        assert response.status_code == 200
        assert response.json() == {
            "message": "Appointment deleted successfully",
            "appointment_id": 1,
        }
        mock_get.assert_called_once_with(1)
        mock_remove.assert_called_once_with(1)

def test_delete_appointment_not_found():
    with patch('db_client.get_appointment') as mock_get:
        mock_get.return_value = None
        
        response = client.delete("/appointments/99")
        
        assert response.status_code == 404
        assert response.json() == {"detail": "Appointment not found"}
        mock_get.assert_called_once_with(99)
