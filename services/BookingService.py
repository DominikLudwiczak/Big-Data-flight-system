from connect import session
import uuid


class BookingService:
    def create_initial(self):
        query = f"DROP TABLE IF EXISTS bookings;"
        session.execute(query)

        query = f"DROP TABLE IF EXISTS flights;"
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
                seat_number TEXT
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
        insert_booking_query = session.prepare("""
            INSERT INTO bookings (booking_id, flight_id, passenger_name, seat_number)
            VALUES (uuid(), ?, ?, ?)
        """)

        query = 'CREATE INDEX IF NOT EXISTS bookings_flight_id_idx ON bookings (flight_id);'
        session.execute(query)
        query = 'CREATE INDEX IF NOT EXISTS bookings_passenger_name_idx ON bookings (passenger_name);'
        session.execute(query)

        for data in booking_data:
            session.execute(insert_booking_query, data)

        return flight_id

    def addBooking(self, flight_id, num_seats, passenger_names):
        available_seats_query = f"SELECT booked_seats, capacity FROM flights WHERE flight_id = {flight_id}"
        result = session.execute(available_seats_query)
        row = result.one()
        booked_seats = row.booked_seats if row and row.booked_seats else set()
        capacity = row.capacity if row else 0

        if capacity - num_seats < 0:
            return False, None
        
        insert_booking_query = session.prepare(f"""
                            INSERT INTO bookings (booking_id, flight_id, passenger_name, seat_number)
                            VALUES (?, {flight_id}, ?, ?)
                        """)
        
        update_flight_query = session.prepare(f"""
                        UPDATE flights
                        SET booked_seats = ?,
                            capacity = ?
                        WHERE flight_id = {flight_id}
                    """)

        for row_num in range(1, 3):
            seats = [f"{row_num}{seat}" for seat in "ABCDEF"]
            for i in range(len(seats) - num_seats + 1):
                selected_seats = set(seats[i:i + num_seats])
                if not selected_seats & booked_seats:
                    booking_ids = [uuid.uuid4() for _ in range(num_seats)]
                    updated_booked_seats = booked_seats.union(selected_seats)
                    capacity -= len(selected_seats)
                    session.execute(update_flight_query, (updated_booked_seats, capacity))

                    for booking_id, seat, passenger_name in zip(booking_ids, selected_seats, passenger_names):
                        session.execute(insert_booking_query, (booking_id, passenger_name, seat))

                    return True, list(selected_seats)
        
        # if seats next to each other not avaliable give free seats from each row untill num_seats are provided
        for row_num in range(1, 3):
            seats = [f"{row_num}{seat}" for seat in "ABCDEF"]
            for seat in seats:
                if capacity == 0 or not passenger_names:
                    break
                if seat not in booked_seats:
                    print(seat)
                    booking_id = uuid.uuid4()
                    booked_seats = booked_seats.union({seat})
                    capacity -= 1
                    session.execute(update_flight_query, (booked_seats, capacity))
                    passenger_name = passenger_names.pop(0)
                    session.execute(insert_booking_query, (booking_id, passenger_name, seat))

        return False, None


    def deleteBooking(self, booking_id):
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

    def updateBooking(self, booking_id, flight_id):
        booking_query = f"SELECT flight_id, passenger_name, seat_number FROM bookings WHERE booking_id = {booking_id}"
        result = session.execute(booking_query).one()

        if not result:
            return False, "Booking not found"

        old_flight_id = result.flight_id
        passenger_name = result.passenger_name
        seat_number = result.seat_number

        result = self.addBooking(flight_id, 1, [passenger_name])
        if not result:
            revert_query = f"UPDATE flights SET booked_seats = booked_seats - {{'{seat_number}'}} WHERE flight_id = {flight_id}"
            session.execute(revert_query)
            return False, "No seats left on selected flight"

        self.deleteBooking(booking_id)

        update_old_flight_query = f"UPDATE flights SET booked_seats = booked_seats - {{'{seat_number}'}} WHERE flight_id = {old_flight_id}"
        session.execute(update_old_flight_query)

        return True, f"Booking {booking_id} updated to flight {flight_id}"

    def getAllBookingsById(self, flight_id):
        booking_query = f"SELECT booking_id, seat_number, passenger_name FROM bookings WHERE flight_id = {flight_id}"
        result = session.execute(booking_query)
        if not result:
            return False, "No bookings found"
        for row in result:
            print(f"Booking ID: {row.booking_id}, Seat: {row.seat_number}, Name: {row.passenger_name}")
        
        return True, result