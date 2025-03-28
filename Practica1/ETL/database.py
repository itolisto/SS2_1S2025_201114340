import pyodbc

SERVER = 'DESKTOP-2TMTRTC\SQLEXPRESS'
USERNAME = 'usac'
PASSWORD = 'abcdeF1+'

connectionString = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER};UID={USERNAME};PWD={PASSWORD};Trusted_Connection=yes'

conn = pyodbc.connect(connectionString)

conn.autocommit = True

cursor = conn.cursor()

def close_conn():
    cursor.close()
    conn.close()

# C:\Users\Pat0\AppData\Local\Programs\Python\Launcher\