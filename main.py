from init import Init
# from connect import Connect
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controllers.FlightController import router as flight_router
from controllers.BookingContoller import router as booking_router

app = FastAPI()

origins = [
    "http://localhost:4200"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    init = Init()
    init.init('flights_system')

app.include_router(flight_router)
app.include_router(booking_router)
