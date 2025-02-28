from extract import extract
from transformation import transform
from load import load
import model as mdl
import querys as qrs
import os


clear = lambda: os.system('cls')

def displayMenu():
    data = None
    dataframe = None

    while True:
        clear()
        print("Seleccione una opción:")
        print("1. Borrar Modelo")
        print("2. Crear Modelo")
        print("3. Extraer datos")
        print("4. Transformar datos")
        print("5. Cargar datos")
        print("6. Realizar Consultas")
        print("7. Salir")

        def todo(): 
            print("implementacion pendiente") 

        option = input("\nOpción: ")

        dictionarySwitcher = {
            '1': mdl.drop_model,
            '2': mdl.create_model,
            '3': extract,
            '4': transform,
            '5': load,
            '6': qrs.display_querys,
            '7': exit,
        }

        if option == '3':
            dataframe = dictionarySwitcher[option]()
            option = input("press enter")
            continue    

        if option == "4":
            if dataframe is None:
                print('Extrae datos antes de transformar')
                option = input("press enter")
                continue

            data = dictionarySwitcher[option](dataframe.copy())
            option = input("press enter")
            continue

        if option == "5":
            if data is None:
                print('Transforma datos antes de insertarlo')
                option = input("press enter")
                continue
                
            dictionarySwitcher[option](data.copy())
            option = input("press enter")
            continue

        if option == "6":
            clear()
        
        if option == '':
            option = input("press enter")
            continue
        
        dictionarySwitcher[option]()

        option = input("press enter")

if __name__ == "__main__":
    displayMenu()