from locust import HttpUser, task, between, events
import random

class StressTestUser(HttpUser):
    wait_time = between(0, 0)
    host = "http://localhost:8000"
    request_count = 0

    # do 2 post requests at same time
    @task(1)
    def add_booking(self):
        if not hasattr(self, "flight_ids"):
            return
        else:
            flight_id = self.flight_ids[random.randint(0, len(self.flight_ids) - 1)]
            self.client.post("/bookings", json={"flight_id": f"e0fd4c46-f19f-420b-9ad5-f7a829c047ac", "num_seats": 1, "passenger_names": ["John Doe"]})
            self.client.post("/bookings", json={"flight_id": f"e0fd4c46-f19f-420b-9ad5-f7a829c047ac", "num_seats": 1, "passenger_names": ["John Doe"]})