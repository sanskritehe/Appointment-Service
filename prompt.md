# Copilot Agent – POST Endpoint Implementation

You are an AI coding agent. Your task is to implement a POST (create) REST API endpoint.

These instructions are generic and apply to ANY repository and ANY resource.

---

## Step 1 – Read the Jira Ticket

Use the Jira tool to fetch the ticket provided.

Extract:
- The resource name (e.g. "appointment", "user", "order")
- The endpoint to implement (e.g. POST /appointments)
- Any specific business logic called out
- The Confluence page reference for the API spec

---

## Step 2 – Fetch API Specification from Confluence

Use the Confluence tool to fetch the page referenced in the Jira ticket.

Find the section for the POST endpoint of the resource.

Extract:
- The exact endpoint path
- The exact request body JSON format
- The exact response JSON format
- Any validation rules

---

## Step 3 – Read Existing Code

Use the GitHub tool to read the existing implementation files in the repository.

Understand:
- How existing endpoints are structured
- How new records are created and saved
- How responses are returned
- What imports are already present

DO NOT modify any already implemented endpoints.

---

## Step 4 – Implement the POST Endpoint

A POST endpoint must:
- Accept the request body matching the Confluence spec
- Validate required fields
- Create a new resource record
- Save and return the created resource
- Return appropriate HTTP status (201 Created where possible)
- Follow the exact same code style as existing endpoints
- Use dependency injection for sessions or clients
- Return a JSON-serializable response

---

## Step 5 – Create a Branch

Use the GitHub tool to create a new branch:
- Branch name: feature/{jira-ticket-id}-post-{resource-name}
- Base branch: main

---

## Step 6 – Push the Code

Push only the minimal necessary changes to the feature branch.

Commit message format:
"[{jira-ticket-id}] Implement POST /{resource} endpoint"

---

## Step 7 – Raise a Pull Request

Create a PR with:
- Title: [{jira-ticket-id}] Implement POST /{resource}
- Body: what was implemented, files changed, Jira and Confluence references
- Head: feature branch
- Base: main

---

## Rules

- Never modify already working endpoints
- Always validate request body against Confluence spec
- Always follow existing code style
- Always follow the Confluence spec for request/response format
- Minimal changes only — do not refactor unrelated code


---

## Live Context for This Ticket

### Jira Ticket: KAN-9
**Summary:**  Create POST endpoint for booking an appointment
**Status:** To Do
**Priority:** Medium
**Labels:** none
**URL:** https://hpe-team2.atlassian.net/browse/KAN-9

**Description:**
Create a new POST /appointments endpoint that allows patients to book an appointment with a doctor.   Requirements: Accept patient ID, doctor ID, appointment date, and time slot Validate that the time slot is available before confirming Return a booking confirmation with a generated appointment ID Store the appointment record in the database Return 409 Conflict if the slot is already taken

---

### API Specification (from Confluence: API Development Guidelines)
**Source:** https://hpe-cpp-team2.atlassian.net/wiki/spaces/hpeteam2/pages/5505025/API+Development+Guidelines

API Specifications &ndash; Appointment Database Service This page defines the complete API specifications for the Appointment Database Service. All request and response formats are defined here as the single source of truth. === ALREADY IMPLEMENTED === API 1: Create Appointment Endpoint: POST /appointments Request: { &quot;user&quot;: &quot;string&quot;, &quot;time&quot;: &quot;string&quot; } Response: { &quot;id&quot;: 1, &quot;user&quot;: &quot;string&quot;, &quot;time&quot;: &quot;string&quot;, &quot;status&quot;: &quot;booked&quot; } API 2: Get All Appointments Endpoint: GET /appointments Response: [ { &quot;id&quot;: 1, &quot;user&quot;: &quot;string&quot;, &quot;time&quot;: &quot;string&quot;, &quot;status&quot;: &quot;booked&quot; } ] API 3: Delete Appointment Endpoint: DELETE /appointments/{id} Request: appointment_id as path parameter Response: { &quot;message&quot;: &quot;Appointment deleted successfully&quot;, &quot;appointment_id&quot;: 1 } Error Response (404): { &quot;detail&quot;: &quot;Appointment not found&quot; } === TO BE IMPLEMENTED === API 4: Update Appointment Endpoint: PUT /appointments/{id} Request: appointment_id as path parameter Body: { &quot;time&quot;: &quot;string&quot;, &quot;status&quot;: &quot;string&quot; } Response: { &quot;id&quot;: 1, &quot;user&quot;: &quot;string&quot;, &quot;time&quot;: &quot;string&quot;, &quot;status&quot;: &quot;string&quot; } Error Response (404): { &quot;detail&quot;: &quot;Appointment not found&quot; }
