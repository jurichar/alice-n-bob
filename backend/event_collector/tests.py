"""
tests.py is the file that contains the tests for the FastAPI application.
"""

import os
import dotenv
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timezone, timedelta

from functions import (
    create_delivery,
    get_delivery_by_id,
    reset_db,
    update_delivery_state,
    get_ongoing_deliveries,
    get_delivery_counts,
    create_event,
    get_events_by_delivery_id,
)
from utils import generate_name
from config import Base, init_db
from main import app
from models import DeliveryState, Delivery


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
    assert count["ongoing_deliveries"] == 0
    assert count["total_deliveries"] == 0
    create_delivery(db, generate_name())
    create_delivery(db, generate_name())
    create_delivery(db, generate_name())
    count = get_delivery_counts(db)
    assert count["ongoing_deliveries"] == 3
    assert count["total_deliveries"] == 3


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


def test_post_deliveries_id_event():
    init_db()
    delivery_id = generate_name()
    response = client.post(
        f"/deliveries/{delivery_id}/events", json={"type": "TAKEN_OFF"}
    )
    print(response.json())
    assert response.status_code == 200
    assert response.json()["type"] == "TAKEN_OFF"


def test_get_deliveries():
    init_db()
    response = client.get("/deliveries")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_deliveries_id_events():
    init_db()
    delivery_id = generate_name()
    client.post(f"/deliveries/{delivery_id}/events", json={"type": "TAKEN_OFF"})
    response = client.get(f"/deliveries/{delivery_id}/events")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_counts():
    init_db()
    reset_db(SessionLocal())
    response = client.get("/counts")
    assert response.status_code == 200
    assert "ongoing_deliveries" in response.json()
    assert "total_deliveries" in response.json()
    assert response.json()["ongoing_deliveries"] == 0
    assert response.json()["total_deliveries"] == 0
    client.post(f"/deliveries/{generate_name()}/events", json={"type": "TAKEN_OFF"})
    client.post(f"/deliveries/{generate_name()}/events", json={"type": "TAKEN_OFF"})
    client.post(f"/deliveries/{generate_name()}/events", json={"type": "TAKEN_OFF"})
    response = client.get("/counts")
    assert response.json()["ongoing_deliveries"] == 3
    assert response.json()["total_deliveries"] == 3


def test_data_persistence(db):
    delivery_id = generate_name()
    create_delivery(db, delivery_id)

    init_db()

    persisted_delivery = get_delivery_by_id(db, delivery_id)
    assert persisted_delivery is not None
    assert persisted_delivery.id == delivery_id


def test_counts_api(db):
    init_db()
    delivery_id_1 = generate_name()
    delivery_id_2 = generate_name()
    create_delivery(db, delivery_id_1)
    create_delivery(db, delivery_id_2)

    update_delivery_state(
        db, get_delivery_by_id(db, delivery_id_1), DeliveryState.PARCEL_DELIVERED
    )

    response = client.get("/counts")
    data = response.json()

    assert response.status_code == 200
    assert data["ongoing_deliveries"] == 1
    assert data["total_deliveries"] == 2


def test_event_ordering(db):
    delivery_id = generate_name()
    create_delivery(db, delivery_id)
    create_event(db, delivery_id, DeliveryState.TAKEN_OFF)
    create_event(db, delivery_id, DeliveryState.LANDED)

    events = get_events_by_delivery_id(db, delivery_id)
    assert events[0].type == DeliveryState.TAKEN_OFF
    assert events[1].type == DeliveryState.LANDED


def test_enforce_delivery_limit(db):
    for _ in range(1001):
        delivery_id = generate_name()
        create_delivery(db, delivery_id)

    delivery_count = db.query(Delivery).count()
    assert delivery_count == 1000

    first_delivery = db.query(Delivery).order_by(Delivery.created_at).first()
    assert first_delivery.created_at > datetime.now(timezone.utc) - timedelta(days=1)
    assert first_delivery.state == DeliveryState.PARCEL_COLLECTED
