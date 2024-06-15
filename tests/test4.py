from locust import HttpUser, task, between, events

class StressTestUser(HttpUser):
    wait_time = between(0, 0)
    host = "http://localhost:8000"
    
    @task(1)
    def post_booking(self):
        self.client.post("/bookings/seated", json={"flight_id": "3bb6f975-b786-434c-95c9-4a71bb500fc4", "booking_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6", "seat_number": "1A", "passenger_name": "Test"})

    @task(1)
    def del_booking(self):
        booking = self.client.get("/bookings").json()
        booking = booking[0] if len(booking) > 0 else None
        if not booking:
            return
        self.client.delete(f"/bookings/{booking['booking_id']}")

if __name__ == "__main__":
    import os
    os.system("locust -f test4.py --headless -u 2 -r 1 --run-time 10m")