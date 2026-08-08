# Librería de Python para trabajar en SQLite
# SQLite es una BBDD relacional que no necesita servidor externo
import sqlite3
# Importación específica para Type Hinting (Anotaciones de tipo)
# Para usar como etiqueta para definir la salida de la función get_connection()
from sqlite3 import Connection

# Nombre de la BBDD (archivo en local)
DB_NAME = "gestionIncidencias.db"

# Conexion con la BBDD y retorno de la conexión en variable conn
def get_connection() -> Connection:
    conn = sqlite3.connect(DB_NAME)
    return conn

# Inicialización de la BBDD y tablas
def init_db() -> None:
    # Creación de la conexión
    conn = get_connection()
    # Objeto tipo cursor: interfaz para enviar sentencias SQL
    cursor = conn.cursor()
    # Método principal del objeto cursor, ejecuta las sentencias que se le pasan
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS technicians (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        active INTEGER NOT NULL CHECK (active IN (0,1))
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tickets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        created_by TEXT NOT NULL,
        status TEXT NOT NULL,
        technician_id INTEGER,
        FOREIGN KEY (technician_id) REFERENCES technicians(id) 
    )
    """)

    # Persistencia: grabado de datos en el BBDD
    conn.commit()
    # Corta conexión con BBDD y libera memoria
    conn.close()