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

    def addFlight(self, flight_name, source, destination, departure_time, arrival_time, capacity, booked_seats):
        insert_query = f"""
            INSERT INTO flights (flight_id, flight_name, source, destination, departure_time, arrival_time, capacity, booked_seats)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        session.execute(insert_query, (flight_name, source, destination, departure_time, arrival_time, capacity, booked_seats))

    def deleteFlight(self, flightId):
        query = f"DELETE FROM flights WHERE flight_id = {flightId}"
        session.execute(query)
        query = f"DELETE FROM bookings WHERE flight_id = {flightId}"
        session.execute(query)