from locust import HttpUser, task, between, events

class StressTestUser(HttpUser):
    wait_time = between(0, 0)
    host = "http://localhost:8000"
    
    @task(1)
    def post_booking(self):
        booking = self.client.get("/bookings").json()[0]
        flights = self.client.get("/flights").json()
        flight = next((f for f in flights if f["flight_id"] != booking["flight_id"] and f["capacity"] > 0), None)
        result = self.client.put(f"/bookings/{booking['booking_id']}?bookingId={booking['booking_id']}&flightId={flight['flight_id']}")

if __name__ == "__main__":
    import os
    os.system("locust -f test5.py --headless -u 1 -r 1 --run-time 5m")