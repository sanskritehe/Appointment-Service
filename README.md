Adding Appointment-Service

## Delete Appointment API

The service provides an endpoint to delete an existing appointment by its unique identifier.

### Endpoint
```
DELETE /appointments/{id}
```

### Description
Remove the appointment resource specified by `id`. Returns `204 No Content` on success or `404 Not Found` if the appointment does not exist.
