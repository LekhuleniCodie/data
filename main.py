from utils.transformer import Transformer
from api_client.clockify_client import ClockifyClient
from db.postgres_handler import PostgresHandler
from models import Clients
import os
import pandas as pd
import json
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


pd.set_option('display.max_columns', None)

def main():

    api_key = os.environ['clockify_api_key']
    workspaceId = os.environ['wID']
    db_url = "postgresql://myuser:mypassword@localhost:5432/mydatabase"

    clockify_requester = ClockifyClient(api_key)
    transformer = Transformer()

    users = clockify_requester.get_users(workspaceId)

    df = transformer.process_users(users)

    print(df.info())

    # handler = PostgresHandler(db_url)

    # handler.insert_clients(df)



if __name__ == "__main__":
    main()