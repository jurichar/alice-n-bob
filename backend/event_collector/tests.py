"""
tests.py is the file that contains the tests for the FastAPI application.
"""

import os
import dotenv
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from functions import (
    create_delivery,
    get_delivery_by_id,
    update_delivery_state,
    get_ongoing_deliveries,
    get_delivery_counts,
    create_event,
    get_events_by_delivery_id,
)
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


def test_create_delivery(db):
    delivery_id = generate_name()
    delivery = create_delivery(db, delivery_id)
    assert delivery.id == delivery_id


def test_get_delivery_by_id(db):
    delivery_id = generate_name()
    create_delivery(db, delivery_id)
    retrieved_delivery = get_delivery_by_id(db, delivery_id)
    assert retrieved_delivery.id == delivery_id


def test_update_delivery_state(db):
    delivery_id = generate_name()
    delivery = create_delivery(db, delivery_id)
    updated_delivery = update_delivery_state(db, delivery, DeliveryState.CRASHED)
    assert updated_delivery.state == DeliveryState.CRASHED


def test_get_ongoing_deliveries(db):
    ongoing_deliveries = [
        create_delivery(db, generate_name()),
        create_delivery(db, generate_name()),
    ]
    ongoing_deliveries[0].state = DeliveryState.PARCEL_DELIVERED
    db.commit()
    ongoing_deliveries = get_ongoing_deliveries(db)
    assert len(ongoing_deliveries) == 1
    assert ongoing_deliveries[0].state == DeliveryState.PARCEL_COLLECTED


def test_get_delivery_counts(db):
    count = get_delivery_counts(db)
    assert count["total"] == 0
    assert count["ongoing"] == 0
    assert count["delivered"] == 0
    assert count["crashed"] == 0
    create_delivery(db, generate_name())
    create_delivery(db, generate_name())
    create_delivery(db, generate_name())
    count = get_delivery_counts(db)
    assert count["total"] == 3
    assert count["ongoing"] == 3
    assert count["delivered"] == 0
    assert count["crashed"] == 0


def test_create_event(db):
    delivery_id = generate_name()
    create_delivery(db, delivery_id)
    event = create_event(db, delivery_id, DeliveryState.PARCEL_COLLECTED)
    assert event.delivery_id == delivery_id
    assert event.type == DeliveryState.PARCEL_COLLECTED


def test_get_events_by_delivery_id(db):
    delivery_id = generate_name()
    create_delivery(db, delivery_id)
    create_event(db, delivery_id, DeliveryState.PARCEL_COLLECTED)
    create_event(db, delivery_id, DeliveryState.TAKEN_OFF)
    create_event(db, delivery_id, DeliveryState.LANDED)
    create_event(db, delivery_id, DeliveryState.CRASHED)
    create_event(db, delivery_id, DeliveryState.PARCEL_DELIVERED)
    events = get_events_by_delivery_id(db, delivery_id)
    assert len(events) == 5
