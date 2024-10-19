"""
models.py is the file that contains the models for SQLAlchemy ORM.
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
import enum

Base = declarative_base()


class DeliveryState(str, enum.Enum):
    PARCEL_COLLECTED = "PARCEL_COLLECTED"
    TAKEN_OFF = "TAKEN_OFF"
    LANDED = "LANDED"
    CRASHED = "CRASHED"
    PARCEL_DELIVERED = "PARCEL_DELIVERED"


class Delivery(Base):
    __tablename__ = "deliveries"

    id = Column(String, primary_key=True, default="1")
    state = Column(enum.Enum(DeliveryState))
    created_at = Column(String)
    updated_at = Column(String)


class Event(Base):
    __tablename__ = "events"

    id = Column(String, primary_key=True, autoincrement=True)
    delivery_id = Column(String)
    type = Column(String)
    created_at = Column(String)
    updated_at = Column(String)
