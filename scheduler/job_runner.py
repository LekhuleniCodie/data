from prefect import task, flow
from api_client.clockify_client import ClockifyClient
from db.postgres_handler import PostgresHandler
from utils.transformer import Transformer
import os
from dotenv import load_dotenv
import json

# api_key = os.environ['clockify_api_key']
# workspaceId = os.environ['w_id']
# db_url =  #needs to be safe

load_dotenv()

# Access variables
api_key = os.getenv("API_KEY")
workspace_id = os.getenv("WORKSPACE_ID")
db_url = os.getenv("DB_URL")

clockify_requester = ClockifyClient(api_key)
transformer = Transformer()
handler = PostgresHandler(db_url)


@task(log_prints=True)
def fetch_clients():
    return clockify_requester.get_clients(workspace_id)

@task(log_prints=True)
def process_clients(clients):
    return transformer.process_clients(clients)

@task(log_prints=True)
def insert_clients(df_clients):
    handler.insert_clients(df_clients)


@task(log_prints=True)
def fetch_users():
    return clockify_requester.get_users(workspace_id)

@task(log_prints=True)
def process_users(users):
    return transformer.process_users(users)

@task(log_prints=True)
def insert_users(df_users):
    handler.insert_users(df_users)

@task(log_prints=True)
def fetch_tasks():
    return clockify_requester.get_all_tasks(workspace_id)

@task(log_prints=True)
def process_tasks(tasks):
    return transformer.process_tasks(tasks)

@task(log_prints=True)
def insert_tasks(df_tasks):
    handler.insert_tasks(df_tasks)

@task(log_prints=True)
def fetch_entries():
    return clockify_requester.get_all_time_entries(workspace_id)

@task(log_prints=True)
def process_entries(entries):
    return transformer.process_time_entries_user(entries)

@task(log_prints=True)
def insert_entries(df_entries):
    handler.insert_user_time_entries(df_entries)

@task(log_prints=True)
def fetch_projects():
    return clockify_requester.get_projects(workspace_id)

@task(log_prints=True)
def process_projects(projects):
    return transformer.process_projects(projects)

@task(log_prints=True)
def insert_projects(df_projects):
    handler.insert_projects(df_projects)


@flow(name="Clockify Full ETL")
def clockify_etl():
    # Clients
    clients_raw = fetch_clients()
    df_clients = process_clients(clients_raw)
    insert_clients(df_clients)

    # Users
    users_raw = fetch_users()
    df_users = process_users(users_raw)
    insert_users(df_users)

    # Tasks
    tasks_raw = fetch_tasks()
    df_tasks = process_tasks(tasks_raw)
    insert_tasks(df_tasks)

    # Entries
    entries_raw = fetch_entries()
    df_entries = process_entries(entries_raw)
    insert_entries(df_entries)

    # Projects
    projects_raw = fetch_projects()
    df_projects = process_projects(projects_raw)
    insert_projects(df_projects)


if __name__ == "__main__":
    clockify_etl()
