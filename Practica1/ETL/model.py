import database

def create_model():
    try:
        db_result = database.cursor.execute("SELECT 1 FROM sys.databases WHERE name = 'seminario'").fetchall()

        if len(db_result) == 0:
            database.cursor.execute("USE master")
            database.cursor.execute("CREATE DATABASE seminario")
            database.cursor.execute("USE seminario")
            database.cursor.execute("DROP SCHEMA IF EXISTS practica1")
            database.cursor.execute("CREATE SCHEMA practica1")

            database.cursor.execute("""
                IF OBJECT_ID('practica1.dim_flight_status', 'U') IS NOT NULL
                    DROP TABLE practica1.dim_flight_status;


                IF OBJECT_ID('practica1.dim_nationality', 'U') IS NOT NULL
                    DROP TABLE practica1.dim_nationality;


                IF OBJECT_ID('practica1.dim_age', 'U') IS NOT NULL
                    DROP TABLE practica1.dim_age;


                IF OBJECT_ID('practica1.dim_gender', 'U') IS NOT NULL
                    DROP TABLE practica1.dim_gender;


                IF OBJECT_ID('practica1.dim_passenger', 'U') IS NOT NULL
                    DROP TABLE practica1.dim_passenger;


                IF OBJECT_ID('practica1.dim_pilot', 'U') IS NOT NULL
                    DROP TABLE practica1.dim_pilot;


                IF OBJECT_ID('practica1.dim_arrival_airport', 'U') IS NOT NULL
                    DROP TABLE practica1.dim_arrival_airport;


                IF OBJECT_ID('practica1.dim_departure_date', 'U') IS NOT NULL
                    DROP TABLE practica1.dim_departure_date;


                IF OBJECT_ID('practica1.dim_airport_continent', 'U') IS NOT NULL
                    DROP TABLE practica1.dim_airport_continent;


                IF OBJECT_ID('practica1.dim_departure_country', 'U') IS NOT NULL
                    DROP TABLE practica1.dim_departure_country;


                IF OBJECT_ID('practica1.dim_departure_airport', 'U') IS NOT NULL
                    DROP TABLE practica1.dim_departure_airport;


                IF OBJECT_ID('practica1.fact_flight', 'U') IS NOT NULL
                    DROP TABLE practica1.fact_flight;



                CREATE TABLE practica1.dim_departure_airport (
                    sk_id INTEGER NOT NULL,
                    airport_name NVARCHAR(255) NOT NULL,
                    PRIMARY KEY(sk_id)
                );


                CREATE TABLE practica1.dim_departure_country (
                    sk_id INTEGER NOT NULL,
                    country_name NVARCHAR(64) NOT NULL,
                    country_code NVARCHAR(4) NOT NULL,
                    PRIMARY KEY(sk_id)
                );


                CREATE TABLE practica1.dim_airport_continent (
                    sk_id INTEGER NOT NULL,
                    continent_code NVARCHAR(4) NOT NULL,
                    continent_name NVARCHAR(16) NOT NULL,
                    PRIMARY KEY(sk_id)
                );


                CREATE TABLE practica1.dim_departure_date (
                    sk_id INTEGER NOT NULL,
                    departure_date DATE NOT NULL,
                    month INTEGER NOT NULL,
                    day INTEGER NOT NULL,
                    year INTEGER NOT NULL,
                    PRIMARY KEY(sk_id)
                );


                CREATE TABLE practica1.dim_arrival_airport (
                    sk_id INTEGER NOT NULL,
                    arrival_airport NVARCHAR(8) NOT NULL,
                    PRIMARY KEY(sk_id)
                );


                CREATE TABLE practica1.dim_pilot (
                    sk_id INTEGER NOT NULL,
                    pilot_name NVARCHAR(64) NOT NULL,
                    PRIMARY KEY(sk_id)
                );


                CREATE TABLE practica1.dim_passenger (
                    sk_id NVARCHAR(64) NOT NULL UNIQUE,
                    sk_gender INTEGER NOT NULL,
                    sk_age INTEGER NOT NULL,
                    sk_nationality INTEGER NOT NULL,
                    first_name NVARCHAR(32) NOT NULL,
                    last_name NVARCHAR(32) NOT NULL,
                    PRIMARY KEY(sk_id)
                );


                CREATE TABLE practica1.dim_gender (
                    sk_id INTEGER NOT NULL,
                    gender NVARCHAR(8) NOT NULL,
                    PRIMARY KEY(sk_id)
                );


                CREATE TABLE practica1.dim_age (
                    sk_id INTEGER NOT NULL,
                    age INTEGER NOT NULL,
                    PRIMARY KEY(sk_id)
                );


                CREATE TABLE practica1.dim_nationality (
                    sk_id INTEGER NOT NULL,
                    nationality NVARCHAR(56) NOT NULL,
                    PRIMARY KEY(sk_id)
                );


                CREATE TABLE practica1.dim_flight_status (
                    sk_id INTEGER NOT NULL,
                    flight_status NVARCHAR(16) NOT NULL,
                    PRIMARY KEY(sk_id)
                );


                CREATE TABLE practica1.fact_flight (
                    id INTEGER IDENTITY(1,1) NOT NULL,
                    sk_airport_continent INTEGER NOT NULL,
                    sk_departure_country INTEGER NOT NULL,
                    sk_departure_airport INTEGER NOT NULL,
                    sk_departure_date INTEGER NOT NULL,
                    sk_arrival_airport INTEGER NOT NULL,
                    sk_pilot INTEGER NOT NULL,
                    sk_passenger NVARCHAR(64) NOT NULL,
                    sk_flight_status INTEGER NOT NULL,
                    PRIMARY KEY(id)
                );


                ALTER TABLE practica1.fact_flight
                ADD FOREIGN KEY(sk_airport_continent) REFERENCES practica1.dim_airport_continent(sk_id)
                ON UPDATE NO ACTION ON DELETE NO ACTION;

                ALTER TABLE practica1.fact_flight
                ADD FOREIGN KEY(sk_departure_country) REFERENCES practica1.dim_departure_country(sk_id)
                ON UPDATE NO ACTION ON DELETE NO ACTION;

                ALTER TABLE practica1.fact_flight
                ADD FOREIGN KEY(sk_departure_airport) REFERENCES practica1.dim_departure_airport(sk_id)
                ON UPDATE NO ACTION ON DELETE NO ACTION;

                ALTER TABLE practica1.fact_flight
                ADD FOREIGN KEY(sk_departure_date) REFERENCES practica1.dim_departure_date(sk_id)
                ON UPDATE NO ACTION ON DELETE NO ACTION;

                ALTER TABLE practica1.fact_flight
                ADD FOREIGN KEY(sk_arrival_airport) REFERENCES practica1.dim_arrival_airport(sk_id)
                ON UPDATE NO ACTION ON DELETE NO ACTION;

                ALTER TABLE practica1.fact_flight
                ADD FOREIGN KEY(sk_pilot) REFERENCES practica1.dim_pilot(sk_id)
                ON UPDATE NO ACTION ON DELETE NO ACTION;

                ALTER TABLE practica1.fact_flight
                ADD FOREIGN KEY(sk_passenger) REFERENCES practica1.dim_passenger(sk_id)
                ON UPDATE NO ACTION ON DELETE NO ACTION;

                ALTER TABLE practica1.dim_passenger
                ADD FOREIGN KEY(sk_gender) REFERENCES practica1.dim_gender(sk_id)
                ON UPDATE NO ACTION ON DELETE NO ACTION;

                ALTER TABLE practica1.dim_passenger
                ADD FOREIGN KEY(sk_age) REFERENCES practica1.dim_age(sk_id)
                ON UPDATE NO ACTION ON DELETE NO ACTION;

                ALTER TABLE practica1.dim_passenger
                ADD FOREIGN KEY(sk_nationality) REFERENCES practica1.dim_nationality(sk_id)
                ON UPDATE NO ACTION ON DELETE NO ACTION;

                ALTER TABLE practica1.fact_flight
                ADD FOREIGN KEY(sk_flight_status) REFERENCES practica1.dim_flight_status(sk_id)
                ON UPDATE NO ACTION ON DELETE NO ACTION;
            """)

            print("\nExito, modelo creado")
        else:
            print("\nElimina el modelo actual antes de crearlo de nuevo")

    except Exception as e:
        print(f"\nError al crear modelo: {e}")


def drop_model():
    try:
        db_result = database.cursor.execute("SELECT 1 FROM sys.databases WHERE name = 'seminario'").fetchall()

        if len(db_result) == 0:
            print("\nNo existe ningun modelo, para continuar presiona \"Enter\"...")
        else:
            database.cursor.execute("USE master")
            database.cursor.execute("DROP DATABASE IF EXISTS seminario")
            print("\nModelo eliminado, para continuar presiona \"Enter\"...")

    except Exception as e:
        print(f"\nError al borrar modelo: {e}")