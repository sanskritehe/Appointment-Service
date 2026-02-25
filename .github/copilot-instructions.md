# Copilot Instructions – Appointment Service

## 1. Service Overview

This repository implements the `appointment-service`.

Purpose:
- Handle business logic for booking, listing, updating, and cancelling appointments.
- Communicate with the `appointment-database-service` via HTTP.
- Must NOT directly access any database.

This service:
- Uses FastAPI.
- Uses Pydantic for request/response models.
- Uses a service layer for business logic.
- Uses a separate DB client for inter-service calls.

---

## 2. Architecture Rules

Strict separation of concerns must be maintained:

- `routes/` → Only define API endpoints.
- `services/` → Contain business logic.
- `db_client.py` → Only responsible for HTTP calls to DB service.
- `models.py` → Pydantic schemas.
- `config.py` → Configuration constants.
- `main.py` → App initialization only.

Business logic must NEVER be placed inside routes.
Database calls must NEVER be made directly from routes.

---

## 3. Inter-Service Communication

The Appointment Service must:

- Call the Database Service using `requests`.
- Use `DB_SERVICE_URL` from `config.py`.
- Never hardcode database URLs.
- Never directly access a database.
- Handle HTTP errors using `raise_for_status()`.

The DB service endpoints follow:
- POST   /appointments
- GET    /appointments

Do not modify DB endpoints unless explicitly instructed.

---

## 4. Coding Conventions

- Use FastAPI decorators.
- Use Pydantic models for request validation.
- Keep endpoints minimal.
- Return JSON responses.
- Maintain current response structures.
- Use clean function naming.

---

## 5. Business Logic Rules

This service is responsible for:

- Booking appointments.
- Adding validation logic.
- Enforcing appointment rules.
- Adding future rules like:
  - Prevent double booking.
  - Validate time format.
  - Restrict cancellation based on status.

Business rules must be implemented inside `services/booking_service.py`.

Do NOT implement business rules inside DB client.

---

## 6. When Adding New Features

Follow this flow:

1. Define or extend Pydantic schema in `models.py`.
2. Add endpoint in `routes/`.
3. Add business logic in `services/`.
4. If DB interaction is required, modify `db_client.py`.
5. Maintain compatibility with existing structure.

Do not refactor unrelated files.

---

## 7. Testing Requirements

When implementing new features:

- Create pytest test cases.
- Cover:
  - Successful booking.
  - Failure scenarios.
  - Invalid input cases.
- Mock DB service calls where needed.

---

## 8. AI Modification Rules

When modifying this repository:

1. Analyze existing structure before writing code.
2. Reuse existing patterns.
3. Avoid rewriting entire files.
4. Add minimal necessary changes.
5. Maintain backward compatibility.
6. Preserve existing API behavior unless explicitly instructed.

---

## 9. Constraints

- This service must remain independent from database logic.
- No direct SQLAlchemy usage.
- No database sessions.
- No schema migrations.
- No cross-service business logic inside DB layer.

This is strictly a business logic and API gateway service.