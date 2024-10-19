"""
route.py is the file that contains the routes from SQLAlchemy ORM methods in the CRUD operations.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from config import get_db
from schemas import EventResponse, EventCreate, DeliveryResponse, DeliveryState

router = APIRouter()


@router.post("/deliveries/{id}/events", response_model=EventResponse)
async def root(delivery_id: str, event: EventCreate, db: Session = Depends(get_db)):
    if not delivery:
        delivery = function.create_delivery(db, delivery_id)

    new_event = function.create_event(db, delivery_id, event.type)
    return EventResponse(**new_event.__dict__)


# @router.post("/deliveries/{delivery_id}/events", response_model=EventResponse) ok
# @router.get("/deliveries", response_model=list[DeliveryResponse])
# @router.get("/deliveries/{delivery_id}/events", response_model=list[EventResponse])


@router.get("/counts")
async def counts():
    return {"message": "ok"}
