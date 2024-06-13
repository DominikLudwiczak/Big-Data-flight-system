from fastapi.routing import APIRouter
from services.FlightService import FlightService
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
def addFlight(departure_airport: str, arrival_airport: str, departure_time: str, arrival_time: str):
    service.addFlight(departure_airport, arrival_airport, departure_time, arrival_time)

@router.delete("/{flightId}")
def deleteFlight(flightId: uuid.UUID):
    service.deleteFlight(flightId)