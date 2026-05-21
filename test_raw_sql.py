import pyodbc

server = 'abin-sql-server-2026.database.windows.net'
database = 'userdb'
username = 'sqladmin'
password = 'Mysql123'

conn = pyodbc.connect(
    'DRIVER={ODBC Driver 18 for SQL Server};'
    f'SERVER={server},1433;'
    f'DATABASE={database};'
    f'UID={username};'
    f'PWD={password};'
    'Encrypt=yes;'
    'TrustServerCertificate=yes;'
    'Connection Timeout=30;'
)

print("CONNECTED SUCCESSFULLY")