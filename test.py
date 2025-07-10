import os
import pandas as pd
import json
from utils.transformer import Transformer
from api_client.linear_client import LinearClient
from db.postgres_handler import PostgresHandler
pd.set_option('display.max_columns', None) 
from sqlalchemy import create_engine


def main():
    DATABASE_URL = "postgresql+psycopg2://postgres:%40Admin2025@localhost:5432/linear_clockify_db"


    api_key = os.getenv("LINEAR_API_KEY")
    linear_client = LinearClient(api_key)
    json_dat = linear_client.query_issues()
    transformer = Transformer()
    linear_users_df = transformer.process_linear_issues(json_dat)
    handler = PostgresHandler(DATABASE_URL)

    print(linear_users_df.info())

    handler.insert_linear_issues(linear_users_df)


if __name__=="__main__":
    main() 