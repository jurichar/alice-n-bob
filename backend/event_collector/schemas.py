"""
schemas.py is the file that contains the schemas for Pydantic models.
"""

from pydantic import BaseModel
from datetime import datetime
from enum import Enum


class DeliveryState(str, Enum):
    PARCEL_COLLECTED = "PARCEL_COLLECTED"
    TAKEN_OFF = "TAKEN_OFF"
    LANDED = "LANDED"
    CRASHED = "CRASHED"
    PARCEL_DELIVERED = "PARCEL_DELIVERED"


class EventCreate(BaseModel):
    type: DeliveryState


class DeliveryResponse(BaseModel):
    id: str
    state: DeliveryState
    created_at: datetime
    updated_at: datetime


class EventResponse(BaseModel):
    id: str
    delivery_id: str
    created_at: datetime
    updated_at: datetime
