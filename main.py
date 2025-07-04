from fastapi import FastAPI
from schemas import ClientCreate, ClientUpdate, Status, TaskCreate, TaskUpdate, RateInfo, Membership, Estimate, ProjectTask, ProjectCreate, ProjectUpdate
from api_client.clockify_client import ClockifyClient
import os
import requests
from dotenv import load_dotenv

"""
FastAPI backend for interacting with Clockify's API.

This service exposes RESTful endpoints to:
- Retrieve users, clients, projects, tasks, and time entries from Clockify.
- Create new clients, projects, and tasks.
- Update existing clients, projects, and tasks.

Environment variables required:
- API_KEY: Your Clockify API key.
- WORKSPACE_ID: The ID of the Clockify workspace to target.
"""

load_dotenv()

app = FastAPI()

api_key = os.getenv("API_KEY")
workspace_id = os.getenv("WORKSPACE_ID")
db_url = os.getenv("DB_URL")


c_client = ClockifyClient(api_key)
# ─────────────────────────────────────────
# GET Endpoints
# ─────────────────────────────────────────

@app.get('/')
def run_backend_server():
    """
    Welcome message for the Clockify backend.
    
    Returns:
        dict: A welcome message.
    """
    return {"message": "Welcome to clockfy_clients backend"}

@app.get("/users")
def get_users():
    """
    Retrieve all users in the workspace.
    
    Returns:
        list: List of user objects from Clockify.
    """
    return c_client.get_users(workspace_id)

@app.get("/clients")
def get_clients():
    """
    Retrieve all clients in the workspace.
    
    Returns:
        list: List of client objects from Clockify.
    """
    return c_client.get_clients(workspace_id)

@app.get("/projects")
def get_projects():
    """
    Retrieve all projects in the workspace.
    
    Returns:
        list: List of project objects from Clockify.
    """
    return c_client.get_projects(workspace_id)

@app.get("/tasks")
def get_tasks():
    """
    Retrieve all tasks across all projects in the workspace.
    
    Returns:
        list: List of task objects from Clockify.
    """
    return c_client.get_all_tasks(workspace_id)

@app.get("/time_entries")
def get_time_entries():
    """
    Retrieve all time entries for all users in the workspace.
    
    Returns:
        list: List of time entry objects from Clockify.
    """
    return c_client.get_all_time_entries(workspace_id)

# @app.post("/users")
# def post_user(user: UserCreate):
#     data = user.dict()
#     result = c_client.post_user(workspace_id, data)
#     if result is None:
#         return {"error": "Failed to create user."}
#     return result


@app.post("/clients")
def post_client(client: ClientCreate):
    """
    Create a new client in the workspace.

    Args:
        client (ClientCreate): Payload containing client info.

    Returns:
        dict: Created client or error message.
    """
    data = client.model_dump()
    result = c_client.post_client(workspace_id, data)
    if result is None:
        return {"error": "Failed to create client."}
    return result

@app.post("/projects")
def post_project(project: ProjectCreate):
    """
    Create a new project in the workspace.

    Args:
        project (ProjectCreate): Payload containing project info.

    Returns:
        dict: Created project or error message.
    """
    data = project.model_dump()
    result = c_client.post_project(workspace_id, data)
    if result is None:
        return {"error": "Failed to create client."}
    return result

@app.post("/tasks")
def post_task(task: TaskCreate, project_id: str):
    """
    Create a new task within a given project.

    Args:
        task (TaskCreate): Payload containing task info.
        project_id (str): ID of the project to assign the task to.

    Returns:
        dict: Created task or error message.
    """
    data = task.model_dump()
    result = c_client.post_task(workspace_id, project_id, data)
    if result is None:
        return {"error": "Failed to create client."}
    return result


# @app.post("/time_entries")
# def post_time_entry(time_entry: TimeEntryCreate, user_id: str):
#     data = time_entry.dict()
#     result = c_client.post_time_entry(workspace_id, user_id, data)
#     if result is None:
#         return {"error": "Failed to create client."}
#     return result




@app.put("/clients")
def update_client(client: ClientUpdate, client_id:str):
    """
    Update an existing client.

    Args:
        client (ClientUpdate): Payload with updated client info.
        client_id (str): ID of the client to update.

    Returns:
        dict: Updated client or error message.
    """
    data = client.model_dump()
    result = c_client.update_client(workspace_id, client_id, data)
    if result is None:
        return {"error": "Failed to update client."}
    return result


@app.put("/projects")
def update_project(project: ProjectUpdate, project_id:str):
    """
    Update an existing project.

    Args:
        project (ProjectUpdate): Payload with updated project info.
        project_id (str): ID of the project to update.

    Returns:
        dict: Updated project or error message.
    """
    data
    data = project.model_dump()
    result = c_client.update_project(workspace_id, project_id, data)
    if result is None:
        return {"error": "Failed to update project."}
    return result


@app.put("/tasks")
def update_tasks(task: TaskUpdate, task_id:str, project_id:str):
    """
    Update a task within a given project.

    Args:
        task (TaskUpdate): Payload with updated task info.
        task_id (str): ID of the task to update.
        project_id (str): ID of the project the task belongs to.

    Returns:
        dict: Updated task or error message.
    """
    data = task.model_dump()
    result = c_client.update_task(workspace_id, project_id, task_id, data)
    if result is None:
        return {"error": "Failed to update task."}
    return result







