import psycopg2
import configparser
import os

# Conectarse a la base de datos
conn = psycopg2.connect(
    dbname='flightsdb',
    user='postgres',
    password='postgres',
    host='localhost'
)
print("Conexión exitosa")

# Crear un cursor
cur = conn.cursor()

# Verificar si la tabla ya existe
cur.execute("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'flights');")
table_exists = cur.fetchone()[0]

if table_exists:
    print("La tabla ya existe.")

else:
    # Crear la tabla si no existe
    sql_query = """
    CREATE TABLE flights (
        id SERIAL PRIMARY KEY,
        departure_airport_name VARCHAR(255),
        departure_airport_id VARCHAR(255),
        departure_airport_time TIMESTAMP WITH TIME ZONE DEFAULT timezone('America/Santiago', CURRENT_TIMESTAMP),
        arrival_airport_name VARCHAR(255),
        arrival_airport_id VARCHAR(255),
        arrival_airport_time TIMESTAMP WITH TIME ZONE DEFAULT timezone('America/Santiago', CURRENT_TIMESTAMP),
        duration NUMERIC,
        airplane VARCHAR(255),
        airline VARCHAR(255),
        airline_logo VARCHAR(255),
        carbon_emissions NUMERIC,
        price NUMERIC,
        currency CHAR(3),
        airline_logo_url VARCHAR(255)
    );
    """
    cur.execute(sql_query)
    conn.commit()
    print("Tabla creada exitosamente")


conn.close()
cur.close()
