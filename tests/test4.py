from locust import HttpUser, task, between, events

class StressTestUser(HttpUser):
    wait_time = between(0, 0)
    host = "http://localhost:8000"
    
    @task(1)
    def post_booking(self):
        self.client.post("/bookings/seated", json={"flight_id": "c679f2ec-3d83-4ef6-9bfd-1dc7343d9236", "booking_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6", "seat_number": "1A", "passenger_name": "Test"})

if __name__ == "__main__":
    import os
    os.system("locust -f test4.py --headless -u 2 -r 1 --run-time 5m")