from init import Init
from fastapi import FastAPI

app = FastAPI()

@app.on_event("startup")
def startup_event():
    init = Init()
    init.init('flights_system')

@app.get("/")
def read_root():
    return {"Hello": "World"}
