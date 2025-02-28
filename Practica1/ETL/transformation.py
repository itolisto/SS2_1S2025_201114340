import pandas as pd

def transform(dataframe):
    dataframe.rename(columns={'Passenger ID': 'sk_id'}, inplace = True)
    dataframe.rename(columns={'First Name': 'first_name'}, inplace = True)
    dataframe.rename(columns={'Last Name': 'last_name'}, inplace = True)
    dataframe.rename(columns={'Gender': 'gender'}, inplace = True)
    dataframe.rename(columns={'Age': 'age'}, inplace = True)
    dataframe.rename(columns={'Nationality': 'nationality'}, inplace = True)
    dataframe.rename(columns={'Airport Name': 'airport_name'}, inplace = True)
    dataframe.rename(columns={'Airport Country Code': 'country_code'}, inplace = True)
    dataframe.rename(columns={'Country Name': 'country_name'}, inplace = True)
    dataframe.rename(columns={'Airport Continent': 'continent_code'}, inplace = True)
    dataframe.rename(columns={'Continents': 'continent_name'}, inplace = True)
    dataframe.rename(columns={'Departure Date': 'departure_date'}, inplace = True)
    dataframe.rename(columns={'Arrival Airport': 'arrival_airport'}, inplace = True)
    dataframe.rename(columns={'Pilot Name': 'pilot_name'}, inplace = True)
    dataframe.rename(columns={'Flight Status': 'flight_status'}, inplace = True)

    # PARA ACCEDER A UNA COLUMNA ESPECÍFICA DEL DATAFRAME, SE UTILIZA dataframe['NOMBRE DE LA COLUMNA']
    # ESTO PERMITE OBTENER UNA SERIE DE PANDAS QUE CONTIENE LOS VALORES DE ESA COLUMNA
    # CON ELLO, SE PUEDE APLICAR MÉTODOS DE PANDAS A ESA SERIE

    # UNA SITUACIÓN QUE SE PUEDE PRESENTAR ES QUE SE DESEE CREAR UNA DIMENSIÓN A PARTIR DE UNA COLUMNA DEL DATAFRAME
    # PARA ELLO, SE DEBE OBTENER LOS VALORES ÚNICOS DE ESA COLUMNA Y ASIGNARLES UN ID ÚNICO

    dim_airport_continent = dataframe[['continent_code', 'continent_name']].drop_duplicates()
    dim_airport_continent['sk_id'] = range(1, len(dim_airport_continent) + 1)

    print('\ncontinent_code dups: ', dim_airport_continent['continent_code'].duplicated().sum()) # Debe ser 0

    print('\ncontinent_name dups: ', dim_airport_continent['continent_name'].duplicated().sum())  # Debe ser 0

    print("\ndim_airport_continent:")
    print(dim_airport_continent.head())

    dim_departure_country = dataframe[['country_name', 'country_code']].drop_duplicates()
    dim_departure_country['sk_id'] = range(1, len(dim_departure_country) + 1)

    print('\ncountry_name dups: ', dim_departure_country['country_name'].duplicated().sum())  # Debe ser 0

    print('\ncountry_code dups: ', dim_departure_country['country_code'].duplicated().sum())

    print("\ndim_departure_country:")
    print(dim_departure_country.head())

    dim_departure_airport = dataframe[['airport_name']].drop_duplicates()   
    dim_departure_airport['sk_id'] = range(1, len(dim_departure_airport) + 1)

    print("\ndim_departure_airport:")
    print(dim_departure_airport.head())

    dataframe['departure_date'] = dataframe['departure_date'].apply(parse_dates)

    dim_departure_date = dataframe[['departure_date']].drop_duplicates()
    dim_departure_date['sk_id'] = range(1, len(dim_departure_date) + 1)

    dim_departure_date['year'] = dim_departure_date['departure_date'].dt.year
    dim_departure_date['month'] = dim_departure_date['departure_date'].dt.month
    dim_departure_date['day'] = dim_departure_date['departure_date'].dt.day
    
    print("\nDimDepartureDate:")
    print(dim_departure_date.head())

    dim_arrival_airport = dataframe[['arrival_airport']].drop_duplicates()
    dim_arrival_airport['sk_id'] = range(1, len(dim_arrival_airport) + 1)

    print("\ndim_arrival_airport:")
    print(dim_arrival_airport.head())

    dim_pilot = dataframe[['pilot_name']].drop_duplicates()
    dim_pilot['sk_id'] = range(1, len(dim_pilot) + 1)

    print("\ndim_pilot:")
    print(dim_pilot.head())

    dim_gender = dataframe[['gender']].drop_duplicates()
    dim_gender['sk_id'] = range(1, len(dim_gender) + 1)

    print("\ndim_gender:")
    print(dim_gender.head())

    dim_age = dataframe[['age']].drop_duplicates()
    dim_age['sk_id'] = range(1, len(dim_age) + 1)

    print("\ndim_age:")
    print(dim_age.head())

    dim_nationality = dataframe[['nationality']].drop_duplicates()
    dim_nationality['sk_id'] = range(1, len(dim_nationality) + 1)

    print("\ndim_nationality:")
    print(dim_nationality.head())    

    dim_passenger = dataframe[['sk_id', 'first_name', 'last_name', 'gender', 'age', 'nationality']].drop_duplicates()

    dim_passenger['sk_gender'] = dim_passenger['gender'].map(dim_gender.set_index('gender')['sk_id'])
    dim_passenger['sk_age'] = dim_passenger['age'].map(dim_age.set_index('age')['sk_id'])
    dim_passenger['sk_nationality'] = dim_passenger['nationality'].map(dim_nationality.set_index('nationality')['sk_id'])

    dim_passenger = dim_passenger[['sk_id', 'first_name', 'last_name', 'sk_gender', 'sk_age', 'sk_nationality']]

    # tenemos que convertirlo a string para poder insertarlo a la base de datos, no lo hicimos antes
    # para poder hacer el mapping que acabamos de hacer
    dim_age['age'] = dim_age['age'].astype(str)

    print("\ndim_passenger:")
    print(dim_passenger.head())

    dim_flight_status = dataframe[['flight_status']].drop_duplicates()
    dim_flight_status['sk_id'] = range(1, len(dim_flight_status) + 1)

    print("\ndim_flight_status:")
    print(dim_flight_status.head())
    
    # ENTONCES UTILIZANDO LOS ID DE LAS DIMENSIONES, SE DEBE RELACIONAR CON LA TABLA DE HECHOS CON LOS ID CORRESPONDIENTES
    # PARA ELLO SE PUEDE UTILIZAR LA FUNCIÓN map DE PANDAS

    # df['NOMBRE DE LA COLUMNA'].map(SERIE.set_index('NOMBRE DE LA COLUMNA')['NOMBRE DE LA COLUMNA A RELACIONAR'])
    # LA LÓGICCA DE ESTA FUNCIÓN ES LA SIGUIENTE:
    # 1. SE TOMA LA COLUMNA DEL DATAFRAME QUE SE DESEA RELACIONAR
    # 2. SE UTILIZA LA FUNCIÓN set_index PARA ESTABLECER LA COLUMNA COMO ÍNDICE DE LA SERIE
    # 3. SE RELACIONA LA COLUMNA DEL DATAFRAME CON LA SERIE UTILIZANDO map
    # 4. SE OBTIENE UNA SERIE CON LOS VALORES RELACIONADOS
    # 5. SE ASIGNA LA SERIE AL DATAFRAME CON df['NOMBRE DE LA COLUMNA RELACIONADA'] = SERIE


    # cambiar el nombre de la columna en el dataframe original a el nombre establecido en la tabla de hechos 
    dataframe.rename(columns={'sk_id': 'sk_passenger'}, inplace = True)

    # mapear a la llave surrogada usando las dos columnas para asegurar la integridad
    dataframe = dataframe.merge(dim_airport_continent, left_on = ['continent_code', 'continent_name'], right_on = ['continent_code', 'continent_name'], how = 'left', validate = 'm:1')

    # renombrar la key de la columna agregada al establecido en el modelo establecido
    dataframe.rename(columns={'sk_id': 'sk_airport_continent'}, inplace = True)

    print('\nairport continent keys:')    
    print(dataframe['sk_airport_continent'].head())

    # mapear a la llave surrogada usando las dos columnas para asegurar la integridad
    dataframe = dataframe.merge(dim_departure_country, left_on = ['country_code', 'country_name'], right_on = ['country_code', 'country_name'], how = 'left', validate = 'm:1')

    # renombrar la key de la columna agregada al establecido en el modelo establecido
    dataframe.rename(columns={'sk_id': 'sk_departure_country'}, inplace = True)

    print('\ndeparture country keys:')    
    print(dataframe['sk_departure_country'].head())

    dataframe['sk_departure_airport'] = dataframe['airport_name'].map(dim_departure_airport.set_index('airport_name')['sk_id'])

    dataframe['sk_departure_date'] = dataframe['departure_date'].map(dim_departure_date.set_index('departure_date')['sk_id'])

    dataframe['sk_arrival_airport'] = dataframe['arrival_airport'].map(dim_arrival_airport.set_index('arrival_airport')['sk_id'])

    dataframe['sk_pilot'] = dataframe['pilot_name'].map(dim_pilot.set_index('pilot_name')['sk_id'])

    dataframe['sk_flight_status'] = dataframe['flight_status'].map(dim_flight_status.set_index('flight_status')['sk_id'])

    fact_flight = dataframe[['sk_airport_continent', 'sk_departure_country', 'sk_departure_airport', 'sk_departure_date', 'sk_arrival_airport', 'sk_pilot', 'sk_passenger', 'sk_flight_status']]
    
    # verificar la cabeza de todos
    print("\nfact_flight:")
    print(fact_flight.head())

    print("\nNúmero total de registros:", len(fact_flight))

    print("\nTransformacion Completada con exito!")
    
    # retornar las dimensiones
    return [dim_airport_continent, dim_departure_country, dim_departure_airport, dim_departure_date, dim_arrival_airport, dim_pilot, dim_gender, dim_age, dim_nationality, dim_passenger, dim_flight_status, fact_flight]


# LAS FECHAS PUEDEN ESTAR EN FORMATO 'MM/DD/YYYY' O 'MM-DD-YYYY', POR LO QUE SE DEBE NORMALIZAR A UN FORMATO CONSISTENTE
def parse_dates(str_date):
    # SE RECORREN LOS FORMATOS DE FECHA HASTA ENCONTRAR UNO QUE FUNCIONE
    for fmt in ('%m/%d/%Y', '%m-%d-%Y'):
        try:
            # SE INTENTA CONVERTIR LA FECHA AL FORMATO '%Y-%m-%d' (YYYY-MM-DD) COMO LO REQUIERE SQL SERVER
            return pd.to_datetime(str_date, format=fmt)
        except ValueError:
            continue
        # SI NO SE PUDO CONVERTIR LA FECHA, SE RETORNA UN VALOR NULO (NaT)
    return pd.NaT