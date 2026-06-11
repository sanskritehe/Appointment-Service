import strawberry
from typing import Optional
from app.services.booking_service import (
    book_appointment, list_appointments, update_booking, cancel_booking,
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
    def appointment(self, id: int) -> Optional[Appointment]:
        for r in list_appointments():
            if r["id"] == id:
                return Appointment(id=r["id"], user=r["user"], time=r["time"], status=r["status"])
        return None


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
