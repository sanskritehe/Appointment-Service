### FILE: app/db/db_client.py
```python
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError

class DBClient:
    def __init__(self, session: AsyncSession):
        self.session = session

    def query(self, model):
        """
        Create an async query for the given model.

        Args:
            model: The SQLAlchemy model to query.

        Returns:
            sqlalchemy.future.select: The async query object.
        """
        return select(model)  # Use SQLAlchemy's `select` for async queries.

    async def execute(self, query):
        """
        Execute an asynchronous query.

        Args:
            query: The query object.

        Returns:
            result: The result of query execution.
        """
        try:
            result = await self.session.execute(query)
            return result
        except SQLAlchemyError as e:
            raise RuntimeError(f"Database execution error: {e}")

    async def commit(self):
        """
        Commit the current transaction.
        """
        try:
            await self.session.commit()
        except SQLAlchemyError as e:
            raise RuntimeError(f"Database commit error: {e}")

```

### FILE: app/routes/appointments.py
```python
from fastapi import APIRouter, HTTPException, Depends
from app.services.appointment_service import AppointmentService
from app.schemas.response import ErrorResponseModel

router = APIRouter()

@router.delete("/appointments/{id}", status_code=204, responses={
    404: {"model": ErrorResponseModel},
    500: {"model": ErrorResponseModel},
})
async def delete_appointment(id: int, appointment_service: AppointmentService = Depends()):
    """
    Cancel an appointment (hard delete) by ID.

    Args:
        id (int): The ID of the appointment to be deleted.
        appointment_service (AppointmentService): Service layer for managing appointments.

    Returns:
        None: Success without content.
    """
    if id <= 0:
        raise HTTPException(status_code=400, detail="ID must be a positive integer.")

    try:
        deleted_rows = await appointment_service.delete_by_id(id)
        if deleted_rows == 0:
            raise HTTPException(status_code=404, detail=f"Appointment with ID {id} not found.")
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
```

### FILE: app/schemas/response.py
```python
from pydantic import BaseModel

class ErrorResponseModel(BaseModel):
    detail: str
    error_code: str = "unknown_error"  # Default value for error_code.
    metadata: dict | None = None
```

### FILE: app/services/appointment_service.py
```python
from sqlalchemy.exc import SQLAlchemyError
from app.db.db_client import DBClient
from app.models.appointment import Appointment

class AppointmentService:
    def __init__(self, db_client: DBClient):
        self.db_client = db_client

    async def get_by_id(self, id: int) -> Appointment | None:
        """
        Fetch an appointment by its ID.

        Args:
            id (int): The ID of the appointment to retrieve.

        Returns:
            Appointment | None: The retrieved appointment object, or None if not found.
        """
        try:
            query = self.db_client.query(Appointment).filter(Appointment.id == id)
            result = await self.db_client.execute(query)
            return result.scalar_one_or_none()
        except SQLAlchemyError as e:
            raise RuntimeError(f"Database query error: {e}")

    async def delete_by_id(self, id: int) -> int:
        """
        Delete an appointment by its ID (hard delete).

        Args:
            id (int): The ID of the appointment to delete.

        Returns:
            int: The number of rows deleted.
        """
        try:
            query = self.db_client.query(Appointment).filter(Appointment.id == id).delete()
            result = await self.db_client.execute(query)
            await self.db_client.commit()
            return result.rowcount
        except SQLAlchemyError as e:
            raise RuntimeError(f"Database deletion error: {e}")
```