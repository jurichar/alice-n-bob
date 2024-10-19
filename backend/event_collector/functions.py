"""
crud.py is the file that contains the CRUD operations (Create Read Update Delete).
Only use SQLAlchemy ORM methods in this file.
"""

from sqlalchemy.orm import Session
from models import Delivery, Event, DeliveryState
from datetime import datetime, timezone

"""
------------ DELIVERY PART ------------
"""


def create_delivery(db: Session, delivery_id: str):
    new_delivery = Delivery(
        id=delivery_id,
        state=DeliveryState.PARCEL_COLLECTED,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
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
            Delivery.state != DeliveryState.PARCEL_DELIVERED
            or Delivery.state != DeliveryState.CRASHED
        )
        .all()
    )


def get_delivery_counts(db: Session):
    return {
        "total": db.query(Delivery).count(),
        "ongoing": db.query(Delivery)
        .filter(Delivery.state != DeliveryState.PARCEL_DELIVERED)
        .count(),
        "delivered": db.query(Delivery)
        .filter(Delivery.state == DeliveryState.PARCEL_DELIVERED)
        .count(),
        "crashed": db.query(Delivery)
        .filter(Delivery.state == DeliveryState.CRASHED)
        .count(),
    }


"""
------------ EVENTS PART ------------
"""


def get_events(db: Session):
    pass


def create_event(db: Session, delivery_id: str, event_type: DeliveryState):
    pass


def get_events_by_delivery_id(db: Session, delivery_id: str):
    pass


"""
------------ OTHER ------------
"""


def get_counts(db: Session):
    pass
