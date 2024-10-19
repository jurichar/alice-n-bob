"""
route.py is the file that contains the routes from SQLAlchemy ORM methods in the CRUD operations.
"""

@app.post("/deliveries/{id}/events")
async def root(id: str, event: Event):
    print(f"Delivery {id} transitioned to {event.type}")
    return {"message": "ok"}
