"""
Configuration script for testing endpoints with pytest.
Made according to fastAPI documentation
https://fastapi.tiangolo.com/how-to/testing-database/
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db
import app.schemas


from app.main import app

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

@pytest.fixture()
def client():
    """
    Yield test client for tests
    """
    with TestClient(app) as client:
        yield client

@pytest.fixture
def test_db_session():
    """
    Fixture to provide a test database session
    """
    db = TestingSessionLocal()
    yield db
    db.rollback()
    db.close()

