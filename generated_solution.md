Perfect! I've successfully implemented the GET /appointments/{id} endpoint (KAN-15) with the following changes:

## Summary of Implementation

**Files Modified:**

1. **`db_client.py`** - Added `get_appointment_by_id()` function
   - Makes HTTP GET request to fetch a single appointment by ID
   - Follows the same pattern as existing functions

2. **`booking_service.py`** - Added `get_appointment()` service function
   - Wraps the database call with error handling
   - Returns 404 with error detail "Appointment not found" when appointment doesn't exist
   - Consistent with existing error handling patterns

3. **`routes/appointments.py`** - Added GET endpoint
   - `@router.get("/{appointment_id}")` handles requests to GET /appointments/{appointment_id}
   - Tagged with KAN-15 reference
   - Returns AppointmentResponse format as specified in Confluence spec

**Implementation Details:**
- ✅ Accepts `appointment_id` as integer path parameter
- ✅ Returns appointment object with id, user, time, and status fields
- ✅ Returns 404 error with `{"detail": "Appointment not found"}` when not found
- ✅ Follows existing code patterns and style
- ✅ Uses dependency injection pattern (FastAPI automatic parameter injection)
- ✅ No existing endpoints were modified

The implementation is minimal, focused, and matches the specification provided in the Jira ticket and Confluence API guidelines.