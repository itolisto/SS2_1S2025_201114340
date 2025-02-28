import database
import os
import pandas as pd

def display_querys():
    db_result = database.cursor.execute("SELECT 1 FROM sys.databases WHERE name = 'seminario'").fetchall()

    if len(db_result) == 0:
        print('\nno existe ningun modelo, crea modelo y carga datos antes de hacer consultas\n')
        return

    database.cursor.execute("USE seminario")

    while True:
        os.system('cls')

        print("Seleccione la consulta que desea hacer:")
        print('1. Contar las entradas en cada tabla')
        print('2. Porcentaje pasajeros por genero')
        print('3. Salidas por nacionalidad y mes')
        print('4. Conteo vuelos por pais')
        print('5. Top 5 aeropuertos con mas pasajeros')
        print('6. Conteo por estado de vuelo')
        print('7. Top 5 paises mas visitados')
        print('8. Top 5 continentes mas visitados')
        print('9. Top 5 Edades por genero que mas viajan')
        print('10. Conteo de vuelos por \'mes-año\'')
        print('11. Regresar')
        print('12. Salir')

        option = input('\nOpción: ')

        if option == '1':
            entradas_tablas()

        if option == '2':
            porcentaje_por_genero()

        if option == '3':
            salidas_nacionalidad_mes()

        if option == '4':
            vuelos_por_pais()

        if option == '5':
            top_aeropuerto_mas_pasajeros()

        if option == '6':
            total_estado_vuelo()

        if option == '7':
            top_paises_visitados()

        if option == '8':
            top_continentes_visitados()

        if option == '9':
            top_edades_genero()

        if option == '10':
            total_vuelos_mes_anio()

        if option == '11':
            return
        
        if option == '12':
            exit()

def entradas_tablas():

    result = database.cursor.execute("SELECT COUNT(sk_id) as C FROM practica1.dim_airport_continent").fetchval()

    print('\nEntradas en continentes de aeropuerto: ', result)

    result = database.cursor.execute("SELECT COUNT(sk_id) as C FROM practica1.dim_departure_country").fetchval()

    print('\nEntradas en paises de salida: ', result)

    result = database.cursor.execute("SELECT COUNT(sk_id) as C FROM practica1.dim_departure_airport").fetchval()

    print('\nEntradas en aeropuerto de salida: ', result)

    result = database.cursor.execute("SELECT COUNT(sk_id) as C FROM practica1.dim_departure_date").fetchval()

    print('\nEntradas fecha de salida: ', result)

    result = database.cursor.execute("SELECT COUNT(sk_id) as C FROM practica1.dim_arrival_airport").fetchval()

    print('\nEntradas aeropuerto destino: ', result)

    result = database.cursor.execute("SELECT COUNT(sk_id) as C FROM practica1.dim_pilot").fetchval()

    print('\nEntradas pilotos: ', result)

    result = database.cursor.execute("SELECT COUNT(sk_id) as C FROM practica1.dim_gender").fetchval()

    print('\nEntradas genero: ', result)

    result = database.cursor.execute("SELECT COUNT(sk_id) as C FROM practica1.dim_age").fetchval()

    print('\nEntradas edad: ', result)

    result = database.cursor.execute("SELECT COUNT(sk_id) as C FROM practica1.dim_nationality").fetchval()

    print('\nEntradas nacionalidades: ', result)

    result = database.cursor.execute("SELECT COUNT(sk_id) as C FROM practica1.dim_passenger").fetchval()

    print('\nEntradas pasajero: ', result)

    result = database.cursor.execute("SELECT COUNT(sk_id) as C FROM practica1.dim_flight_status").fetchval()

    print('\nEntradas estado de vuelo: ', result)

    result = database.cursor.execute("SELECT COUNT(id) as C FROM practica1.fact_flight").fetchval()

    print('\nEntradas hecho vuelo: ', result)

    input("\npress Enter to continue")


def porcentaje_por_genero():
    valuex = []
    valuex.append([1.1,2.2])
    
    total = database.cursor.execute("""
        SELECT COUNT(ff.id)
        FROM practica1.fact_flight ff
        RIGHT JOIN practica1.dim_passenger dp ON dp.sk_id = ff.sk_passenger
    """).fetchval()

    mujer_id = database.cursor.execute("""
        SELECT sk_id
        FROM practica1.dim_gender
        WHERE gender = 'Female'
    """).fetchval()

    mujer_porcentaje = database.cursor.execute(f"""
        SELECT (COUNT(ff.id)*100.0)/{total}
        FROM practica1.fact_flight ff
        LEFT JOIN practica1.dim_passenger dp ON dp.sk_id = ff.sk_passenger
        WHERE dp.sk_gender = {mujer_id}
    """).fetchval()

    hombre_porcentaje = 100.0 - float(mujer_porcentaje)

    print(f"mujeres: {mujer_porcentaje}")
    print(f"hombres: {hombre_porcentaje}")

    input("\npress Enter to continue")

def salidas_nacionalidad_mes():
    query ="""
        SELECT dn.nationality, ddd.year, ddd.month, COUNT(dn.sk_id) AS total
        FROM practica1.fact_flight ff
            RIGHT JOIN practica1.dim_departure_date ddd ON ddd.sk_id = ff.sk_departure_date
            RIGHT JOIN practica1.dim_passenger dp ON dp.sk_id = ff.sk_passenger
            RIGHT JOIN practica1.dim_nationality dn ON dn.sk_id = dp.sk_nationality
        GROUP BY
            dn.nationality,
            ddd.year,
            ddd.month
        ORDER BY
            dn.nationality,
            ddd.month
    """
    
    df = pd.read_sql_query(query, database.conn)

    print('\n')
    
    paises = df[['nationality']].drop_duplicates()

    df['fecha'] = df['month'].astype(str) + '-' + df['year'].astype(str)
    df['total'] = df['total'].astype(int)

    df = df.sort_values(by=['year','month'])

    fechas = df['fecha'].drop_duplicates()

    df_pivot = df.pivot_table(index="nationality", columns="fecha", values="total", fill_value='0').astype(int)
    df_pivot = df_pivot.reindex(columns=fechas, fill_value='0')

    df_pivot = df_pivot.reset_index()

    for row in df_pivot.iterrows():
        print(row)
    
    print('\n')
    # for r in result:
    print(df_pivot)

    input("\npress Enter to continue")

def stored_procedure_example():

    database.cursor.execute("""
        CREATE OR ALTER PROCEDURE practica1.percentage_by_gender
            @top INT
        AS
        BEGIN
            DECLARE @ans INT

            SELECT @ans = sk_id
            FROM practica1.dim_gender
            WHERE sk_id = @top

            RETURN @ans
        END
    """)
    
    result = database.cursor.execute("""
        DECLARE @generoid INT
        EXEC @generoid = practica1.percentage_by_gender @top = 1
        SELECT @generoid
    """).fetchval()

    print('\ngenero 1 es: ', result)
    
    result = database.cursor.execute("""
        DECLARE @generoid INT
        EXEC @generoid = practica1.percentage_by_gender @top = 2
        SELECT @generoid
    """).fetchval()

    print('\ngenero 2 es: ', result)

    input("\npress Enter to continue")


def vuelos_por_pais():
    query = """
        SELECT ddc.country_name, COUNT(ddc.sk_id) AS total 
        FROM practica1.fact_flight ff
        RIGHT JOIN practica1.dim_departure_country ddc ON ddc.sk_id = ff.sk_departure_country
        GROUP BY ddc.country_name
        ORDER BY ddc.country_name
    """

    df = pd.read_sql_query(query, database.conn)

    print('\n')

    for row in df.iterrows():
        index = row[0] + 1
        name = row[1]['country_name']
        total = row[1]['total']
        print(f'{index}.{name}: {total}')

    input("\npress Enter to continue")

def top_aeropuerto_mas_pasajeros():
    query = """
        SELECT TOP 5 dda.airport_name, COUNT(dda.sk_id) AS total 
        FROM practica1.fact_flight ff
        RIGHT JOIN practica1.dim_departure_airport dda ON dda.sk_id = ff.sk_departure_airport
        GROUP BY dda.airport_name
        ORDER BY total DESC
    """

    df = pd.read_sql_query(query, database.conn)

    print('\n', "Aeropuerto mas transitado de salidas:\n")

    print(df)

    query = """
        SELECT TOP 5 daa.arrival_airport, COUNT(daa.sk_id) AS total 
        FROM practica1.fact_flight ff
        RIGHT JOIN practica1.dim_arrival_airport daa ON daa.sk_id = ff.sk_departure_airport
        GROUP BY daa.arrival_airport
        ORDER BY total DESC
    """

    df = pd.read_sql_query(query, database.conn)

    print('\n', "Aeropuerto de destino mas transitados:\n")

    print(df)

    input("\npress Enter to continue")

def total_estado_vuelo():
    query = """
        SELECT dfs.flight_status, COUNT(dfs.sk_id) AS Total
        FROM practica1.fact_flight ff
        RIGHT JOIN practica1.dim_flight_status dfs ON dfs.sk_id = ff.sk_flight_status
        GROUP BY dfs.flight_status
    """
    df = pd.read_sql_query(query, database.conn)

    print('\n', df)

    input("\npress Enter to continue")

def top_paises_visitados():
    query = """
        SELECT TOP 5 ddc.country_name, COUNT(ddc.sk_id) as total
        FROM practica1.fact_flight ff
        RIGHT JOIN practica1.dim_departure_country ddc ON ddc.sk_id = ff.sk_departure_country
        GROUP BY ddc.country_name
        ORDER BY total DESC
    """
    df = pd.read_sql_query(query, database.conn)

    print('\n', df)

    input("\npress Enter to continue")

def top_continentes_visitados():
    query = """
        SELECT TOP 5 dac.continent_name, dac.continent_code, COUNT(dac.sk_id) as total
        FROM practica1.fact_flight ff
        RIGHT JOIN practica1.dim_airport_continent dac ON dac.sk_id = ff.sk_airport_continent
        GROUP BY 
            dac.continent_name,
            dac.continent_code
        ORDER BY total DESC 
    """
    df = pd.read_sql_query(query, database.conn)

    print('\n', df)

    input("\npress Enter to continue")

def top_edades_genero():
    mujer_id = database.cursor.execute("""
        SELECT sk_id
        FROM practica1.dim_gender
        WHERE gender = 'Female'
    """).fetchval()

    mujeres_query = f"""
        SELECT TOP 5 da.age, dg.gender, COUNT(da.sk_id) as total
        FROM practica1.fact_flight ff
        RIGHT JOIN practica1.dim_passenger dp ON dp.sk_id = ff.sk_passenger
        RIGHT JOIN practica1.dim_age da ON da.sk_id = dp.sk_age
        RIGHT JOIN practica1.dim_gender dg ON dg.sk_id = dp.sk_gender 
        WHERE dp.sk_gender = {mujer_id}
        GROUP BY 
            da.age,
            dg.gender
        ORDER BY total DESC
    """

    df = pd.read_sql_query(mujeres_query, database.conn)

    print('\nTop edades de mujeres: \n', df)

    
    hombre_id = database.cursor.execute("""
        SELECT sk_id
        FROM practica1.dim_gender
        WHERE gender = 'Male'
    """).fetchval()

    hombres_query = F"""
        SELECT TOP 5 da.age, dg.gender, COUNT(da.sk_id) as total
        FROM practica1.fact_flight ff
        RIGHT JOIN practica1.dim_passenger dp ON dp.sk_id = ff.sk_passenger
        RIGHT JOIN practica1.dim_age da ON da.sk_id = dp.sk_age
        RIGHT JOIN practica1.dim_gender dg ON dg.sk_id = dp.sk_gender 
        WHERE dp.sk_gender = {hombre_id}
        GROUP BY 
            da.age,
            dg.gender
        ORDER BY total DESC
    """

    df = pd.read_sql_query(hombres_query, database.conn)

    print('\nTop edades de hombres: \n', df)

    input("\npress Enter to continue")
    
def total_vuelos_mes_anio():
    query = """
        SELECT dd.month, dd.year, COUNT(dd.sk_id) as total
        FROM practica1.fact_flight ff
        RIGHT JOIN practica1.dim_departure_date dd ON dd.sk_id = ff.sk_departure_date
        GROUP BY 
            dd.month,
            dd.year
        ORDER BY
            dd.month,
            dd.year
    """

    df = pd.read_sql_query(query, database.conn)

    print('\n', df)

    input("\npress Enter to continue")
