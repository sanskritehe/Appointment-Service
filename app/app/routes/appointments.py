from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from typing import List, Any
from app.services.appointment_service import get_paginated_appointments

router = APIRouter()

class AppointmentResponse(BaseModel):
    id: int
    status: str
    # Include other appointment fields as necessary

class PaginatedResponse(BaseModel):
    total: int
    page: int
    limit: int
    count: int
    data: List[AppointmentResponse]

@router.get("/appointments", response_model=PaginatedResponse)
async def get_appointments(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Number of items per page"),
):
    try:
        paginated_result = await get_paginated_appointments(page, limit)
        if not paginated_result["data"] and page > 1:
            raise HTTPException(status_code=404, detail="Page number out of range.")
        paginated_result["count"] = len(paginated_result["data"])
        return paginated_result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")
