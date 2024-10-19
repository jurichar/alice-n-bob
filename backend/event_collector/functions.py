"""
function.py is the file that contains the CRUD operations (Create Read Update Delete).
Only use SQLAlchemy ORM methods in this file.
"""

from sqlalchemy.orm import Session
from utils import generate_name
from models import Delivery, Event, DeliveryState
from datetime import datetime, timezone

"""
------------ DELIVERY PART ------------
"""

MAX_DELIVERIES = 1000


def enforce_delivery_limit(db: Session):
    delivery_count = db.query(Delivery).count()

    if delivery_count >= MAX_DELIVERIES:
        oldest_deliveries = (
            db.query(Delivery)
            .order_by(Delivery.created_at)
            .limit(delivery_count - MAX_DELIVERIES + 1)
            .all()
        )
        for delivery in oldest_deliveries:
            db.query(Event).filter(Event.delivery_id == delivery.id).delete()
            db.delete(delivery)
        db.commit()


def create_delivery(db: Session, delivery_id: str):
    new_delivery = Delivery(
        id=delivery_id,
        state=DeliveryState.PARCEL_COLLECTED,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    enforce_delivery_limit(db)

    db.add(new_delivery)
    db.commit()
    db.refresh(new_delivery)

    return new_delivery


def get_delivery_by_id(db: Session, delivery_id: str):
    return db.query(Delivery).filter(Delivery.id == delivery_id).first()


def update_delivery_state(db: Session, delivery: Delivery, new_state: DeliveryState):
    delivery.state = new_state
    delivery.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(delivery)
    return delivery


def get_ongoing_deliveries(db: Session):
    return (
        db.query(Delivery)
        .filter(
            Delivery.state.notin_(
                [DeliveryState.CRASHED, DeliveryState.PARCEL_DELIVERED]
            )
        )
        .all()
    )


def get_delivery_counts(db: Session):
    return {
        "ongoing_deliveries": db.query(Delivery)
        .filter(
            Delivery.state != DeliveryState.PARCEL_DELIVERED
            or Delivery.state != DeliveryState.CRASHED
        )
        .count(),
        "total_deliveries": db.query(Delivery).count(),
    }


"""
------------ EVENTS PART ------------
"""


def create_event(db: Session, delivery_id: str, type: DeliveryState):
    new_event = Event(
        id=generate_name(),
        type=type,
        delivery_id=delivery_id,
        created_at=datetime.now(timezone.utc),
    )
    db.add(new_event)
    db.commit()
    db.refresh(new_event)
    return new_event


def get_events_by_delivery_id(db: Session, delivery_id: str):
    return db.query(Event).filter(Event.delivery_id == delivery_id).all()


def reset_db(db: Session):
    db.query(Event).delete()
    db.query(Delivery).delete()
    db.commit()
    return True
