

class Flight:
    def __init__(self, flight_id, departure_airport, arrival_airport, departure_time, arrival_time, capacity, booked_seats):
        self.flight_id = flight_id
        self.departure_airport = departure_airport
        self.arrival_airport = arrival_airport
        self.departure_time = departure_time
        self.arrival_time = arrival_time
        self.capacity = capacity
        self.booked_seats = booked_seats
    
    def to_json(self):
        return {
            "flight_id": str(self.flight_id),
            "departure_airport": self.departure_airport,
            "arrival_airport": self.arrival_airport,
            "departure_time": self.departure_time.isoformat() if self.departure_time else None,
            "arrival_time": self.arrival_time.isoformat() if self.arrival_time else None,
            "capacity": self.capacity,
            "booked_seats": list(self.booked_seats) if self.booked_seats else []
        }
    
    @staticmethod
    def to_json(flight_id, departure_airport, arrival_airport, departure_time, arrival_time, capacity, booked_seats):
        return {
            "flight_id": str(flight_id),
            "departure_airport": departure_airport,
            "arrival_airport": arrival_airport,
            "departure_time": departure_time.isoformat() if departure_time else None,
            "arrival_time": arrival_time.isoformat() if arrival_time else None,
            "capacity": capacity,
            "booked_seats": list(booked_seats) if booked_seats else []
        }