from pydantic import BaseModel
from uuid import UUID


class Booking(BaseModel):
    flight_id: UUID
    booking_id: UUID
    passenger_name: str
    seat_number: str

    def to_json(self) -> dict:
        return self.model_dump_json()
    
    @staticmethod
    def to_json(flight_id, booking_id, passenger_name, seat_number) -> dict:
        return {
            "flight_id": flight_id,
            "booking_id": booking_id,
            "passenger_name": passenger_name,
            "seat_number": seat_number
        }