from database import Base
from sqlalchemy import Column, Integer , String , Boolean,Index , ForeignKey

class Dbmanager(Base):
    __tablename__ = 'dbmanager'

    id = Column(Integer, primary_key = True , index = True)
    fname = Column(String)
    lname = Column(String)
    mobile = Column(Integer)

class Users(Base):
    __tablename__ = 'dbmanager_app'
    
    id = Column(Integer, primary_key = True , index = True)
    fname = Column(String)
    lname = Column(String)
    mobile = Column(Integer, unique=True)
    email = Column(Integer, unique=True)
    hashed_pw = Column(String)
    notes = Column(String , ForeignKey("dbmanager.id"))

