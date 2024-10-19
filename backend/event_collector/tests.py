"""
tests.py is the file that contains the tests for the FastAPI application.
"""

import os
import dotenv
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from functions import create_delivery, update_delivery_state
from utils import generate_name
from config import Base, init_db
from main import app
from models import Delivery, Event, DeliveryState


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


def test_create_delivery(db):
    delivery_id = generate_name()
    delivery = create_delivery(db, delivery_id)
    assert delivery.id == delivery_id


def test_update_delivery_state(db):
    delivery_id = generate_name()
    delivery = create_delivery(db, delivery_id)
    updated_delivery = update_delivery_state(db, delivery, DeliveryState.CRASHED)
    assert updated_delivery.state == DeliveryState.CRASHED
