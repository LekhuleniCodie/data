from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Clients  
from sqlalchemy.orm import Session as SessionType  
from sqlalchemy.dialects.postgresql import insert  

class PostgresHandler:

    def __init__(self, db_conn_url: str):
        self.db_conn_url = db_conn_url

        
        self.engine = create_engine(self.db_conn_url, echo=False)

        
        self.SessionLocal = sessionmaker(bind=self.engine)



    def insert_clients(self, df):
        records = df.to_dict(orient='records')

        qry = insert(Clients).values(records)

        # clashing id?
        qry = qry.on_conflict_do_nothing(index_elements=['id']) 

        with self.SessionLocal() as session:
            session.execute(qry)
            session.commit()

        print("Clients inserted.")


    
