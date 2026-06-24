import strawberry
import strawberry.federation
from app.database import DatabaseClient
from fastapi import HTTPException

db = DatabaseClient()

@strawberry.federation.type(keys=['id'])
class Appointment:
    id: strawberry.ID
    user: str
    time: str
    status: str

@strawberry.type
class Query:
    @strawberry.field
    def appointment(self, id: strawberry.ID) -> Appointment:
        row = db.get_appointment(int(id))
        if row:
            return Appointment(
                id=strawberry.ID(str(row['id'])),
                user=row['user'],
                time=row['time'],
                status=row['status'],
            )
        else:
            raise HTTPException(status_code=404, detail="Appointment not found")

schema = strawberry.federation.Schema(query=Query)
