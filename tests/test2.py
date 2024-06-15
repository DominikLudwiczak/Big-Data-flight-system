from locust import HttpUser, task, between, events
import uuid
import random

class StressTestUser(HttpUser):
    wait_time = between(0, 0)
    host = "http://localhost:8000"
    request_count = 0
    

    @task(1)
    def get_all_bookings(self):
        self.client.get("/bookings")

    @task(1)
    def get_all_flights(self):
        self.client.get("/flights")

    @task(1)
    def get_all_bookings_by_flight_id(self):
        flights = self.client.get("/flights").json()
        flight_ids = [flight["flight_id"] for flight in flights]
        if len(flight_ids) == 0:
            return
        flight_id = flight_ids[random.randint(0, len(flight_ids) - 1)]
        if not flight_id:
            return
        
        self.client.get(f"/bookings/{flight_id}")

    @task(1)
    def add_booking(self):
        flights = self.client.get("/flights").json()
        flight_ids = [flight["flight_id"] for flight in flights]
        if len(flight_ids) == 0:
            return
        flight_id = flight_ids[random.randint(0, len(flight_ids) - 1)]

        random_uuid = uuid.uuid4()
        if not flight_id:
            return
        self.client.post("/bookings", json=[{"flight_id": f"{flight_id}", "booking_id": f"{random_uuid}", "passenger_name": "John Doe", "seat_number": "25B"}])

    @task(1)
    def update_booking(self):
        flights = self.client.get("/flights").json()
        flight_ids = [flight["flight_id"] for flight in flights]
        if len(flight_ids) == 0:
            return
        flight_id = flight_ids[random.randint(0, len(flight_ids) - 1)]

        bookings = self.client.get("/bookings").json()
        booking_ids = [booking["booking_id"] for booking in bookings]
        if len(booking_ids) == 0:
            return
        booking_id = booking_ids[random.randint(0, len(booking_ids) - 1)]

        if not booking_id or not flight_id:
            return

        self.client.put(f"/bookings/{booking_id}?bookingId={booking_id}&flightId={flight_id}")
    
    @task(1)
    def delete_booking(self):
        bookings = self.client.get("/bookings").json()
        if not bookings:
            return
        booking_ids = [booking["booking_id"] for booking in bookings]
        if len(booking_ids) == 0:
            return
        booking_id = booking_ids[random.randint(0, len(booking_ids) - 1)]
        
        self.client.delete(f"/bookings/{booking_id}")


if __name__ == "__main__":
    import os
    os.system("locust -f test2.py --headless -u 2 -r 1 --run-time 10m")