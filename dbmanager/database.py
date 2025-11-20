from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Base class for ORM models
Base = declarative_base()

# Database URL
SQL_DB_URL = "sqlite:///dbmanager_app.db"

# Engine (connect_args needed for SQLite in multi-threaded apps)
engine = create_engine(SQL_DB_URL, connect_args={"check_same_thread": False})

# Session factory
SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)
