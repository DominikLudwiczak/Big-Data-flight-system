from locust import HttpUser, task, between, events
import random

class StressTestUser(HttpUser):
    wait_time = between(0.1, 0.1)
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
        flight_id = flight_ids[random.randint(0, len(flight_ids) - 1)]
        if not flight_id:
            return

        flight_id = self.flight_ids[random.randint(0, len(self.flight_ids) - 1)]
        self.client.get(f"/bookings/flight/{flight_id}")

    @task(1)
    def add_booking(self):
        flights = self.client.get("/flights").json()
        flight_ids = [flight["flight_id"] for flight in flights]
        flight_id = flight_ids[random.randint(0, len(flight_ids) - 1)]

        if not flight_id:
            return
        self.client.post("/bookings", json={"flight_id": f"{flight_id}", "num_seats": 1, "passenger_names": ["John Doe"]})

    @task(1)
    def update_booking(self):
        flights = self.client.get("/flights").json()
        flight_ids = [flight["flight_id"] for flight in flights]
        flight_id = flight_ids[random.randint(0, len(flight_ids) - 1)]

        bookings = self.client.get("/bookings").json()
        booking_ids = [booking["booking_id"] for booking in bookings]
        booking_id = booking_ids[random.randint(0, len(booking_ids) - 1)]

        if not booking_id or not flight_id:
            return

        self.client.put(f"/bookings/{booking_id}", json={"flight_id": f"{flight_id}"})
    
    @task(1)
    def delete_booking(self):
        bookings = self.client.get("/bookings").json()
        if not bookings:
            return
        booking_ids = [booking["booking_id"] for booking in bookings]
        booking_id = booking_ids[random.randint(0, len(booking_ids) - 1)]
        
        booking_id = self.booking_ids[random.randint(0, len(self.booking_ids) - 1)]
        self.client.delete(f"/bookings/{booking_id}")


if __name__ == "__main__":
    import os
    os.system("locust -f test2.py --headless -u 2 -r 1 --run-time 1m")