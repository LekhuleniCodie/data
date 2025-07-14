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
        #connection creation
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

        # extractiion of all columns to be updated except for the id
        updated_cols = {
            col.name: qry.excluded[col.name]
            for col in mod_class.__table__.columns
            if col.name != "id"
        }

        #when the ids are clasing? update with pleasure!!!

        qry = qry.on_conflict_do_update(
            index_elements=['id'],
            set_=updated_cols
        )

        with self.SessionLocal() as session:
            result = session.execute(qry)
            session.commit()

        if result.rowcount > 0:
            print("DB insertion of {mod_class.__name__} was a success.")
            return True
        else:
            print("DB insertion of {mod_class.__name__} failed.")

    
    # all the methods below make use of the method above


    def insert_linear_projects(self, df: pd.DataFrame):

        """Inserts linear projects into a database and also links the project to the teams assigned to it

        Args:
            df(pd.DataFrame): a dataframe containing linear projects data
        
        """
        team_project_list = [] #array that will store a dict of key-value pairs of team_id and project_id

        for _, row in df.iterrows(): #df rows iteration
            project_id = row["id"] #extract project id
            teams_in_project = row["teams_nodes"] #extract the list of teams in a specific project ie row
            for team in teams_in_project:
                team_id = team["id"]
                team_project_list.append({ #appending to array the key-value pairs of the team_id and the project_id
                    "team_id": team_id,
                    "project_id": project_id
                })


        team_project_df = pd.DataFrame(team_project_list) #convert dict to df (consistency purposes of the pipeline (JSOON -> df -> PostgreSQL))

        df = df.drop("teams_nodes", axis=1) #remove the teams col in the df (preparation for insertion to db)

        self.insert_to_db(df, linear_models.Project)
        self.insert_to_db(team_project_df, linear_models.TeamProject)

    def insert_linear_teams(self, df: pd.DataFrame):

        """Inserts linear teams into a database and also links the teams to the members in it

        Args:
            df(pd.DataFrame): a dataframe containing linear projects data
        
        """
        team_members_list = [] #array to store key-value pairs of a member and the team they belong to

        for _, row in df.iterrows(): #rows of the df itteration
            team_id = row["id"] #extract team id
            users_in_team = row["members_nodes"] #extract users in a specific team

            for user in users_in_team: 
                user_id = user["id"]
                team_members_list.append({ #append key value pair of user_id and team_id
                    "user_id" : user_id, 
                    "team_id" : team_id
                })
        team_users_df = pd.DataFrame(team_members_list)

        df = df.drop("members_nodes", axis=1) #

        self.insert_to_db(df, linear_models.Team) #db insertion in the teams table in the linear_schema

        self.insert_to_db(team_users_df, linear_models.TeamMember)

    ###############################################################################################################
    """These are methods to get data from the db."""

    def get_all_as_dicts(self, model_class):
        with self.SessionLocal() as session:
            records = session.query(model_class).all()
            return [
                {column.name: getattr(record, column.name) for column in model_class.__table__.columns}
                for record in records
            ]
        
    def get_one_as_dict_or_fail(self, model_class, record_id):
        with self.SessionLocal() as session:
            record = session.query(model_class).get(record_id)
            if not record:
                raise ValueError(f"No {model_class.__name__} found with id {record_id}")
            return {column.name: getattr(record, column.name) for column in model_class.__table__.columns}





    def get_clockify_users_db(self): 
        return self.get_all_as_dicts(clockify_models.User)
    
    
    def get_clockify_clients_db(self):
        return self.get_all_as_dicts(clockify_models.Client)

    def get_clockify_tasks_db(self):
        return self.get_all_as_dicts(clockify_models.Task)

    def get_clockify_time_entries_db(self):
        return self.get_all_as_dicts(clockify_models.TimeEntry)

    def get_clockify_projects_db(self):
        return self.get_all_as_dicts(clockify_models.Project)
        
        

