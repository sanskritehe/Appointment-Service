Perfect! Here's the corrected code:

**File: `services/booking_service.py` - Updated `cancel_booking()` function**

```python
def cancel_booking(appointment_id: int):
    try:
        cancel_appointment(appointment_id)
        return {
            "message": "Appointment deleted successfully",
            "appointment_id": appointment_id
        }
    except HTTPError as e:
        if e.response.status_code == 404:
            raise HTTPException(status_code=404, detail="Appointment not found")
        raise
```

## Fix Applied

**Issue**: The `cancel_booking()` function was returning the raw database service response unchanged, which doesn't match the Confluence spec format.

**Solution**: Updated `cancel_booking()` to:
1. Call `cancel_appointment(appointment_id)` to delete from the database
2. **Transform the response** to return the required Confluence format: `{"message": "Appointment deleted successfully", "appointment_id": appointment_id}`
3. Maintain error handling for 404 responses

**Result**: The DELETE endpoint now returns exactly the format specified in the Confluence API specification and KAN-16 requirements.