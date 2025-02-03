"""
Script for connecting to the databse
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

USER = os.environ.get("POSTGRES_USER")
PASSWD = os.environ.get("POSTGRES_PASSWORD")

SQLALCHEMY_DATABASE_URL = f"postgresql://{USER}:{PASSWD}@localhost/newpostgres"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
