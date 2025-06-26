from utils.transformer import Transformer
from api_client.clockify_client import ClockifyClient
from db.postgres_handler import PostgresHandler
from models import Client, TimeEntry
import os
import pandas as pd
import json
from sqlalchemy import create_engine, Column, Integer, String, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


pd.set_option('display.max_columns', None)

def main():
    engine = create_engine("postgresql://myuser:mypassword@localhost:5432/mydatabase")

    metadata = MetaData()
    metadata.reflect(bind=engine)

    timestamps_table = metadata.tables['timestamps']
    column_names = [col.name for col in timestamps_table.columns]





    api_key = os.environ['clockify_api_key']
    workspaceId = os.environ['wID']
    db_url = "postgresql://myuser:mypassword@localhost:5432/mydatabase"


    clockify_requester = ClockifyClient(api_key)
    transformer = Transformer()
    # w_id = clockify_requester.get_workspace_id()

    # print(w_id)


    # users = clockify_requester.get_users(workspaceId)
    # clients = clockify_requester.get_clients(workspaceId)
    # tasks = clockify_requester.get_all_tasks(workspaceId)

    time_entries = clockify_requester.get_all_time_entries(workspaceId)



    # df_users = transformer.process_users(users)
    # df_clients = transformer.process_clients(clients)
    # df_tasks = transformer.process_tasks(tasks)

    df_time_entries = transformer.process_time_entries_user(time_entries)

    df_time_entries.to_csv("time_entries.csv")
    # print(df_time_entries)
    # print(df_time_entries.info())
    # print(df_time_entries.columns.tolist())

    # print(df_clients)

    # handler = PostgresHandler(db_url)

    # # # # # # # handler.insert_users(df_users)
    # handler.insert_clients(df_clients)
    # # # # # handler.insert_tasks(df_tasks)


    # handler.insert_user_time_entries(df_time_entries)

    # time_entry_arr = []

    # for column in TimeEntry.__table__.columns:
    #     time_entry_arr.append(column.name)

    # print(df_time_entries.columns.tolist())
    # print(time_entry_arr)
    # print(column_names)

    # print(df_time_entries.columns.tolist() == time_entry_arr == column_names)




    


if __name__ == "__main__":
    main()