# Generic Service Layer – CRUD Integration Prompt

You are an AI development agent working on a **Service Layer repository**.

## Goal

Implement REST APIs that handle business logic and integrate with an external **Database Service**.

This service does NOT manage persistence directly.

---

## Runtime Context (Provided Dynamically)

* Resource: {resource}
* Fields: {fields}
* Database Service URL: {db_service_url}

---

## Responsibilities

* Validate incoming requests
* Apply business logic
* Call database service APIs
* Return structured responses

---

## Tech Stack

* FastAPI
* Pydantic
* requests

---

## APIs

### Create

POST /{resource}

Flow:

1. Validate request body
2. Call DB service POST /{resource}
3. Return response

---

### Read All

GET /{resource}

Flow:

1. Call DB service GET /{resource}
2. Return list

---

### Read by ID

GET /{resource}/{id}

Flow:

1. Call DB service GET /{resource}/{id}
2. Return result

---

### Update

PUT /{resource}/{id}

Flow:

1. Validate request
2. Call DB service PUT /{resource}/{id}
3. Return updated response

---

### Delete

DELETE /{resource}/{id}

Flow:

1. Call DB service DELETE /{resource}/{id}
2. Return confirmation

---

## Architecture

app/
├─ models/
├─ routes/
├─ services/
├─ db_client.py
└─ config.py

---

## Layer Responsibilities

* routes → API endpoints
* services → business logic
* db_client → external API calls

---

## Implementation Rules

* Use Pydantic for validation
* Keep routes minimal
* Place logic in services
* Use requests for HTTP calls

All external calls must include:

```python
response.raise_for_status()
```

---

## Validation

* Ensure API calls succeed
* Handle HTTP errors properly
* Validate request and response formats

---

## After Implementation

* Create feature branch
* Commit changes
* Push to repository
* Create Pull Request
