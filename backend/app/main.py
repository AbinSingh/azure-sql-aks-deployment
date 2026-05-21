import os
from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL


app = FastAPI()

DB_SERVER = os.getenv("DB_SERVER")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

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

class User(BaseModel):
    username: str

@app.get("/")
def health():
    return {"status": "Backend running"}

@app.post("/users")
def create_user(user: User):

    with engine.connect() as conn:
        conn.execute(
            text("INSERT INTO users (username) VALUES (:username)"),
            {"username": user.username}
        )
        conn.commit()

    return {"message": "User stored successfully"}