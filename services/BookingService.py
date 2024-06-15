from connect import session
from entities.Booking import Booking
import uuid


class BookingService:

    def addBooking(self, flight_id, num_seats, passenger_names):
        starting_len = len(passenger_names)
        available_seats_query = f"SELECT booked_seats, capacity FROM flights WHERE flight_id = {flight_id}"
        result = session.execute(available_seats_query)
        row = result.one()
        booked_seats = row.booked_seats if row and row.booked_seats else set()
        capacity = row.capacity if row else 0

        if capacity - num_seats < 0:
            return None
        
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

        for row_num in range(1, 31):
            seats = [f"{row_num}{seat}" for seat in "ABCDEF"]
            for i in range(len(seats) - num_seats + 1):
                selected_seats = set(seats[i:i + num_seats])
                if not selected_seats & booked_seats:
                    booking_ids = [uuid.uuid4() for _ in range(num_seats)]
                    for booking_id, seat, passenger_name in zip(booking_ids, selected_seats, passenger_names):
                        session.execute(insert_booking_query, (booking_id, passenger_name, seat))

                    updated_booked_seats = booked_seats.union(selected_seats)
                    capacity -= len(selected_seats)
                    session.execute(update_flight_query, (updated_booked_seats, capacity))

                    for booking_id, seat, passenger_name in zip(booking_ids, selected_seats, passenger_names):
                        session.execute(insert_booking_query, (booking_id, passenger_name, seat))

                    return list(selected_seats)
                
        given_seats = []
        # if seats next to each other not avaliable give free seats from each row untill num_seats are provided
        for row_num in range(1, 31):
            seats = [f"{row_num}{seat}" for seat in "ABCDEF"]
            for seat in seats:
                if capacity == 0 or not passenger_names:
                    break
                if seat not in booked_seats:
                    print(seat)
                    booking_id = uuid.uuid4()
                    passenger_name = passenger_names.pop(0)
                    booked_seats = booked_seats.union({seat})
                    capacity -= 1
                    session.execute(update_flight_query, (booked_seats, capacity))
                    passenger_name = passenger_names.pop(0)
                    session.execute(insert_booking_query, (booking_id, passenger_name, seat))
                    given_seats.append(seat)
        if len(passenger_names < starting_len):
            return given_seats

        return None


    def deleteBooking(self, booking_id):
        booking_query = f"SELECT flight_id, seat_number FROM bookings WHERE booking_id = {booking_id}"
        result = session.execute(booking_query)
        if not result:
            return "Booking not found"
        
        row = result.one()
        flight_id = row.flight_id
        seat_number = row.seat_number
        
        delete_booking_query = f"DELETE FROM bookings WHERE booking_id = {booking_id}"
        session.execute(delete_booking_query)
        
        flights_query = f"SELECT capacity FROM flights WHERE flight_id = {flight_id}"
        capacity = session.execute(flights_query).one().capacity

        update_seats_query = f"UPDATE flights SET booked_seats = booked_seats - {{'{seat_number}'}}, capacity = {capacity + 1} WHERE flight_id = {flight_id}"
        session.execute(update_seats_query)
        
        return f"Booking {booking_id} removed, seat {seat_number} freed"

    def updateBooking(self, booking_id, flight_id):
        booking_query = f"SELECT flight_id, passenger_name, seat_number FROM bookings WHERE booking_id = {booking_id}"
        result = session.execute(booking_query).one()

        if not result:
            return "Booking not found"

        old_flight_id = result.flight_id
        passenger_name = result.passenger_name
        seat_number = result.seat_number

        result = self.addBooking(flight_id, 1, [passenger_name])
        if not result:
            return "No seats left on selected flight"

        self.deleteBooking(booking_id)

        return f"Booking {booking_id} updated to flight {flight_id}"

    def getAllBookingsByFlightId(self, flight_id):
        result_set = session.execute(f"SELECT * FROM bookings WHERE flight_id = {flight_id}")
        bookings = []
        for row in result_set:
            bookings.append(Booking.to_json(row.flight_id, row.booking_id, row.passenger_name, row.seat_number))
         
        return bookings
    
    def getBookingById(self, booking_id):
        result = session.execute(f"SELECT * FROM bookings WHERE booking_id = {booking_id}").one()
        if not result:
            return None
        return Booking.to_json(result.flight_id, result.booking_id, result.passenger_name, result.seat_number)
    
    def getAllBookings(self):
        result_set = session.execute("SELECT * FROM bookings")
        bookings = []
        for row in result_set:
            bookings.append(Booking.to_json(row.flight_id, row.booking_id, row.passenger_name, row.seat_number))
        return bookings
    
    def addSeatedBooking(self, booking):
        select_query = f"SELECT capacity, booked_seats FROM flights WHERE flight_id = {booking.flight_id}"
        result = session.execute(select_query).one()
        if not result:
            return "Flight not found"
        if booking.seat_number in result.booked_seats:
            return "Seat already booked"
        
        flight_insert_query = f"UPDATE flights SET booked_seats = booked_seats + {{'{booking.seat_number}'}}, capacity = {result.capacity - 1} WHERE flight_id = {booking.flight_id}"
        session.execute(flight_insert_query)
        
        insert_query = session.prepare("""
            INSERT INTO bookings (booking_id, flight_id, passenger_name, seat_number)
            VALUES (?, ?, ?, ?)
        """)
        session.execute(insert_query, (booking.booking_id, booking.flight_id, booking.passenger_name, booking.seat_number))
        return f"Booking {booking.booking_id} added"