import psycopg2
import os

class Database:
    def __init__(self, dbname, user, password, host):
        self.conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host)
        self.cur = self.conn.cursor()

    def get_all_flights(self):
        query = """
            SELECT * FROM flights
        """
        self.cur.execute(query)
        flights = self.cur.fetchall()
        return flights

    def get_flight(self, identifier):
        query = """
            SELECT * FROM flights WHERE id = %s
        """
        self.cur.execute(query, (identifier,))
        flight = self.cur.fetchone()
        return flight
    
    def insert_flight(self, dic):
        insert_query = """
            INSERT INTO flights 
            (departure_airport_name, departure_airport_id, departure_airport_time, 
            arrival_airport_name, arrival_airport_id, arrival_airport_time, 
            duration, airplane, airline, airline_logo, 
            carbon_emissions, price, currency, airline_logo_url) 
            VALUES 
            (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            dic['departure_airport_name'], dic['departure_airport_id'], dic['departure_airport_time'],
            dic['arrival_airport_name'], dic['arrival_airport_id'], dic['arrival_airport_time'],
            dic['duration'], dic['airplane'], dic['airline'], dic['airline_logo'],
            dic['carbon_emissions'], dic['price'], dic['currency'], dic['airline_logo_url']
        )
        self.cur.execute(insert_query, values)
        self.conn.commit()

    def close(self):
        self.cur.close()
        self.conn.close()

if __name__ == "__main__":
    # dbname = os.environ['DATABASE_NAME']
    # user = os.environ['DATABASE_USER']
    # password = os.environ['DATABASE_PASSWORD']
    # host = 'db'

    dbname = 'flightsdb'
    user = 'postgres'
    password = 'postgres'
    host = 'localhost'

    db = Database(dbname, user, password, host)
