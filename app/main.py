from fastapi import FastAPI
from db import Database
from typing import Union
from datetime import datetime
import pytz
import os
from pydantic import BaseModel

# Datos de conexión PostgreSQL
# pg_dbname = os.environ['DATABASE_NAME']
# pg_user = os.environ['DATABASE_USER']
# pg_password = os.environ['DATABASE_PASSWORD']
# pg_host = 'db'

pg_dbname = 'flightsdb'
pg_user = 'postgres'
pg_password = 'postgres'
pg_host = 'localhost'

# Crear instancia de Database
db = Database(pg_dbname, pg_user, pg_password, pg_host)

# Crea una instancia de FastAPI y la almacena en la variable app.
app = FastAPI() 

class FlightData(BaseModel):
    price: int
    currency: str
    carbon_emissions: int
    airline_logo_url: str
    departure_airport_name: str
    departure_airport_id: str
    departure_airport_time: str
    arrival_airport_name: str
    arrival_airport_id: str
    arrival_airport_time: str
    duration: int
    airplane: str
    airline: str
    airline_logo: str


@app.get("/flights")
def get_all_flights(page: int = 1, count: int = 25, departure: Union[str, None] = None, 
                    arrival: Union[str, None] = None, date: Union[str, None] = None):
    flights = db.get_all_flights()
    list_flights = []
    flights_filtered = []

    actual_datetime = datetime.now(pytz.timezone('America/Santiago'))

    if departure and arrival == None and date == None:
        flights_filtered = [flight for flight in flights if flight[2] == departure]
    elif arrival and departure == None and date == None:
        flights_filtered = [flight for flight in flights if flight[5] == arrival]
    elif date and departure == None and arrival == None:
        flights_filtered = [flight for flight in flights if flight[3].strftime("%Y-%m-%d") == date and actual_datetime <= flight[3]]
    elif departure and arrival and date == None:
        flights_filtered = [flight for flight in flights if flight[2] == departure and flight[5] == arrival]
    elif departure and date and arrival == None:
        flights_filtered = [flight for flight in flights if flight[2] == departure and flight[3].strftime("%Y-%m-%d") == date and actual_datetime <= flight[3]]
    elif arrival and date and departure == None:
        flights_filtered = [flight for flight in flights if flight[5] == arrival and flight[3].strftime("%Y-%m-%d") == date and actual_datetime <= flight[3]]
    elif departure and arrival and date:
        flights_filtered = [flight for flight in flights if flight[2] == departure and flight[5] == arrival and flight[3].strftime("%Y-%m-%d") == date and actual_datetime <= flight[3]]
    else:
        flights_filtered = flights

    for i in range(count*(page - 1),(count)*page):
        if i < len(flights_filtered):
            list_flights.append(flights_filtered[i])
        else:
            break

    return {"flights": list_flights}


@app.get("/flights/{identifier}")
def get_flight(identifier: int):
    flight = db.get_flight(identifier)
    return {"flight": flight}

@app.post("/flights")
async def insert_flight(data: FlightData):
    try:
        db.insert_flight(data.model_dump())
        return {"message": "Flight inserted successfully"}
    except Exception as e:
        return {"message": f"An error ocurred inserting the flight: {e}"}

