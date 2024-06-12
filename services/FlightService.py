from connect import Connect

class FlightService:
    def __init__(self):
        conn = Connect()
        self.session = conn.getSession()

    def getFlight(self, flightId):
        result = self.session.execute(f"SELECT * FROM flights WHERE flight_id = {flightId}")
        return {    }

    def getAllFlights(self):
        result = self.session.execute("SELECT * FROM flights")
        return result

    def addFlight(self, departure_airport, arrival_airport, departure_time, arrival_time):
        insert_query = session.prepare("""
            INSERT INTO flights (flight_id, departure_airport, arrival_airport, departure_time, arrival_time, capacity, booked_seats)
            VALUES (uuid(), ?, ?, ?, ?, 180, ?)
        """)
        session.execute(insert_query, (departure_airport, arrival_airport, departure_time, arrival_time, set()))

    def deleteFlight(self, flightId):
        query = f"DELETE FROM flights WHERE flight_id = {flightId}"
        self.session.execute(query)
        query = f"DELETE FROM bookings WHERE flight_id = {flightId}"
        self.session.execute(query)