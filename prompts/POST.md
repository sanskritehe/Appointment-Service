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
