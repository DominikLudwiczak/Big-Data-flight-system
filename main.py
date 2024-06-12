from init import Init
from connect import Connect

conn = Connect()

init = Init(conn)
init.init('flights_system')

init.create_tables()
init.seed_data()

conn.close()
