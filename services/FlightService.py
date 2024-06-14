from connect import session
from entities.Flight import Flight
from datetime import datetime
from cassandra.query import BatchStatement, SimpleStatement

class FlightService:

    def getFlight(self, flightId):
        result = session.execute(f"SELECT * FROM flights WHERE flight_id = {flightId}").one()
        if not result:
            return None
        return Flight.to_json(result.flight_id, result.departure_airport, result.arrival_airport, result.departure_time, result.arrival_time, result.capacity, result.booked_seats)

    def getAllFlights(self):
        result_set = session.execute("SELECT * FROM flights")
        flights = []
        for row in result_set:
            flights.append(Flight.to_json(
                row.flight_id,
                row.departure_airport,
                row.arrival_airport,
                row.departure_time,
                row.arrival_time,
                row.capacity,
                row.booked_seats
            ))
        return flights

    def addFlight(self, departure_airport, arrival_airport, departure_time, arrival_time):

        insert_query = session.prepare("""
            INSERT INTO flights (flight_id, departure_airport, arrival_airport, departure_time, arrival_time, capacity, booked_seats)
            VALUES (uuid(), ?, ?, ?, ?, 180, ?)
        """)
        session.execute(insert_query, (departure_airport, arrival_airport, departure_time, arrival_time, set()))

    def deleteFlight(self, flightId):
        # Step 1: Delete flight record from 'flights' table
        query = f"DELETE FROM flights WHERE flight_id = {flightId}"
        session.execute(query)

        # Step 2: Delete all bookings associated with the flight_id
        select_query = f"SELECT booking_id FROM bookings WHERE flight_id = {flightId}"
        rows = session.execute(select_query)

        batch = BatchStatement()

        for row in rows:
            delete_query = f"DELETE FROM bookings WHERE booking_id = {row.booking_id}"
            batch.add(SimpleStatement(delete_query))

        session.execute(batch)