import sqlite3
from sqlite3 import Connection

DB_NAME = "claseExperiencial.db"

def get_connection() -> Connection:
    conn = sqlite3.connect(DB_NAME)
    return conn

def init_db() -> None:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE technicians (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        active INTEGER NOT NULL CHECK (active IN (0,1))
    )
    """)

    cursor.execute("""
    CREATE TABLE tickets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        created_by TEXT NOT NULL,
        status TEXT NOT NULL,
        technician_id INTEGER,
        FOREIGN KEY (technician_id) REFERENCES technicians(id) 
    )
    """)

    conn.commit()
    conn.close()

