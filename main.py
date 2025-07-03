from fastapi import FastAPI
from schemas import ClientCreate, ClientUpdate, Status, TaskCreate, TaskUpdate, RateInfo, Membership, Estimate, ProjectTask, ProjectCreate, ProjectUpdate
from api_client.clockify_client import ClockifyClient
import os
import requests
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

api_key = os.getenv("API_KEY")
workspace_id = os.getenv("WORKSPACE_ID")
db_url = os.getenv("DB_URL")


c_client = ClockifyClient(api_key)

#get requests

@app.get('/')
def run_backend_server():
    return {"message": "Welcome to clockfy_clients backend"}

@app.get("/users")
def get_users():
    return c_client.get_users(workspace_id)

@app.get("/clients")
def get_clients():
    return c_client.get_clients(workspace_id)

@app.get("/projects")
def get_projects():
    return c_client.get_projects(workspace_id)

@app.get("/tasks")
def get_tasks():
    return c_client.get_all_tasks(workspace_id)

@app.get("/time_entries")
def get_time_entries():
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
    data = client.model_dump()
    result = c_client.post_client(workspace_id, data)
    if result is None:
        return {"error": "Failed to create client."}
    return result

@app.post("/projects")
def post_project(project: ProjectCreate):
    data = project.model_dump()
    result = c_client.post_project(workspace_id, data)
    if result is None:
        return {"error": "Failed to create client."}
    return result

@app.post("/tasks")
def post_task(task: TaskCreate, project_id: str):
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
    data = client.model_dump()
    result = c_client.update_client(workspace_id, client_id, data)
    if result is None:
        return {"error": "Failed to update client."}
    return result


@app.put("/projects")
def update_project(project: ProjectUpdate, project_id:str):
    data = project.model_dump()
    result = c_client.update_project(workspace_id, project_id, data)
    if result is None:
        return {"error": "Failed to update project."}
    return result


@app.put("/tasks")
def update_tasks(task: TaskUpdate, task_id:str, project_id:str):
    data = task.model_dump()
    result = c_client.update_task(workspace_id, project_id, task_id, data)
    if result is None:
        return {"error": "Failed to update task."}
    return result







