from fastapi.routing import APIRouter
from services.BookingService import BookingService
import uuid

router = APIRouter(prefix="/bookings", tags=["bookings"])

service = BookingService()

@router.get("/{flightId}")
def getAllBookingsByFlightId(flightId: uuid.UUID):
    return service.getAllBookingsById(flightId)

@router.post("/")
def addBooking(flight_id: uuid.UUID, num_seats: int, passenger_names: list[str]):
    service.addBooking(flight_id, num_seats, passenger_names)

@router.delete("/{bookId}")
def deleteBooking(bookId: uuid.UUID):
    service.deleteBooking(bookId)

@router.put("/{bookId}")
def updateBooking(bookingId: uuid.UUID, flightId: uuid.UUID):
    service.updateBooking(bookingId, flightId)