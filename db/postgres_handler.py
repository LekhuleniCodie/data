from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Client, User, Task, TimeEntry
from sqlalchemy.orm import Session as SessionType  
from sqlalchemy.dialects.postgresql import insert  

class PostgresHandler:

    def __init__(self, db_conn_url: str):
        self.db_conn_url = db_conn_url

        
        self.engine = create_engine(self.db_conn_url, echo=False)

        
        self.SessionLocal = sessionmaker(bind=self.engine)

    def insert_to_db(self, df, mod_class):
        records = df.to_dict(orient="records")

        if not records:
            return False  # nothing to insert

        qry = insert(mod_class).values(records)

        #duplicate keys?
        qry = qry.on_conflict_do_nothing(index_elements=['id'])

        with self.SessionLocal() as session:
            result = session.execute(qry)
            session.commit()

        return result.rowcount > 0 


    def insert_clients(self, df):
        result = self.insert_to_db(df, Client)

        if result:
            print("Clients insertion success.")
        else:
            print("Clients insertion failed.")

        


    def insert_users(self, df):
        result = self.insert_to_db(df, User)

        if result:
            print("Users insertion success.")
        else:
            print("User insertion failed.")

    
    def insert_tasks(self, df):
        result = self.insert_to_db(df, Task)

        if result:
            print("Tasks insertion success.")
        else:
            print("Tasks insertion failed.")

    def insert_user_time_entries(self, df):
        
        result = self.insert_to_db(df, TimeEntry)

        if result:
            print("Time entries insertion success.")
        else:
            print("Time entries insertion failed.")
