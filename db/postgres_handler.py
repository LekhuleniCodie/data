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

        return result.rowcount > 0
    
    # all the methods below make use of the method above

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
        result = self.insert_to_db(df, clockify_models.User) #db insertion to the users table in the clockify_schema
        print("Users insertion success." if result else "Users insertion failed.")

    def insert_clockify_tasks(self, df: pd.DataFrame) -> None:
        """
        Inserts task records into the database.

        Args:
            df (pd.DataFrame): DataFrame containing task data.
        """
        result = self.insert_to_db(df, clockify_models.Task) #db insertion to the tasks table in the clockify_schema
        print("Tasks insertion success." if result else "Tasks insertion failed.")

    def insert_clockify_user_time_entries(self, df: pd.DataFrame) -> None:
        """
        Inserts time entry records into the database.

        Args:
            df (pd.DataFrame): DataFrame containing time entry data.
        """
        result = self.insert_to_db(df, clockify_models.TimeEntry) #db insertion to the time_entries table in the clockify_schema
        print("Time entries insertion success." if result else "Time entries insertion failed.")

    def insert_clockify_projects(self, df: pd.DataFrame) -> None:
        """
        Inserts project records into the database.

        Args:
            df (pd.DataFrame): DataFrame containing project data.
        """
        result = self.insert_to_db(df, clockify_models.Project) #db insertion to the projects table in the clockify_schema
        print("Projects insertion success." if result else "Projects insertion failed.")


    """Insertion to the the linear db"""


    def insert_linear_users(self, df: pd.DataFrame):
        """
        Inserts linear user records into a database

        Args:
            df(pd.DataFrame): a dataframe containing linear users data
        
        """
        result = self.insert_to_db(df, linear_models.User) #insertion to the users table in the the linear_schema
        print("Linear users success." if result else "Projects insertion failed.")


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

        if self.insert_to_db(df, linear_models.Project): #insertion to the projects table in the the linear_schema
            print("Linear projects insertion success.")
        else:
            print("Linear projects insertion failed.")

        if self.insert_to_db(team_project_df, linear_models.TeamProject): #insertion to the TeamProjects table in the linear schema
            print("Linear team-projects insertion success.")
        else:
            print("Linear team-projects insertion failed.")

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

        if self.insert_to_db(df, linear_models.Team): #db insertion in the teams table in the linear_schema
            print("Linear teams insertion success.")
        else:
            print("Linear teams insertion failed")

        if self.insert_to_db(team_users_df, linear_models.TeamMember): #db insertion in the team_members table in the linear_schema
            print("Linear team-members insertion success.")
        else:
            print("Linear team-members insertion failed.")

    def insert_linear_issues(self, df: pd.DataFrame):
        """Inserts Linear issues into a database.

        Args:
            df(pd.DataFrame): a dataframe containing linear issues data
        
        """
        if self.insert_to_db(df, linear_models.Issue): #db insertion to the issues table in the linear_schema
            print("Linear issues insertion success.")
        else:
            print("Linear issues insertion failed.")


    #no data in Linear yet! To be tested after the receipt of data
    def insert_linear_cycle(self, df: pd.DataFrame):
        """Inserts Linear cycles into a database.

        Args:
            df(pd.DataFrame): a dataframe containing linear cycles data
        
        """
        if self.insert_to_db(df, linear_models.Issue):
            print("Linear issues insertion success.")
        else:
            print("Linear issues insertion failed.")
        result = self.insert_to_db(df, linear_models.Cycle)


    def insert_linear_customers(self, df: pd.DataFrame):
        """Inserts Linear customers into a database.

        Args:
            df(pd.DataFrame): a dataframe containing linear customers data
        
        """
        result = self.insert_to_db(df, linear_models.Customer)
            
        
        

