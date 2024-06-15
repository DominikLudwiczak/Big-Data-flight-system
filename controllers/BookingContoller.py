from fastapi.routing import APIRouter
from services.BookingService import BookingService
from entities.Booking import Booking
import uuid

router = APIRouter(prefix="/bookings", tags=["bookings"])

service = BookingService()

@router.get("/{flightId}")
def getAllBookingsByFlightId(flightId: uuid.UUID):
    return service.getAllBookingsByFlightId(flightId)

@router.post("/")
def addBooking(bookings_list: list[Booking]):
    flight_id = bookings_list[0].flight_id
    passanger_names = [booking.passenger_name for booking in bookings_list]
    return service.addBooking(flight_id, len(passanger_names), passanger_names)

@router.post("/seated")
def addSeatedBooking(booking: Booking):
    return service.addSeatedBooking(booking)

@router.delete("/{bookId}")
def deleteBooking(bookId: uuid.UUID):
    service.deleteBooking(bookId)

@router.put("/{bookId}")
def updateBooking(bookingId: uuid.UUID, flightId: uuid.UUID):
    return service.updateBooking(bookingId, flightId)

@router.get("/")
def getAllBookings():
    return service.getAllBookings()
