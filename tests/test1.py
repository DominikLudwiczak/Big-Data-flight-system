from locust import HttpUser, task, between, events

class StressTestUser(HttpUser):
    wait_time = between(0, 0)
    host = "http://localhost:8000"

    @task(1)
    def get_all_bookings(self):
        self.client.get("/bookings")

if __name__ == "__main__":
    import os
    os.system("locust -f test1.py --headless -u 1 -r 1 --run-time 1m")