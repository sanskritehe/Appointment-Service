from fastapi import HTTPException
from app.db_client import update_appointment_in_db, get_appointment_by_id, get_appointments_paginated
from app.constants import VALID_TRANSITIONS

ALLOWED_STATUSES = {"booked", "confirmed", "completed", "cancelled"}

async def update_appointment_status(appointment_id: int, new_status: str):
    if new_status not in ALLOWED_STATUSES:
        raise HTTPException(
            status_code=400,
            detail="Invalid status value. Allowed values are: 'booked', 'confirmed', 'completed', 'cancelled'."
        )

    appointment = await get_appointment_by_id(appointment_id)
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")

    current_status = appointment["status"]
    if current_status not in VALID_TRANSITIONS or new_status not in VALID_TRANSITIONS[current_status]:
        raise HTTPException(
            status_code=400,
            detail="Invalid status transition"
        )

    updated_appointment = await update_appointment_in_db(appointment_id, {"status": new_status})
    if not updated_appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
        
    return updated_appointment

async def get_paginated_appointments(page: int, limit: int):
    offset = (page - 1) * limit
    try:
        appointments, total_count = await get_appointments_paginated(offset, limit)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {
        "total": total_count,
        "page": page,
        "limit": limit,
        "data": appointments
    }
