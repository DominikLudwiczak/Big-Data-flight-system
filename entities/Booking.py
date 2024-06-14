from pydantic import BaseModel
from uuid import UUID


class Booking(BaseModel):
    flight_id: UUID
    booking_id: UUID
    passenger_name: str
    seat_number: str

    def to_json(self) -> dict:
        return self.model_dump_json()