from prefect import task, flow
from api_client.clockify_client import ClockifyClient
from db.postgres_handler import PostgresHandler
from utils.transformer import Transformer
import os
from dotenv import load_dotenv
import json

"""
job_runner.py

This script defines a complete ETL (Extract, Transform, Load) pipeline for integrating data from the Clockify API into a PostgreSQL database using Prefect for orchestration.

The pipeline performs the following steps:
1. Extracts data from Clockify (clients, users, tasks, time entries, and projects) using the ClockifyClient.
2. Transforms the raw API data into cleaned pandas DataFrames using the Transformer utility.
3. Loads the cleaned data into the corresponding PostgreSQL tables via PostgresHandler.

All steps are structured as Prefect tasks, and the entire flow is wrapped in a Prefect flow named "Clockify Full ETL".
Environment variables (API key, workspace ID, and DB URL) are loaded securely via dotenv.

"""


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
    """
    Executes a full ETL (Extract, Transform, Load) pipeline for Clockify data.

    Steps:
    1. Extract data from the Clockify API:
        - Clients
        - Users
        - Tasks
        - Time entries
        - Projects
    2. Transform the raw data into cleaned, structured DataFrames using custom transformers.
    3. Load the transformed data into a PostgreSQL database using SQLAlchemy.

    This flow provides a reproducible way to synchronize data from Clockify into
    a local or remote database for further analysis or integration.
    """
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
