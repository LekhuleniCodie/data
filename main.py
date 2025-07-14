from fastapi import FastAPI
from schemas import ClientCreate, ClientUpdate, Status, TaskCreate, TaskUpdate, RateInfo, Membership, Estimate, ProjectTask, ProjectCreate, ProjectUpdate
from api_client.clockify_client import ClockifyClient
from api_client.linear_client import LinearClient
from db.postgres_handler import PostgresHandler
import clockify_models, linear_models
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

clockify_api_key = os.getenv("API_KEY")
linear_api_key = os.getenv("LINEAR_API_KEY")
workspace_id = os.getenv("WORKSPACE_ID")
# db_url = os.getenv("DB_URL")
db_url = "postgresql+psycopg2://postgres:%40Admin2025@localhost:5432/linear_clockify_db"
handler = PostgresHandler(db_url)


c_client = ClockifyClient(clockify_api_key, workspace_id)
l_client = LinearClient(linear_api_key)
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

@app.get("/clockify_users")
def get_users():
    """
    Retrieve all users in the workspace.
    
    Returns:
        list: List of user objects from Clockify.
    """
    return handler.get_all_as_dicts(clockify_models.User)

# @app.get("/clockify_users_db")
# def get_users():
#     """
#     Retrieve all users in the workspace.
    
#     Returns:
#         list: List of user objects from Clockify.
#     """
    

@app.get("/clockify_clients")
def get_clients():
    """
    Retrieve all clients in the workspace.
    
    Returns:
        list: List of client objects from Clockify.
    """
    return handler.get_all_as_dicts(clockify_models.Client)

@app.get("/clockify_projects")
def get_projects():
    """
    Retrieve all projects in the workspace.
    
    Returns:
        list: List of project objects from Clockify.
    """
    return handler.get_all_as_dicts(clockify_models.Project)

@app.get("/clockify_tasks")
def get_tasks():
    """
    Retrieve all tasks across all projects in the workspace.
    
    Returns:
        list: List of task objects from Clockify.
    """
    return handler.get_all_as_dicts(clockify_models.Task)

@app.get("/clockify_time_entries")
def get_time_entries():
    """
    Retrieve all time entries for all users in the workspace.
    
    Returns:
        list: List of time entry objects from Clockify.
    """
    return handler.get_all_as_dicts(clockify_models.TimeEntry)

@app.post("/clockify_clients")
def post_client(client: ClientCreate):
    """
    Create a new client in the workspace.

    Args:
        client (ClientCreate): Payload containing client info.

    Returns:
        dict: Created client or error message.
    """
    dat = client.model_dump()
    result = c_client.post_data(data_type="client", data=dat)
    if result is None:
        return {"error": "Failed to create client."}
    return result

@app.post("/clockify_projects")
def post_project(project: ProjectCreate):
    """
    Create a new project in the workspace.

    Args:
        project (ProjectCreate): Payload containing project info.

    Returns:
        dict: Created project or error message.
    """
    dat = project.model_dump()
    result = c_client.post_data(data_type="project", data=dat)
    if result is None:
        return {"error": "Failed to create client."}
    return result

@app.post("/clockify_tasks")
def post_task(task: TaskCreate, project_id: str):
    """
    Create a new task within a given project.

    Args:
        task (TaskCreate): Payload containing task info.
        project_id (str): ID of the project to assign the task to.

    Returns:
        dict: Created task or error message.
    """
    dat = task.model_dump()
    result = c_client.post_data(data_type="task", data=dat, url_params={"project_id":project_id})
    if result is None:
        return {"error": "Failed to create client."}
    return result


@app.put("/clockify_clients")
def update_client(client: ClientUpdate, client_id:str):
    """
    Update an existing client.

    Args:
        client (ClientUpdate): Payload with updated client info.
        client_id (str): ID of the client to update.

    Returns:
        dict: Updated client or error message.
    """
    dat = client.model_dump()
    result = c_client.put_data(data_type="client", data=dat, url_params={"client_id":client_id})
    if result is None:
        return {"error": "Failed to update client."}
    return result


@app.put("/clockify_projects")
def update_project(project: ProjectUpdate, project_id:str):
    """
    Update an existing project.

    Args:
        project (ProjectUpdate): Payload with updated project info.
        project_id (str): ID of the project to update.

    Returns:
        dict: Updated project or error message.
    """
    dat = project.model_dump()
    result = c_client.put_data(data_type="project", data=dat, url_params={"project_id":project_id})
    if result is None:
        return {"error": "Failed to update project."}
    return result


@app.put("/clockify_tasks")
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
    dat = task.model_dump()
    result = c_client.put_data(data_type="task", data=dat, url_params={"task_id":task_id, "project_id":project_id})
    if result is None:
        return {"error": "Failed to update task."}
    return result


@app.get("/linear_users")
def get_clients():
    response = l_client.get_data("users")

    if response:
        return response
    else:
        return {"message": "No clients in the linear workspace."}

@app.get("/linear_issues")
def get_issues():
    response = l_client.get_data("issues")

    if response:
        return response
    else:
        return {"message": "No issues in the linear workspace."}

@app.get("/linear_cycles")
def get_cycles():
    response = l_client.get_data("cycles")

    if response:
        return response
    else:
        return {"message": "No cycles in the linear workspace."}
    

@app.get("/linear_projects")
def get_projects():
    response = l_client.get_data("projects")

    if response:
        return response
    else:
        return {"message": "No projects in the linear workspace."}
    
@app.get("/linear_customers")
def get_cycles():
    response = l_client.get_data("customers")

    if response:
        return response
    else:
        return {"message": "No customers in the linear workspace."}
    

@app.get("/linear_teams")
def get_cycles():
    response = l_client.get_data("teams")

    if response:
        return response
    else:
        return {"message": "No teams in the linear workspace."}

    












