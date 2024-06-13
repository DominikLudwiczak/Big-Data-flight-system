

class Booking:
    def __init__(self, flight_id, booking_id, passenger_name, seat_number):
        self.flight_id = flight_id
        self.booking_id = booking_id
        self.passenger_name = passenger_name
        self.seat_number = seat_number

    def to_json(self):
        return {
            "flight_id": str(self.flight_id),
            "booking_id": str(self.booking_id),
            "passenger_name": self.passenger_name,
            "seat_number": self.seat_number
        }
    
    @staticmethod
    def to_json(flight_id, booking_id, passenger_name, seat_number):
        return {
            "flight_id": str(flight_id),
            "booking_id": str(booking_id),
            "passenger_name": passenger_name,
            "seat_number": seat_number
        }