"""
schemas.py is the file that contains the schemas for Pydantic models.
"""

from pydantic import BaseModel


class Event(BaseModel):
    type: str
