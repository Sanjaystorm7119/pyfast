from database import Base
from sqlalchemy import Column, Integer , String , Boolean,Index

class Dbmanager(Base):
    __tablename__ = 'dbmanager'

    id = Column(Integer, primary_key = True , index = True)
    fname = Column(String)
    lname = Column(String)
    mobile = Column(Integer)
