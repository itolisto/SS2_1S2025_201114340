import pandas as pd

def extract():

    try:
        dataframe = pd.read_csv("C:/Users/Juan Enrique/seminario2/lab/practica1/VuelosDataSet.csv")
        print("\nCantidad de registros: ", len(dataframe))

        print("\nPrimeras 5 filas:")
        print(dataframe.head())

        print("\nUltimas 5 filas:")
        print(dataframe.tail(), '\n')

        return dataframe

    except Exception as e:
        print(f"Error leyendo el archivo: {e}")
        return 