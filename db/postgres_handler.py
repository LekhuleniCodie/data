from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session as SessionType
from sqlalchemy.dialects.postgresql import insert
from typing import Type, Any
import pandas as pd

from models import Client, User, Task, TimeEntry, Project


class PostgresHandler:
    """
    Handles PostgreSQL interactions using SQLAlchemy.
    Provides methods to insert DataFrames into database tables, handling conflict resolution on primary keys.
    """

    def __init__(self, db_conn_url: str):
        """
        Initializes the database engine and session factory.

        Args:
            db_conn_url (str): The SQLAlchemy connection string to the database.
        """
        try:
            self.db_conn_url = db_conn_url
            self.engine = create_engine(self.db_conn_url, echo=False)
            self.SessionLocal = sessionmaker(bind=self.engine)
            print("DB connection initialized successfully.")
        except Exception as e:
            print("Failed to initialize DB connection.")
            print(f"Error: {e}")
            raise

    def insert_to_db(self, df: pd.DataFrame, mod_class: Type[Any]) -> bool:
        """
        Inserts a DataFrame into a specified database table using SQLAlchemy.

        Args:
            df (pd.DataFrame): The DataFrame to insert.
            mod_class (Base): SQLAlchemy ORM model class representing the table.

        Returns:
            bool: True if any rows were affected, False otherwise.
        """
        records = df.to_dict(orient="records")
        if not records:
            return False

        qry = insert(mod_class).values(records)

        # Define conflict handling: update all columns except 'id'
        updated_cols = {
            col.name: qry.excluded[col.name]
            for col in mod_class.__table__.columns
            if col.name != "id"
        }

        qry = qry.on_conflict_do_update(
            index_elements=['id'],
            set_=updated_cols
        )

        with self.SessionLocal() as session:
            result = session.execute(qry)
            session.commit()

        return result.rowcount > 0

    def insert_clients(self, df: pd.DataFrame) -> None:
        """
        Inserts client records into the database.

        Args:
            df (pd.DataFrame): DataFrame containing client data.
        """
        result = self.insert_to_db(df, Client)
        print("Clients insertion success." if result else "Clients insertion failed.")

    def insert_users(self, df: pd.DataFrame) -> None:
        """
        Inserts user records into the database.

        Args:
            df (pd.DataFrame): DataFrame containing user data.
        """
        result = self.insert_to_db(df, User)
        print("Users insertion success." if result else "Users insertion failed.")

    def insert_tasks(self, df: pd.DataFrame) -> None:
        """
        Inserts task records into the database.

        Args:
            df (pd.DataFrame): DataFrame containing task data.
        """
        result = self.insert_to_db(df, Task)
        print("Tasks insertion success." if result else "Tasks insertion failed.")

    def insert_user_time_entries(self, df: pd.DataFrame) -> None:
        """
        Inserts time entry records into the database.

        Args:
            df (pd.DataFrame): DataFrame containing time entry data.
        """
        result = self.insert_to_db(df, TimeEntry)
        print("Time entries insertion success." if result else "Time entries insertion failed.")

    def insert_projects(self, df: pd.DataFrame) -> None:
        """
        Inserts project records into the database.

        Args:
            df (pd.DataFrame): DataFrame containing project data.
        """
        result = self.insert_to_db(df, Project)
        print("Projects insertion success." if result else "Projects insertion failed.")
