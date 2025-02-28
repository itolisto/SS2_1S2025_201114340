import pyodbc

SERVER = 'localhost'
USERNAME = 'sa'
PASSWORD = 'abcdeF1+'

connectionString = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER};UID={USERNAME};PWD={PASSWORD};Trusted_Connection=no'

conn = pyodbc.connect(connectionString)

conn.autocommit = True

cursor = conn.cursor()

def close_conn():
    cursor.close()
    conn.close()