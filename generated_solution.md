## Summary

I've completed the implementation of the PUT /appointments/{id} endpoint for the KAN-10 ticket. Here's what was already in place and what I enhanced:

### ✅ Already Implemented:
- **Route** (`routes/appointments.py` lines 26-28): PUT endpoint accepting appointment_id and AppointmentUpdate model
- **Models** (`models.py`): AppointmentUpdate and AppointmentResponse models with correct fields
- **DB Client** (`db_client.py`): HTTP PUT request to backend service

### 📝 Enhancement Made:
**File: `app/services/booking_service.py`**

Added proper error handling to the `update_booking()` function to catch HTTP 404 responses and return the API spec-compliant error response:
```python
def update_booking(appointment_id: int, data):
    try:
        return update_appointment(appointment_id, data)
    except HTTPError as e:
        if e.response.status_code == 404:
            raise HTTPException(status_code=404, detail="Appointment not found")
        raise
```

### ✅ Specification Compliance:
- **Endpoint**: PUT /appointments/{id} ✓
- **Request body**: Accepts `time` and `status` fields ✓
- **Response**: Returns full appointment object with id, user, time, status ✓
- **Error handling**: Returns 404 with detail "Appointment not found" ✓
- **No modifications**: All existing endpoints remain unchanged ✓

The implementation now fully satisfies the API specification and will properly propagate 404 errors from the backend database service with the correct error response format.