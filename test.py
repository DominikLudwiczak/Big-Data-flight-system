from services.BookingService import BookingService
from services.FlightService import FlightService
from datetime import datetime


# class CassandraTests(unittest.TestCase):
#     def test_connect(self):
#         self.assertEqual(session.keyspace, 'flights_system')


if __name__ == '__main__':
    BookingService = BookingService()
    FlightService = FlightService()
    # flight_id = BookingService.create_initial()
    # BookingService.addBooking('4090aa08-52be-48c8-8fc4-7622de8efbfe', 8, ['1Mike', '2Jef', '3John', '4Doe', '5Jane', '6Ron', '7Harry', '8Potter'])
    # BookingService.getAllBookingsById(flight_id)
    FlightService.addFlight('XDD', 'DDX', datetime.now(), datetime.now())
    success, msg = BookingService.updateBooking('caf5347c-7bc2-4e1f-9d6b-cf1842c01613', 'f24c18c3-6bea-4c48-a284-9ad81dcd6a30')
    # print(success, msg)
    # BookingService.addBooking('7de32efa-2dd0-4fd0-a281-eda2ebecd343', 1, ['1Mike'])
    FlightService.getAllFlights()