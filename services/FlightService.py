from connect import session

class FlightService:
    def getFlight(self, flightId):
        result = session.execute(f"SELECT * FROM flights WHERE flight_id = {flightId}")
        return result

    def getAllFlights(self):
        result = session.execute("SELECT * FROM flights")
        for row in result:
            print(row)
        return result

    def addFlight(self, departure_airport, arrival_airport, departure_time, arrival_time):
        insert_query = session.prepare("""
            INSERT INTO flights (flight_id, departure_airport, arrival_airport, departure_time, arrival_time, capacity, booked_seats)
            VALUES (uuid(), ?, ?, ?, ?, 180, ?)
        """)
        session.execute(insert_query, (departure_airport, arrival_airport, departure_time, arrival_time, set()))

    def deleteFlight(self, flightId):
        query = f"DELETE FROM flights WHERE flight_id = {flightId}"
        session.execute(query)
        query = f"DELETE FROM bookings WHERE flight_id = {flightId}"
        session.execute(query)