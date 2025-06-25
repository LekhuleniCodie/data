from sqlalchemy import Column, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Clients(Base):
    __tablename__ = "clients"

    id = Column(String(50), primary_key=True)
    name = Column(String(50))
    email = Column(String(50))
    workspace_id = Column(String(50))
    archived = Column(Boolean)
    address = Column(String(50))
    note = Column(String(50))
    currency_id = Column(String(50))
    currency_code = Column(String(50))
