### FILE: app/graphql_schema.py
```python
import strawberry
from typing import Optional
from app.services.booking_service import (
    book_appointment, list_appointments, update_booking, cancel_booking,
    get_appointment_by_id
)


@strawberry.federation.type(keys=["id"])
class Appointment:
    id: int
    user: str
    time: str
    status: str


@strawberry.input
class CreateAppointmentInput:
    user: str
    time: str


@strawberry.input
class UpdateAppointmentInput:
    time: str


@strawberry.type
class Query:
    @strawberry.field
    def appointments(self) -> list[Appointment]:
        records = list_appointments()
        return [Appointment(id=r["id"], user=r["user"], time=r["time"], status=r["status"]) for r in records]

    @strawberry.field
    def appointmentById(self, id: int) -> Appointment:
        appointment = get_appointment_by_id(id)
        if appointment is None:
            raise ValueError("Appointment not found")
        return Appointment(id=appointment["id"], user=appointment["user"], time=appointment["time"], status=appointment["status"])


@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_appointment(self, input: CreateAppointmentInput) -> Appointment:
        r = book_appointment({"user": input.user, "time": input.time})
        return Appointment(id=r["id"], user=r["user"], time=r["time"], status=r["status"])

    @strawberry.mutation
    def update_appointment(self, id: int, input: UpdateAppointmentInput) -> Appointment:
        r = update_booking(id, {"time": input.time})
        return Appointment(id=r["id"], user=r["user"], time=r["time"], status=r["status"])

    @strawberry.mutation
    def cancel_appointment(self, id: int) -> bool:
        cancel_booking(id)
        return True


schema = strawberry.federation.Schema(query=Query, mutation=Mutation, enable_federation_2=True)
```

### FILE: app/services/booking_service.py
```python
from app.db_client import create_appointment, get_all_appointments, update_appointment, cancel_appointment, get_appointment


def book_appointment(data):
    # for adding Buissness rules
    return create_appointment(data)

def list_appointments():
    return get_all_appointments()

def update_booking(appointment_id: int, data):
    return update_appointment(appointment_id, data)

def cancel_booking(appointment_id: int):
    return cancel_appointment(appointment_id)

def get_appointment_by_id(appointment_id: int):
    return get_appointment(appointment_id)
```

### FILE: app/db_client.py
```python
import requests
from app.config import DB_SERVICE_URL

def create_appointment(data: dict):
    response = requests.post(
        f"{DB_SERVICE_URL}/appointments",
        params=data
    )
    response.raise_for_status()
    return response.json()

def get_all_appointments():
    response = requests.get(f"{DB_SERVICE_URL}/appointments")
    response.raise_for_status()
    return response.json()

def update_appointment(appointment_id: int, data):
    response = requests.put(
        f"{DB_SERVICE_URL}/appointments/{appointment_id}",
        json=data
    )
    response.raise_for_status()
    return response.json()

def cancel_appointment(appointment_id: int):
    response = requests.delete(
        f"{DB_SERVICE_URL}/appointments/{appointment_id}"
    )
    return response.json()

def get_appointment(appointment_id: int):
    response = requests.get(
        f"{DB_SERVICE_URL}/appointments/{appointment_id}"
    )
    if response.status_code == 404:
        return None
    response.raise_for_status()
    return response.json()
```