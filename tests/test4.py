from locust import HttpUser, task, between, events

class StressTestUser(HttpUser):
    wait_time = between(0, 0.1)
    host = "http://localhost:8000"
    
    @task(1)
    def post_booking(self):
        self.client.post("/bookings?flight_id=67d89315-c5b7-4ea9-85ae-53fd3df04ffa&num_seats=1", data={"passenger_names": ["John Doe"]})

if __name__ == "__main__":
    import os
    os.system("locust -f test4.py --headless -u 2 -r 1 --run-time 1m")