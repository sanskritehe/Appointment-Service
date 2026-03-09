# Appointment Service – API Implementation Prompt

You are an AI development agent working on the **Appointment-Service** repository.

## Goal

Implement REST APIs for managing appointments and integrate with the **Appointment-Database-Service**.

## Context

Requirements are defined in:

* Jira issue describing appointment APIs
* Confluence page containing the Appointment API schema

The appointment service is responsible for:

* Handling business logic
* Calling the database service APIs

Database service URL:
http://localhost:8001

## APIs to Implement

### 1. Create Appointment

POST /appointments

Request body:
{
"user_id": string,
"doctor_id": string,
"time_slot": string
}

Flow:

1. Validate request using Pydantic model
2. Call database service API to store appointment
3. Return stored appointment

---

### 2. Get All Appointments

GET /appointments

Flow:

1. Call database service
2. Return list of appointments

---

### 3. Cancel Appointment

DELETE /appointments/{appointment_id}

Flow:

1. Accept appointment_id
2. Call database service DELETE API
3. Return cancellation response

---

## Architecture

Follow the existing layered structure:

app/
models/
routes/
services/
db_client.py

Responsibilities:

routes → API endpoints
services → business logic
db_client → calls database service

---

## Implementation Steps

1. Update **db_client.py**

   * Add cancel_appointment function

2. Update **services/booking_service.py**

   * Add cancel_booking function

3. Update **routes/appointments.py**

   * Add DELETE endpoint

4. Ensure clean error handling using raise_for_status()

5. Maintain existing project structure

---

## After Implementation

1. Create new branch:
   feature/cancel-appointment-api

2. Commit changes

3. Push branch to GitHub

4. Create Pull Request
