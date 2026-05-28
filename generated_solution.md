### FILE: routes/appointments.py
```python
from fastapi import APIRouter, status, HTTPException, Depends
from app.models import AppointmentStatusUpdate, AppointmentResponse
from app.services.appointment_service import update_appointment_status as update_status_service

router = APIRouter(prefix="/appointments", tags=["Appointment-Service"])

# Update appointment status (KAN-22)
@router.patch("/{appointment_id}/status", status_code=status.HTTP_200_OK, response_model=AppointmentResponse)
def update_appointment_status_endpoint(
    appointment_id: int,
    req: AppointmentStatusUpdate,
):
    """
    Update the status of an existing appointment.

    - **Path parameter**: Appointment ID
    - **Req body**: {"status": "string"}
    - **Allowed transitions**:
        - booked → confirmed → completed
        - booked → cancelled
        - confirmed → cancelled
    - Returns: Updated appointment object

    Throws:
    - HTTPException 400: If status transition is invalid
    - HTTPException 404: If the appointment does not exist
    """
    updated_appointment = update_status_service(appointment_id, req.dict())
    return AppointmentResponse(**updated_appointment)
```

---

### FILE: services/appointment_service.py
```python
from fastapi import HTTPException
from app.db_client import RecordNotFoundException, get_appointment_by_id, update_appointment
from app.models import AppointmentStatus


VALID_TRANSITIONS = {
    "booked": {"confirmed", "cancelled"},
    "confirmed": {"completed", "cancelled"},
    "completed": set(),
    "cancelled": set()
}


def update_appointment_status(
    appointment_id: int,
    status_update: dict,
):
    """
    Updates the status of an appointment while validating status transitions.

    - **appointment_id**: ID of the appointment to update
    - **status_update**: Dict containing the new status

    Throws:
    - HTTPException 400: If an invalid transition is detected
    - HTTPException 404: If the appointment does not exist
    """

    # Fetch existing appointment
    try:
        appointment = get_appointment_by_id(appointment_id)
    except RecordNotFoundException:
        raise HTTPException(status_code=404, detail="Appointment not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error while fetching appointment: {str(e)}")

    current_status = appointment["status"]
    new_status = status_update.get("status")

    # Validate the state transition
    allowed_transitions = VALID_TRANSITIONS.get(current_status, set())
    if new_status not in allowed_transitions:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid status transition. Cannot transition from '{current_status}' to '{new_status}'. "
                   f"Allowed transitions: {list(allowed_transitions)}"
        )

    # Update the status in the database
    try:
        updated_appointment = update_appointment(appointment_id, status_update)
    except RecordNotFoundException:
        raise HTTPException(status_code=404, detail="Appointment not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error while updating appointment: {str(e)}")

    return updated_appointment
```

---

### FILE: tests/test_patch_status.py
```python
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
```