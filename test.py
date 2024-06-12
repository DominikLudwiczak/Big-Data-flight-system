from services.BookingService import BookingService
from services.FlightService import FlightService
from datetime import datetime
from connect import session


# class CassandraTests(unittest.TestCase):
#     def test_connect(self):
#         self.assertEqual(session.keyspace, 'flights_system')


if __name__ == '__main__':
    BookingService = BookingService()
    FlightService = FlightService()
    # flight_id = BookingService.create_initial()
    # BookingService.addBooking(flight_id, 8, ['1Mike', '2Jef', '3John', '4Doe', '5Jane', '6Ron', '7Harry', '8Potter'])
    # BookingService.getAllBookingsById(flight_id)
    # FlightService.addFlight('JFK', 'LAX', datetime.now(), datetime.now())
    # BookingService.updateBooking('b2009b11-371c-4f0c-a494-506603d719bd', '5db5b464-905f-4e34-8fda-2e53581a1295')
    BookingService.addBooking('120fc823-97af-4717-a0f9-6417c7129739', 1, ['1Mike'])
    FlightService.getAllFlights()