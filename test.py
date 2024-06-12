from cassandra.cluster import Cluster
from cassandra.query import ConsistencyLevel
from datetime import datetime
from services.BookingService import BookingService
import unittest

cluster = Cluster(
    contact_points=[
      ('127.0.0.1', 9042),
      ('127.0.0.1', 9043)
    ]
)


# class CassandraTests(unittest.TestCase):
#     def test_connect(self):
#         self.assertEqual(session.keyspace, 'flights_system')



if __name__ == '__main__':
    BookingService = BookingService()
    flight_id = BookingService.create_initial()
    BookingService.book_tickets(flight_id, 2, ['4Mike', '4Jef'])
    BookingService.display_bookings(flight_id)
    # BookingService.remove_booking("aca51eec-0766-49c7-adc5-c1a5b5fe3b4a")