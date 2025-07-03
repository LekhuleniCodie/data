from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Client, User, Task, TimeEntry, Project
from sqlalchemy.orm import Session as SessionType  
from sqlalchemy.dialects.postgresql import insert  

class PostgresHandler:
    """takes in input of dfs and connects to a db then inserts that df to a df"""

    def __init__(self, db_conn_url: str):
        try: #try creating the db conn
            self.db_conn_url = db_conn_url
            self.engine = create_engine(self.db_conn_url, echo=False)
            self.SessionLocal = sessionmaker(bind=self.engine)
            print("db connection initialized successfully")
        except Exception as e:
            print("Failed to initialize db connection")
            print(f"Error: {e}")
            raise  

    def insert_to_db(self, df, mod_class):
        records = df.to_dict(orient="records") #conversion of the df (cleaned) to a dict

        if not records:
            return False  # nothing to insert

        qry = insert(mod_class).values(records)
        #duplicate keys?
        
        updated_cols = {}

        for col in mod_class.__table__.columns:
            if col.name != "id":  
                updated_cols[col.name] = qry.excluded[col.name]


        qry = qry.on_conflict_do_update(
            index_elements=['id'],
            set_=updated_cols
        )


        with self.SessionLocal() as session:
            result = session.execute(qry) #execute query
            session.commit() #store the changes in db

        return result.rowcount > 0 #tells whether the query was sucessful or not


    def insert_clients(self, df):
        result = self.insert_to_db(df, Client)

        if result:
            print("Clients insertion success.")
        else:
            print("Clients insertion failed.")

        


    def insert_users(self, df):
        """insertion of the users df to db"""
        result = self.insert_to_db(df, User)

        if result:
            print("Users insertion success.")
        else:
            print("User insertion failed.")

    
    def insert_tasks(self, df):
        """insertion of the tasks df to db"""
        result = self.insert_to_db(df, Task)

        if result:
            print("Tasks insertion success.")
        else:
            print("Tasks insertion failed.")

    def insert_user_time_entries(self, df):
        """insertion of the time_entries df to db"""
        result = self.insert_to_db(df, TimeEntry)

        if result:
            print("Time entries insertion success.")
        else:
            print("Time entries insertion failed.")

    
    def insert_projects(self, df):
        """insertion of the projects df to db"""
        result = self.insert_to_db(df, Project)

        if result:
            print("Projects insertion success.")
        else:
            print("Projects insertion failed.")
