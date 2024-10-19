"""
schemas.py is the file that contains the schemas for Pydantic models.
"""

from pydantic import BaseModel
from enum import Enum


class DeliveryState(str, Enum):
    PARCEL_COLLECTED = "PARCEL_COLLECTED"
    TAKEN_OFF = "TAKEN_OFF"
    LANDED = "LANDED"
    CRASHED = "CRASHED"
    PARCEL_DELIVERED = "PARCEL_DELIVERED"


class Event(BaseModel):
    type: str


class DeliveryResponse(BaseModel):
    id: str
    state: DeliveryState
    created_at: str
    updated_at: str


class EventResponse(BaseModel):
    id: str
    delivery_id: str
    type: str
    created_at: str
    updated_at: str
