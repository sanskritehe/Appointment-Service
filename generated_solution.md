### FILE: app/graphql_schema.py
```python
from typing import List

from fastapi import Depends
from strawberry import AUTO
from strawberry.federation import Key
from strawberry.federation.custom_scalar import CustomScalar
from strawberry.schema import StrawberrySchema

from app.services.booking_service import (
    list_appointments,
    book_appointment,
    update_booking,
    cancel_booking
)

from pydantic import BaseModel

class Query:
    @strawberry.federation.type(keys=[Key("id", "ID")])
    class Query:
        appointments: List[str]
        appointments_by_user: List[str]

        @strawberry.field(resolver=lambda: "Hello, world!")
        def message(self):
            return StrawberrySchema._get_type(AUTO)
            pass

        @strawberry.field
        def appointments(self) -> List[str]:
            return list_appointments()

        @strawberry.field
        def appointments_by_user(self, user: str) -> str:
            # You should call your existing service function
            # instead of making an assumption like this.
            # This is an oversimplified example.
            # You should return an empty list if the user does not exist.
            result = []
            # Call existing service function to get data
            data = book_appointment(user)
            if data:
                result = data
            return result

class Mutation:
    @strawberry.federation.type(keys=[Key("id", "ID")])
    class Mutation:
        @strawberry.mutation
        def create_appointment(self, req: str) -> str:
            return book_appointment(req)

        @strawberry.mutation
        def update_appointment_by_id(self, appointment_id: int, req: str) -> str:
            return update_booking(appointment_id, req)

        @strawberry.mutation
        def cancel_appointment_by_id(self, appointment_id: int) -> str:
            return cancel_booking(appointment_id)

class AppointmentQuery:
    class Query:
        appointments: List[str]

        @strawberry.field
        def appointments(self) -> List[str]:
            return list_appointments()

Schema = StrawberrySchema(Query, Mutation)
```