from cassandra.cluster import Cluster
from cassandra.query import ConsistencyLevel
from datetime import datetime
import uuid
import unittest

cluster = Cluster(
    contact_points=[
      ('127.0.0.1', 9042),
      ('127.0.0.1', 9043)
    ]
)

session = cluster.connect()

query = "CREATE KEYSPACE IF NOT EXISTS airline WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 1 }"
session.execute(query)

session.set_keyspace('airline')


# session.default_consistency_level = ConsistencyLevel.QUORUM

class CassandraTests(unittest.TestCase):
    def test_connect(self):
        self.assertEqual(session.keyspace, 'flights_system')


class BookingService:
    def create_initial(self):
        query = f"TRUNCATE bookings;"
        session.execute(query)

        query = f"TRUNCATE flights;"
        session.execute(query)
        
        create_flights_table_query = """
            CREATE TABLE IF NOT EXISTS flights (
                flight_id UUID PRIMARY KEY,
                departure_airport TEXT,
                arrival_airport TEXT,
                departure_time TIMESTAMP,
                arrival_time TIMESTAMP,
                capacity INT,
                booked_seats SET<TEXT>
            )
        """
        session.execute(create_flights_table_query)

        create_bookings_table_query = """
            CREATE TABLE IF NOT EXISTS bookings (
                booking_id UUID PRIMARY KEY,
                flight_id UUID,
                passenger_name TEXT,
                seat_number TEXT,
                booking_time TIMESTAMP
            )
        """
        session.execute(create_bookings_table_query)

        flight_id = uuid.uuid4()
        booked_seats_str = "{" + ', '.join(map(lambda x: f"'{x}'", set(['1A', '2B']))) + "}"
        insert_flight_query = f"""
            INSERT INTO flights (flight_id, departure_airport, arrival_airport, departure_time, arrival_time, capacity, booked_seats)
            VALUES ({flight_id}, 'JFK', 'LAX', toTimestamp(now()), toTimestamp(now()), 178, {booked_seats_str})
        """
        session.execute(insert_flight_query)

        booking_data = [
            (flight_id, 'John Cena', '1A'),
            (flight_id, 'Max Verstappen', '2B')
        ]
        self.insert_query = session.prepare("""
            INSERT INTO bookings (booking_id, flight_id, passenger_name, seat_number, booking_time)
            VALUES (uuid(), ?, ?, ?, toTimestamp(now()))
        """)

        query = 'CREATE INDEX IF NOT EXISTS bookings_flight_id_idx ON bookings (flight_id);'
        session.execute(query)

        for data in booking_data:
            session.execute(self.insert_query, data)

        return flight_id

    def book_tickets(self, flight_id, num_seats, passenger_names):
        available_seats_query = f"SELECT booked_seats, capacity FROM flights WHERE flight_id = {flight_id}"
        result = session.execute(available_seats_query)
        row = result.one()
        booked_seats = row.booked_seats if row else set()
        capacity = row.capacity if row else 0

        if capacity - num_seats < 0:
            return False, None

        for row_num in range(1, 3):
            seats = [f"{row_num}{seat}" for seat in "ABCDEF"]
            for i in range(len(seats) - num_seats + 1):
                selected_seats = set(seats[i:i + num_seats])
                if not selected_seats & booked_seats:
                    booking_ids = [uuid.uuid4() for _ in range(num_seats)]
                    booking_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    for booking_id, seat, passenger_name in zip(booking_ids, selected_seats, passenger_names):
                        insert_booking_query = f"""
                            INSERT INTO bookings (booking_id, flight_id, passenger_name, seat_number, booking_time)
                            VALUES ({booking_id}, {flight_id}, '{passenger_name}', '{seat}', '{booking_time}')
                        """
                        session.execute(insert_booking_query)

                    updated_booked_seats = booked_seats.union(selected_seats)
                    capacity -= len(selected_seats)
                    booked_seats_str = "{" + ', '.join(map(lambda x: f"'{x}'", updated_booked_seats)) + "}"
                    update_flight_query = f"""
                        UPDATE flights
                        SET booked_seats = {booked_seats_str},
                            capacity = {capacity}
                        WHERE flight_id = {flight_id}
                    """
                    session.execute(update_flight_query)

                    return True, list(selected_seats)

        return False, None


    def remove_booking(self, booking_id):
        booking_query = f"SELECT flight_id, seat_number FROM bookings WHERE booking_id = {booking_id}"
        result = session.execute(booking_query)
        if not result:
            return False, "Booking not found"
        
        row = result.one()
        flight_id = row.flight_id
        seat_number = row.seat_number
        
        delete_booking_query = f"DELETE FROM bookings WHERE booking_id = {booking_id}"
        session.execute(delete_booking_query)
        
        update_seats_query = f"UPDATE flights SET booked_seats = booked_seats - {{'{seat_number}'}} WHERE flight_id = {flight_id}"
        session.execute(update_seats_query)
        
        return True, f"Booking {booking_id} removed, seat {seat_number} freed"

    def update_booking(self, booking_id, flight_id):
        booking_query = f"SELECT seat_number, name FROM bookings WHERE booking_id = {booking_id}"
        result = session.execute(booking_query)
        if not result:
            return False, "Booking not found"
        
        row = result.one()
        seat_number = row.seat_number
        
        update_booking_query = f"UPDATE bookings SET flight_id = {flight_id} WHERE booking_id = {booking_id}"
        session.execute(update_booking_query)
        
        return True, f"Booking {booking_id} updated to flight {flight_id}"

    def display_bookings(self, flight_id):
        booking_query = f"SELECT booking_id, seat_number, passenger_name FROM bookings WHERE flight_id = {flight_id}"
        result = session.execute(booking_query)
        if not result:
            return False, "No bookings found"
        for row in result:
            print(f"Booking ID: {row.booking_id}, Seat: {row.seat_number}, Name: {row.passenger_name}")
        
        return True, result


if __name__ == '__main__':
    BookingService = BookingService()
    flight_id = BookingService.create_initial()
    BookingService.book_tickets(flight_id, 2, ['4Mike', '4Jef'])
    BookingService.display_bookings(flight_id)
    # BookingService.remove_booking("aca51eec-0766-49c7-adc5-c1a5b5fe3b4a")