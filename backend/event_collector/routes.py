"""
route.py is the file that contains the routes from SQLAlchemy ORM methods.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from functions import (
    create_delivery,
    get_delivery_by_id,
    update_delivery_state,
    get_ongoing_deliveries,
    get_delivery_counts,
    create_event,
    get_events_by_delivery_id,
)
from config import get_db
from schemas import EventResponse, EventCreate, DeliveryResponse, DeliveryState

router = APIRouter()


@router.post("/deliveries/{id}/events", response_model=EventResponse)
async def root(delivery_id: str, event: EventCreate, db: Session = Depends(get_db)):
    """
    Ingests events. It accepts a JSON payload in the request body in the form `{"type": "TAKEN_OFF"}`.
    """
    if not delivery:
        delivery = create_delivery(db, delivery_id)

    if event.type in [DeliveryState.CRASHED, DeliveryState.PARCEL_DELIVERED]:
        update_delivery_state(db, delivery, event.type)

    new_event = create_event(db, delivery_id, event.type)
    return EventResponse(**new_event.__dict__)


@router.get("/deliveries", response_model=list[DeliveryResponse])
async def deliveries(db: Session = Depends(get_db)):
    """
    Lists all currently ongoing deliveries (i.e., deliveries not in a final state).
    """
    deliveries = get_ongoing_deliveries(db)
    return [DeliveryResponse(**delivery.__dict__) for delivery in deliveries]


@router.get("/deliveries/{delivery_id}/events", response_model=list[EventResponse])
def events(delivery_id: str, db: Session = Depends(get_db)):
    """
    Returns the list of events received for a given delivery mission, whether ongoing or in a final state.
    Only the data of the last 1000 delivery missions should be available, and older data should be discarded.
    """
    delivery = get_delivery_by_id(db=db, delivery_id=delivery_id)
    if not delivery:
        raise HTTPException(status_code=404, detail="Delivery not found")
    events = get_events_by_delivery_id(function, delivery_id)
    return [EventResponse(**event.__dict__) for event in events]


@router.get("/counts")
async def counts(db: Session = Depends(get_db)):
    """
    Returns the number of ongoing deliveries and the total number of deliveries since the beginning.
    """
    return get_ongoing_deliveries(db)
