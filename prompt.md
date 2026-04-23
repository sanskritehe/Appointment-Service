# Copilot Agent – GET Endpoint Implementation

You are an AI coding agent. Your task is to implement a GET (read) REST API endpoint.

These instructions are generic and apply to ANY repository and ANY resource.

---

## Step 1 – Read the Jira Ticket

Use the Jira tool to fetch the ticket provided.

Extract:
- The resource name (e.g. "appointment", "user", "order")
- The endpoint to implement (e.g. GET /appointments or GET /appointments/{id})
- Any specific business logic called out (e.g. filtering, pagination)
- The Confluence page reference for the API spec

---

## Step 2 – Fetch API Specification from Confluence

Use the Confluence tool to fetch the page referenced in the Jira ticket.

Find the section for the GET endpoint of the resource.

Extract:
- The exact endpoint path
- Whether it returns a single resource or a list
- Any query parameters (filters, pagination)
- The exact response JSON format
- The error response format (especially 404 for single resource)

---

## Step 3 – Read Existing Code

Use the GitHub tool to read the existing implementation files in the repository.

Understand:
- How existing GET endpoints are structured
- How queries are made
- How lists vs single records are returned
- What imports are already present

DO NOT modify any already implemented endpoints.

---

## Step 4 – Implement the GET Endpoint

A GET endpoint must:
- Accept path parameters if fetching a single resource
- Accept query parameters if filtering or paginating
- Query the resource correctly
- Return 404 if a single resource is not found
- Return an empty list (not 404) if a collection has no results
- Follow the exact same code style as existing endpoints
- Use dependency injection for sessions or clients
- Return a JSON-serializable response matching the Confluence spec

---

## Step 5 – Create a Branch

Use the GitHub tool to create a new branch:
- Branch name: feature/{jira-ticket-id}-get-{resource-name}
- Base branch: main

---

## Step 6 – Push the Code

Push only the minimal necessary changes to the feature branch.

Commit message format:
"[{jira-ticket-id}] Implement GET /{resource} endpoint"

---

## Step 7 – Raise a Pull Request

Create a PR with:
- Title: [{jira-ticket-id}] Implement GET /{resource}
- Body: what was implemented, files changed, Jira and Confluence references
- Head: feature branch
- Base: main

---

## Rules

- Never modify already working endpoints
- Always return 404 for missing single resources
- Always return empty list for empty collections
- Always follow existing code style
- Always follow the Confluence spec for response format
- Minimal changes only — do not refactor unrelated code


---

## Live Context for This Ticket

### Jira Ticket: KAN-8
**Summary:** Implement GET endpoint for fetching all appointments
**Status:** To Do
**Priority:** Medium
**Labels:** none
**URL:** https://hpe-team2.atlassian.net/browse/KAN-8

**Description:**
 Implement a GET /appointments endpoint that retrieves all appointments from the database service. Call GET /appointments on the database service at  http://localhost:8001 Return the full list of appointments Return empty list if no appointments exist (not 404) Follow the layered architecture: routes → services → db_client Tech stack: FastAPI, Pydantic, requests

---

### API Specification (from Confluence: API Development Guidelines)
**Source:** https://hpe-cpp-team2.atlassian.net/wiki/spaces/hpeteam2/pages/5505025/API+Development+Guidelines

API Specifications &ndash; Appointment Database Service This page defines the complete API specifications for the Appointment Database Service. All request and response formats are defined here as the single source of truth. === ALREADY IMPLEMENTED === API 1: Create Appointment Endpoint: POST /appointments Request: { &quot;user&quot;: &quot;string&quot;, &quot;time&quot;: &quot;string&quot; } Response: { &quot;id&quot;: 1, &quot;user&quot;: &quot;string&quot;, &quot;time&quot;: &quot;string&quot;, &quot;status&quot;: &quot;booked&quot; } API 2: Get All Appointments Endpoint: GET /appointments Response: [ { &quot;id&quot;: 1, &quot;user&quot;: &quot;string&quot;, &quot;time&quot;: &quot;string&quot;, &quot;status&quot;: &quot;booked&quot; } ] API 3: Delete Appointment Endpoint: DELETE /appointments/{id} Request: appointment_id as path parameter Response: { &quot;message&quot;: &quot;Appointment deleted successfully&quot;, &quot;appointment_id&quot;: 1 } Error Response (404): { &quot;detail&quot;: &quot;Appointment not found&quot; } === TO BE IMPLEMENTED === API 4: Update Appointment Endpoint: PUT /appointments/{id} Request: appointment_id as path parameter Body: { &quot;time&quot;: &quot;string&quot;, &quot;status&quot;: &quot;string&quot; } Response: { &quot;id&quot;: 1, &quot;user&quot;: &quot;string&quot;, &quot;time&quot;: &quot;string&quot;, &quot;status&quot;: &quot;string&quot; } Error Response (404): { &quot;detail&quot;: &quot;Appointment not found&quot; }
