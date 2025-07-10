from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session as SessionType
from sqlalchemy.dialects.postgresql import insert
from typing import Type, Any
import pandas as pd

import clockify_models
import linear_models


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

    def insert_clockify_clients(self, df: pd.DataFrame) -> None:
        """
        Inserts client records into the database.

        Args:
            df (pd.DataFrame): DataFrame containing client data.
        """
        result = self.insert_to_db(df, clockify_models.Client)
        print("Clients insertion success." if result else "Clients insertion failed.")

    def insert_clockify_users(self, df: pd.DataFrame) -> None:
        """
        Inserts user records into the database.

        Args:
            df (pd.DataFrame): DataFrame containing user data.
        """
        result = self.insert_to_db(df, clockify_models.User)
        print("Users insertion success." if result else "Users insertion failed.")

    def insert_clockify_tasks(self, df: pd.DataFrame) -> None:
        """
        Inserts task records into the database.

        Args:
            df (pd.DataFrame): DataFrame containing task data.
        """
        result = self.insert_to_db(df, clockify_models.Task)
        print("Tasks insertion success." if result else "Tasks insertion failed.")

    def insert_clockify_user_time_entries(self, df: pd.DataFrame) -> None:
        """
        Inserts time entry records into the database.

        Args:
            df (pd.DataFrame): DataFrame containing time entry data.
        """
        result = self.insert_to_db(df, clockify_models.TimeEntry)
        print("Time entries insertion success." if result else "Time entries insertion failed.")

    def insert_clockify_projects(self, df: pd.DataFrame) -> None:
        """
        Inserts project records into the database.

        Args:
            df (pd.DataFrame): DataFrame containing project data.
        """
        result = self.insert_to_db(df, clockify_models.Project)
        print("Projects insertion success." if result else "Projects insertion failed.")


    """Insertion to the the linear db"""


    def insert_linear_users(self, df: pd.DataFrame):
        """
        Inserts linear user records into a database

        Args:
            df(pd.DataFrame): a dataframe containing linear users data
        
        """
        result = self.insert_to_db(df, linear_models.User)
        print("Linear users success." if result else "Projects insertion failed.")


    def insert_linear_projects(self, df: pd.DataFrame):

        """Inserts linear projects into a database and also links the project to the teams assigned to it

        Args:
            df(pd.DataFrame): a dataframe containing linear projects data
        
        """
        team_project_list = []

        for _, row in df.iterrows():
            project_id = row["id"]
            teams_in_project = row["teams_nodes"]
            for team in teams_in_project:
                team_id = team["id"]
                team_project_list.append({
                    "team_id": team_id,
                    "project_id": project_id
                })


        team_project_df = pd.DataFrame(team_project_list)

        df = df.drop("teams_nodes", axis=1)

        if self.insert_to_db(df, linear_models.Project):
            print("Linear projects insertion success.")
        else:
            print("Linear projects insertion failed.")

        self.insert_to_db(df, linear_models.Project)
        if self.insert_to_db(team_project_df, linear_models.TeamProject):
            print("Linear team-projects insertion success.")
        else:
            print("Linear team-projects insertion failed.")

    def insert_linear_teams(self, df: pd.DataFrame):

        """Inserts linear teams into a database and also links the teams to the members in it

        Args:
            df(pd.DataFrame): a dataframe containing linear projects data
        
        """
        team_members_list = []

        for _, row in df.iterrows():
            team_id = row["id"]
            users_in_team = row["members_nodes"]

            for user in users_in_team:
                user_id = user["id"]
                team_members_list.append({
                    "user_id" : user_id, 
                    "team_id" : team_id
                })
        team_users_df = pd.DataFrame(team_members_list)

        df = df.drop("members_nodes", axis=1)

        if self.insert_to_db(df, linear_models.Team):
            print("Linear teams insertion success.")
        else:
            print("Linear teams insertion failed")

        if self.insert_to_db(team_users_df, linear_models.TeamMember):
            print("Linear team-members insertion success.")
        else:
            print("Linear team-members insertion failed.")

    def insert_linear_issues(self, df: pd.DataFrame):
        if self.insert_to_db(df, linear_models.Issue):
            print("Linear issues insertion success.")
        else:
            print("Linear issues insertion failed.")

    def insert_linear_cycle(self, df: pd.DataFrame):
        result = self.insert_to_db(df, linear_models.Cycle)


    def insert_linear_customers(self, df: pd.DataFrame):
        result = self.insert_to_db(df, linear_models.Customer)
            
        
        

