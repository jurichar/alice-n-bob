"""
models.py is the file that contains the models for SQLAlchemy ORM.
"""

from sqlalchemy import Column, String
from sqlalchemy.orm import declarative_base
from enum import Enum

Base = declarative_base()


class DeliveryState(str, Enum):
    PARCEL_COLLECTED = "PARCEL_COLLECTED"
    TAKEN_OFF = "TAKEN_OFF"
    LANDED = "LANDED"
    CRASHED = "CRASHED"
    PARCEL_DELIVERED = "PARCEL_DELIVERED"


class Delivery(Base):
    __tablename__ = "deliveries"

    id = Column(String, primary_key=True, default="1")
    state = Column(Enum(DeliveryState))
    created_at = Column(String)
    updated_at = Column(String)


class Event(Base):
    __tablename__ = "events"

    id = Column(String, primary_key=True, autoincrement=True)
    delivery_id = Column(String)
    type = Column(String)
    created_at = Column(String)
    updated_at = Column(String)
