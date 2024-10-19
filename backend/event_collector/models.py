"""
models.py is the file that contains the models for SQLAlchemy ORM.
"""

from sqlalchemy import Column, String, Enum, ForeignKey
from sqlalchemy.orm import declarative_base
from enum import Enum as enum

from utils import generate_name

Base = declarative_base()


class DeliveryState(str, enum):
    PARCEL_COLLECTED = "PARCEL_COLLECTED"
    TAKEN_OFF = "TAKEN_OFF"
    LANDED = "LANDED"
    CRASHED = "CRASHED"
    PARCEL_DELIVERED = "PARCEL_DELIVERED"


class Delivery(Base):
    __tablename__ = "deliveries"

    id = Column(String, primary_key=True, default=generate_name())
    state = Column(Enum(DeliveryState))
    created_at = Column(String)
    updated_at = Column(String)


class Event(Base):
    __tablename__ = "events"

    id = Column(String, primary_key=True, default=generate_name())
    delivery_id = Column(String, ForeignKey("deliveries.id"))
    type = Column(Enum(DeliveryState))
    created_at = Column(String)
    updated_at = Column(String)
