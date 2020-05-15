# API Specification

Unless otherwise noted, all actions return 200 on success; those
referencing a task ID return 404 if the ID is not found. The response
body is empty unless specified otherwise. All non-empty response
bodies are JSON. All actions that take a request body are JSON (not
form-encoded).

Task IDs are unique integers, 1 or greater.

## GET /tasks/

Return a list of tasks on the todo list, 
in the format {"id": <task_id>, "summary": \<one-line summary\>}

## GET /tasks/<task_id>/

Fetch all available information for a specific todo item, in the format 
{"id": <task_id>, "summary": \<one-line summary\>, "description" : \<free-form text field\>}

## POST /tasks/

Create a new todo item. 
The POST body is a JSON object with two fields: 
"summary" (must be under 120 characters, no newline), and 
"description" (free-form text field). 
The response is an object with one field: the id created by the server. 
On success, return 201 status.

## DELETE /tasks/<task_id>/

Mark the item as done. 
(I.e., strike it off the list, so GET /tasks will not show it.)
The response body is empty.

## PUT /tasks/<task_id>/

Modify an existing task. 
The PUT body is a JSON object with two fields: 
"summary" (must be under 120 characters, no newline), and 
"description" (free-form text field).
