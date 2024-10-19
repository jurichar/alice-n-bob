"""
tests.py is the file that contains the tests for the FastAPI application.
"""

import os
import dotenv
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import Base, init_db
from main import app


"""
------------ Test setup ------------
"""

dotenv.load_dotenv()
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db():
    init_db()
    session = SessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)


client = TestClient(app)


"""
------------ Tests ------------
"""


def test_counts(db):
    response = client.get("/counts")
    assert response.status_code == 200
    assert response.json() == {"message": "ok"}
