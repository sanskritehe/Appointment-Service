### FILE: db_client.py
```python
import sqlite3


def delete_appointment(appointment_id: int):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM appointments WHERE id = ?", (appointment_id,))
    conn.commit()
    rows_affected = cursor.rowcount
    conn.close()
    if rows_affected == 0:
        return None
    return True

```

### FILE: routes/appointment_routes.py
```python
from fastapi import APIRouter, HTTPException
import services.appointment_service

router = APIRouter()


@router.delete("/appointments/{appointment_id}", response_model=dict)
async def delete_appointment(appointment_id: int):
    result = await services.appointment_service.delete_appointment(appointment_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return {
        "message": "Appointment deleted successfully",
        "appointment_id": appointment_id,
    }

```

### FILE: services/appointment_service.py
```python
import db_client


async def delete_appointment(appointment_id: int):
    return db_client.delete_appointment(appointment_id)

```

### FILE: tests/test_appointment_routes.py
```python
from fastapi import FastAPI
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

```