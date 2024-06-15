import uuid
from connect import session

class Init:
    def init(self, keyspace_name):
        # cluster = self.conn.get_cluster()
        # metadata = cluster.metadata
        
        if keyspace_name not in session.cluster.metadata.keyspaces:
            self.create_keyspace(keyspace_name)
            print(f'Created {keyspace_name} keyspace')
        query = f"USE {keyspace_name};"
        session.execute(query)
        print(f'Connected to {keyspace_name} keyspace')
        self.create_tables()
        self.seed_data()



    def create_keyspace(self, keyspace_name='flights_system'):
        query = f"CREATE KEYSPACE IF NOT EXISTS {keyspace_name}" + " WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '2'};"
        session.execute(query)
        session.set_keyspace(keyspace_name)

    def create_tables(self):
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

        index_query = 'CREATE INDEX IF NOT EXISTS ON bookings(flight_id);'
        session.execute(index_query)
        print('Tables created')

    def seed_data(self):
        query = f"SELECT COUNT(*) FROM flights;"
        result = session.execute(query)
        count = result.one()[0]
        if count > 0:
            print('Data already seeded')
            return

        flight_id = uuid.uuid4()
        booked_seats_str = "{" + ', '.join(map(lambda x: f"'{x}'", set(['1A', '2B']))) + "}"
        insert_flight_query = f"""
            INSERT INTO flights (flight_id, departure_airport, arrival_airport, departure_time, arrival_time, capacity, booked_seats)
            VALUES ({flight_id}, 'JFK', 'LAX', toTimestamp(now()), toTimestamp(now()), 178, {booked_seats_str})
        """
        session.execute(insert_flight_query)

        insert_query = session.prepare("""
            INSERT INTO bookings (booking_id, flight_id, passenger_name, seat_number)
            VALUES (uuid(), ?, ?, ?)
        """)

        booking_data = [
            (flight_id, 'John Cena', '1A'),
            (flight_id, 'Max Verstappen', '2B')
        ]

        for data in booking_data:
            session.execute(insert_query, data)

        print('Data seeded')
        