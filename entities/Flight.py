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
    
    @staticmethod
    def to_json(flight_id, departure_airport, arrival_airport, departure_time, arrival_time, capacity, booked_seats) -> dict:
        return {
            "flight_id": flight_id,
            "departure_airport": departure_airport,
            "arrival_airport": arrival_airport,
            "departure_time": departure_time,
            "arrival_time": arrival_time,
            "capacity": capacity,
            "booked_seats": list(booked_seats) if booked_seats else []
        }