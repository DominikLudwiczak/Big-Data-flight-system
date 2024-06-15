from fastapi.routing import APIRouter
from services.FlightService import FlightService
from entities.Flight import Flight
import uuid

router = APIRouter(prefix="/flights", tags=["flights"])

service = FlightService()

@router.get("/")
def getAllFlights():
    return service.getAllFlights()

@router.get("/{flightId}")
def getFlight(flightId: uuid.UUID):
    return service.getFlight(flightId)

@router.post("/")
def addFlight(flight: Flight):
    departure_airport = flight.departure_airport
    arrival_airport = flight.arrival_airport
    departure_time = flight.departure_time
    arrival_time = flight.arrival_time
    service.addFlight(departure_airport, arrival_airport, departure_time, arrival_time)

@router.delete("/{flightId}")
def deleteFlight(flightId: uuid.UUID):
    service.deleteFlight(flightId)