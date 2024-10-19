"""
route.py is the file that contains the routes from SQLAlchemy ORM methods in the CRUD operations.
"""

from fastapi import APIRouter
from schemas import EventResponse, Event, DeliveryResponse, DeliveryState

router = APIRouter()


@router.post("/deliveries/{id}/events", response_model=EventResponse)
async def root(id: str, event: Event):
    print(f"Delivery {id} transitioned to {event.type}")
    return {"message": "ok"}


# @router.post("/deliveries/{delivery_id}/events", response_model=EventResponse) ok
# @router.get("/deliveries", response_model=list[DeliveryResponse])
# @router.get("/deliveries/{delivery_id}/events", response_model=list[EventResponse])
# @router.get("/counts")
