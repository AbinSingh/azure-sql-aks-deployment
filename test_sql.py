from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

if __name__ == "__main__":
    import pyodbc

    print(pyodbc.drivers())

    DB_SERVER = "abin-sql-server-2026.database.windows.net"
    DB_NAME = "userdb"
    DB_USER = "sqladmin"
    DB_PASSWORD = "Mysql123"

    connection_url = URL.create(
        "mssql+pyodbc",
        username=DB_USER,
        password=DB_PASSWORD,
        host=DB_SERVER,
        port=1433,
        database=DB_NAME,
        query={
            "driver": "ODBC Driver 18 for SQL Server",
            "Encrypt": "yes",
            "TrustServerCertificate": "yes"
        }
    )

    engine = create_engine(connection_url)

    with engine.connect() as conn:

        result = conn.execute(text("SELECT name FROM sys.tables"))

        print("Connected successfully!\n")

        for row in result:
            print(row)