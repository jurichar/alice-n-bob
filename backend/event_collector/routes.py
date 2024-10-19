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
    create_event,
    get_events_by_delivery_id,
    get_delivery_counts,
    reset_db,
    get_all_counts,
)
from config import get_db
from schemas import EventResponse, EventCreate, DeliveryResponse, DeliveryState

router = APIRouter()


@router.post("/deliveries/{delivery_id}/events", response_model=EventResponse)
async def add_event(
    delivery_id: str, event: EventCreate, db: Session = Depends(get_db)
):
    """
    Ingests events. It accepts a JSON payload in the request body in the form `{"type": "TAKEN_OFF"}`.
    """
    delivery = get_delivery_by_id(db, delivery_id)

    if delivery and delivery.state in [
        DeliveryState.PARCEL_DELIVERED,
        DeliveryState.CRASHED,
    ]:
        raise HTTPException(
            status_code=400, detail="Cannot update a completed delivery"
        )

    if not delivery:
        delivery = create_delivery(db, delivery_id)

    new_event = create_event(db, delivery_id, event.type)

    if event.type in [DeliveryState.CRASHED, DeliveryState.PARCEL_DELIVERED]:
        update_delivery_state(db, delivery, event.type)

    return EventResponse(
        id=new_event.id,
        delivery_id=new_event.delivery_id,
        type=new_event.type,
        created_at=new_event.created_at,
        updated_at=new_event.updated_at,
    )


@router.get("/deliveries", response_model=list[DeliveryResponse])
async def deliveries(db: Session = Depends(get_db)):
    """
    Lists all currently ongoing deliveries (i.e., deliveries not in a final state).
    """
    deliveries = get_ongoing_deliveries(db)
    return [
        DeliveryResponse(
            id=delivery.id,
            state=delivery.state,
            created_at=delivery.created_at,
            updated_at=delivery.updated_at,
        )
        for delivery in deliveries
    ]


@router.get("/deliveries/{delivery_id}/events", response_model=list[EventResponse])
def events(delivery_id: str, db: Session = Depends(get_db)):
    """
    Returns the list of events received for a given delivery mission, whether ongoing or in a final state.
    Only the data of the last 1000 delivery missions should be available, and older data should be discarded.
    """
    delivery = get_delivery_by_id(db=db, delivery_id=delivery_id)
    if not delivery:
        raise HTTPException(status_code=404, detail="Delivery not found")
    events = get_events_by_delivery_id(db, delivery_id)
    return [
        EventResponse(
            id=event.id,
            delivery_id=event.delivery_id,
            type=event.type,
            created_at=event.created_at,
            updated_at=event.updated_at,
        )
        for event in events
    ]


@router.get("/deliveries/{delivery_id}", response_model=DeliveryResponse)
def delivery(delivery_id: str, db: Session = Depends(get_db)):
    """
    Returns the state of a given delivery mission.
    """
    delivery = get_delivery_by_id(db=db, delivery_id=delivery_id)
    if not delivery:
        raise HTTPException(status_code=404, detail="Delivery not found")
    return DeliveryResponse(
        id=delivery.id,
        state=delivery.state,
        created_at=delivery.created_at,
        updated_at=delivery.updated_at,
    )


@router.get("/counts")
async def counts(db: Session = Depends(get_db)):
    """
    Returns the number of ongoing deliveries and the total number of deliveries since the beginning.
    """
    return get_delivery_counts(db)


@router.get("/counts_all")
async def counts_all(db: Session = Depends(get_db)):
    """
    Returns the number of ongoing deliveries and the total number of deliveries since the beginning.
    """
    return get_all_counts(db)


@router.get("/reset")
async def reset(db: Session = Depends(get_db)):
    return reset_db(db)
