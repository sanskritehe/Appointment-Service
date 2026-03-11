# Appointment Service – API Implementation Prompt

You are an AI development agent working on the **Appointment-Service** repository.

## Goal

Implement REST APIs for managing appointments and integrate with the **Appointment-Database-Service**.
This service handles **business logic** and calls the database service for data persistence.

Database Service URL:

```
http://localhost:8001
```

---

## Tech Stack

* **FastAPI** – API framework
* **Pydantic** – request validation
* **requests** – HTTP calls to database service
* Layered architecture (routes → services → db_client)

Configuration:

```python
# app/config.py
DB_SERVICE_URL = "http://localhost:8001"
```

---

## Data Models

**AppointmentCreate**

```
user : string
time : string
```

**AppointmentUpdate**

```
time : string
```

**AppointmentResponse**

```
id : int
user : string
time : string
status : string
```

---

## APIs

### Create Appointment

```
POST /appointments
```

Flow:

1. Validate request with `AppointmentCreate`
2. Call `create_appointment()` in `db_client`
3. Return created appointment

---

### Get All Appointments

```
GET /appointments
```

Flow:

1. Call `get_all_appointments()` in `db_client`
2. Return appointment list

---

### Update Appointment

```
PUT /appointments/{appointment_id}
```

Flow:

1. Validate with `AppointmentUpdate`
2. Call `update_appointment()` in `db_client`
3. Return updated appointment

---

### Cancel Appointment

```
DELETE /appointments/{appointment_id}
```

Flow:

1. Call `cancel_appointment()` in `db_client`
2. Return confirmation response

Example:

```json
{
  "message": "Appointment deleted successfully",
  "appointment_id": 5
}
```

---

## Architecture

```
app/
├─ models/        # Pydantic models
├─ routes/        # FastAPI endpoints
├─ services/      # business logic
├─ db_client.py   # calls database service
└─ config.py      # configuration
```

Layer responsibilities:

* **routes** → API endpoints
* **services** → business logic
* **db_client** → calls database APIs using `requests`

All external calls must include:

```python
response.raise_for_status()
```

---

## Implementation Steps

1. Update **db_client.py**

   * create_appointment
   * get_all_appointments
   * update_appointment
   * cancel_appointment

2. Update **services/booking_service.py**

   * book_appointment
   * list_appointments
   * update_booking
   * cancel_booking

3. Update **routes/appointments.py**

```
POST   /appointments
GET    /appointments
PUT    /appointments/{appointment_id}
DELETE /appointments/{appointment_id}
```

---

## After Implementation

Create branch:

```
feature/cancel-appointment-api
```

Commit and push:

```
git add .
git commit -m "Add cancel appointment API"
git push origin feature/cancel-appointment-api
```

Create a **Pull Request** to merge into `main`.
