from fastapi.testclient import TestClient
import threading
from main import app

client = TestClient(app)

def book_all_flight(passenger_name):
    flights = client.get("/flights").json()
    flight = max(flights, key=lambda x: x["capacity"])
    bookings = []
    for i in range(flight["capacity"]):
        bookings.append({"flight_id": flight["flight_id"], "booking_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6", "seat_number": "1A", "passenger_name": f"{passenger_name}_{i}"})
    client.post("/bookings", json=bookings)


def add_booking():
    t1 = threading.Thread(target=book_all_flight, args=('one',))
    t2 = threading.Thread(target=book_all_flight, args=('two',))

    t1.start()
    t2.start()

    t1.join()
    t2.join()

if __name__ == "__main__":
    add_booking()
