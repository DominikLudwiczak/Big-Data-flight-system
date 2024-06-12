from fastapi.routing import APIRouter
from services.FlightService import FlightService
import uuid

router = APIRouter(prefix="/flights", tags=["flights"])


class FlightController:
    def __init__(self):
        self.FlightService = FlightService()

    @router.get("/")
    def getAllFlights(self):
        return self.FlightService.getAllFlights()

    @router.get("/{flightId}")
    def getFlight(self, flightId: uuid.UUID):
        return self.FlightService.getFlight(flightId)

    @router.post("/")
    def addFlight(self, flight_name: str, source: str, destination: str, departure_time: str, arrival_time: str, capacity: int, booked_seats: int):
        self.FlightService.addFlight(flight_name, source, destination, departure_time, arrival_time, capacity, booked_seats)

    @router.delete("/{flightId}")
    def deleteFlight(self, flightId: uuid.UUID):
        self.FlightService.deleteFlight(flightId)