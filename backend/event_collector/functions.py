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


def get_delivery_by_id():
    pass


def update_delivery_state():
    pass


def get_ongoing_deliveries():
    pass


def get_delivery_counts():
    pass


"""
------------ EVENTS PART ------------
"""


def get_events():
    pass


def create_event():
    pass


def get_events_by_delivery_id():
    pass


"""
------------ OTHER ------------
"""


def get_counts():
    pass
