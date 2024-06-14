from pydantic import BaseModel
from typing import Optional, Set
from uuid import UUID
from datetime import datetime

class Flight(BaseModel):
    flight_id: UUID
    departure_airport: str
    arrival_airport: str
    departure_time: Optional[datetime]
    arrival_time: Optional[datetime]
    capacity: int
    booked_seats: Set[str]

    def to_json(self) -> dict:
        return self.model_dump_json()