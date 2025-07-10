from prefect import task, flow
from api_client.clockify_client import ClockifyClient
from api_client.linear_client import LinearClient
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
clockify_api_key = os.getenv("API_KEY")
linear_api_key = os.getenv("LINEAR_API_KEY")
workspace_id = os.getenv("WORKSPACE_ID")
db_url = "postgresql+psycopg2://postgres:%40Admin2025@localhost:5432/linear_clockify_db"

clockify_requester = ClockifyClient(clockify_api_key)
linear_requester = LinearClient(linear_api_key)
transformer = Transformer()
handler = PostgresHandler(db_url)


@task(log_prints=True)
def fetch_clients():
    return clockify_requester.get_clients(workspace_id)

@task(log_prints=True)
def process_clients(clients):
    return transformer.process_clockify_clients(clients)

@task(log_prints=True)
def insert_clients(df_clients):
    handler.insert_clockify_clients(df_clients)


@task(log_prints=True)
def fetch_users():
    return clockify_requester.get_users(workspace_id)

@task(log_prints=True)
def process_users(users):
    return transformer.process_clockify_users(users)

@task(log_prints=True)
def insert_users(df_users):
    handler.insert_clockify_users(df_users)

@task(log_prints=True)
def fetch_tasks():
    return clockify_requester.get_all_tasks(workspace_id)

@task(log_prints=True)
def process_tasks(tasks):
    return transformer.process_clockify_tasks(tasks)

@task(log_prints=True)
def insert_tasks(df_tasks):
    handler.insert_clockify_tasks(df_tasks)

@task(log_prints=True)
def fetch_entries():
    return clockify_requester.get_all_time_entries(workspace_id)

@task(log_prints=True)
def process_entries(entries):
    return transformer.process_clockify_time_entries_user(entries)

@task(log_prints=True)
def insert_entries(df_entries):
    handler.insert_clockify_user_time_entries(df_entries)

@task(log_prints=True)
def fetch_projects():
    return clockify_requester.get_projects(workspace_id)

@task(log_prints=True)
def process_projects(projects):
    return transformer.process_clockify_projects(projects)

@task(log_prints=True)
def insert_projects(df_projects):
    handler.insert_clockify_projects(df_projects)

@task(log_prints=True)
def query_linear_clients():
    return linear_requester.query_users()

@task(log_prints=True)
def process_linear_users(users):
    return transformer.process_linear_users(df_users)

@task 
def insert_linear_users(df_users):
    return handler.insert_linear_users(df_users)

@task(log_prints=True)
def query_linear_projects():
    return linear_requester.query_projects()

@task(log_prints=True)
def process_linear_projects(projects):
    return transformer.process_linear_projects(projects)

@task
def insert_linear_projects(df_projects):
    return handler.insert_linear_projects(df_projects)


@task(log_prints=True)
def query_linear_teams():
    return linear_requester.query_teams()

@task(log_prints=True)
def process_linear_teams(teams):
    return transformer.process_linear_teams(teams)

@task
def insert_linear_teams(df_teams):
    return handler.insert_linear_teams(df_teams)


@task(log_prints=True)
def query_linear_issues():
    return linear_requester.query_issues()

@task(log_prints=True)
def process_linear_issues(issues):
    return transformer.process_linear_issues(issues)

@task
def insert_linear_issues(df_issues):
    return handler.insert_linear_issues(df_issues)


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



@task(log_prints=True)
def query_linear_clients():
    return linear_requester.query_users()

@task(log_prints=True)
def process_linear_users(users):
    return transformer.process_linear_users(users)

@task
def insert_linear_users(df_users):
    return handler.insert_linear_users(df_users)


@task(log_prints=True)
def query_linear_teams():
    return linear_requester.query_teams()

@task(log_prints=True)
def process_linear_teams(teams):
    return transformer.process_linear_teams(teams)

@task
def insert_linear_teams(df_teams):
    return handler.insert_linear_teams(df_teams)


@task(log_prints=True)
def query_linear_projects():
    return linear_requester.query_projects()

@task(log_prints=True)
def process_linear_projects(projects):
    return transformer.process_linear_projects(projects)

@task
def insert_linear_projects(df_projects):
    return handler.insert_linear_projects(df_projects)


@task(log_prints=True)
def query_linear_issues():
    return linear_requester.query_issues()

@task(log_prints=True)
def process_linear_issues(issues):
    return transformer.process_linear_issues(issues)

@task
def insert_linear_issues(df_issues):
    return handler.insert_linear_issues(df_issues)


@flow(name="Linear Full ETL")
def linear_etl():
    """
    Executes a full ETL (Extract, Transform, Load) pipeline for Linear data.

    Steps:
    1. Extract data from the Clockify API:
        - Users
        - Teams
        - Issues
        - Projects
        - Cycles and Customers are still pending..
    2. Transform the raw data into cleaned, structured DataFrames using custom transformers.
    3. Load the transformed data into a PostgreSQL database using SQLAlchemy.

    This flow provides a reproducible way to synchronize data from Linear into
    a local or remote database for further analysis or integration.
    """
    # Users
    raw_users = query_linear_clients()
    df_users = process_linear_users(raw_users)
    insert_linear_users(df_users)

    # Teams
    raw_teams = query_linear_teams()
    df_teams = process_linear_teams(raw_teams)
    insert_linear_teams(df_teams)

    # Projects
    raw_projects = query_linear_projects()
    df_projects = process_linear_projects(raw_projects)
    insert_linear_projects(df_projects)

    # Issues
    raw_issues = query_linear_issues()
    df_issues = process_linear_issues(raw_issues)
    insert_linear_issues(df_issues)



if __name__ == "__main__":
    clockify_etl()
    linear_etl()
