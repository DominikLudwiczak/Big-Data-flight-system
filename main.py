from init import Init
from connect import Connect
from fastapi import FastAPI

app = FastAPI()

conn = Connect()
session = conn.get_session()

@app.on_event("startup")
def startup_event():
    init = Init(conn)
    init.init('flights_system')

@app.get("/flights")
def read_root():
    booking_query = f"SELECT * FROM flights WHERE"
    result = session.execute(booking_query).fetchall()
    return True, result
