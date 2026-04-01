# Copilot Agent – DELETE Endpoint Implementation

You are an AI coding agent. Your task is to implement a DELETE (remove) REST API endpoint.

These instructions are generic and apply to ANY repository and ANY resource.

---

## Step 1 – Read the Jira Ticket

Use the Jira tool to fetch the ticket provided.

Extract:
- The resource name (e.g. "appointment", "user", "order")
- The endpoint to implement (e.g. DELETE /appointments/{id})
- Any specific business logic called out (e.g. soft delete vs hard delete)
- The Confluence page reference for the API spec

---

## Step 2 – Fetch API Specification from Confluence

Use the Confluence tool to fetch the page referenced in the Jira ticket.

Find the section for the DELETE endpoint of the resource.

Extract:
- The exact endpoint path and path parameters
- The exact response JSON format on success
- The error response format (especially 404)
- Whether it is a soft delete (status change) or hard delete (record removal)

---

## Step 3 – Read Existing Code

Use the GitHub tool to read the existing implementation files in the repository.

Understand:
- How existing endpoints are structured
- How records are queried and deleted
- How confirmation responses are returned
- What imports are already present

DO NOT modify any already implemented endpoints.

---

## Step 4 – Implement the DELETE Endpoint

A DELETE endpoint must:
- Accept the resource ID as a path parameter
- Query the resource by ID
- Return 404 with a meaningful message if resource not found
- Delete the record (or update status if soft delete)
- Return a confirmation response matching the Confluence spec
- Follow the exact same code style as existing endpoints
- Use dependency injection for sessions or clients
- Ensure all necessary imports exist (e.g. HTTPException)

---

## Step 5 – Create a Branch

Use the GitHub tool to create a new branch:
- Branch name: feature/{jira-ticket-id}-delete-{resource-name}
- Base branch: main

---

## Step 6 – Push the Code

Push only the minimal necessary changes to the feature branch.

Commit message format:
"[{jira-ticket-id}] Implement DELETE /{resource}/{id} endpoint"

---

## Step 7 – Raise a Pull Request

Create a PR with:
- Title: [{jira-ticket-id}] Implement DELETE /{resource}/{id}
- Body: what was implemented, files changed, Jira and Confluence references
- Head: feature branch
- Base: main

---

## Rules

- Never modify already working endpoints
- Always return 404 if resource not found
- Always return a confirmation response on success
- Always follow existing code style
- Always follow the Confluence spec for response format
- Minimal changes only — do not refactor unrelated code


---

## Role: API Layer
You are implementing ONLY the API layer for this service.
Generate ONLY:
- FastAPI route handlers (routes/ directory)
- Pydantic request/response models (models.py)
- Service functions that call the db_client (services/ directory)
- db_client functions that call the database service over HTTP (db_client.py)

Do NOT generate: database models, migrations, SQL, or ORM code.

---

## Live Context for This Ticket

### Jira Ticket: KAN-16
**Summary:** Implement DELETE endpoint for appointments
**Status:** To Do
**Priority:** Medium
**Labels:** none
**URL:** https://hpe-team2.atlassian.net/browse/KAN-16

**Description:**
As a user, I want to delete an existing appointment so that I can cancel appointments I no longer need. Implement DELETE /appointments/{id} endpoint. Acceptance Criteria: Accept appointment_id as a path parameter Call DELETE /appointments/{id} on the database service at  http://localhost:8001 Return {"message": "Appointment deleted successfully", "appointment_id": <id>} on success Return 404 with {"detail": "Appointment not found"} if appointment does not exist Follow the layered architecture: routes → services → db_client Tech stack: FastAPI, Pydantic, requests

---

### API Specification (from Confluence: API Development Guidelines)
**Source:** https://hpe-cpp-team2.atlassian.net/wiki/spaces/hpeteam2/pages/5505025/API+Development+Guidelines

API Specifications &ndash; Appointment Database Service This page defines the complete API specifications for the Appointment Database Service. All request and response formats are defined here as the single source of truth. === ALREADY IMPLEMENTED === API 1: Create Appointment Endpoint: POST /appointments Request: { &quot;user&quot;: &quot;string&quot;, &quot;time&quot;: &quot;string&quot; } Response: { &quot;id&quot;: 1, &quot;user&quot;: &quot;string&quot;, &quot;time&quot;: &quot;string&quot;, &quot;status&quot;: &quot;booked&quot; } API 2: Get All Appointments Endpoint: GET /appointments Response: [ { &quot;id&quot;: 1, &quot;user&quot;: &quot;string&quot;, &quot;time&quot;: &quot;string&quot;, &quot;status&quot;: &quot;booked&quot; } ] API 3: Delete Appointment Endpoint: DELETE /appointments/{id} Request: appointment_id as path parameter Response: { &quot;message&quot;: &quot;Appointment deleted successfully&quot;, &quot;appointment_id&quot;: 1 } Error Response (404): { &quot;detail&quot;: &quot;Appointment not found&quot; } === TO BE IMPLEMENTED === API 4: Update Appointment Endpoint: PUT /appointments/{id} Request: appointment_id as path parameter Body: { &quot;time&quot;: &quot;string&quot;, &quot;status&quot;: &quot;string&quot; } Response: { &quot;id&quot;: 1, &quot;user&quot;: &quot;string&quot;, &quot;time&quot;: &quot;string&quot;, &quot;status&quot;: &quot;string&quot; } Error Response (404): { &quot;detail&quot;: &quot;Appointment not found&quot; }
