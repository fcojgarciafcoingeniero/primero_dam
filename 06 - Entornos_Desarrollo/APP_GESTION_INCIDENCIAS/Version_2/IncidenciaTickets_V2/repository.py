# Importaciones
# Desde models: los 3 tipos de datos de la app
from models import Technician, Ticket, TicketStatus
# Desde db la función para establecer conexión con la BBDD
from db import get_connection
# List: para indicar que una variable/función usa como tipo de dato una lista
# Opitional: la variable o resultado de una función puede ser de un tipo específico o None
from typing import List, Optional
# Clase Row, optimizada para acceder a los resultados de una base de datos SQLite
# por nombre de columna o por índice numérico
from sqlite3 import Row

# CLASE TechnicianRepository > Métodos (ejecutan SQL):
class TechnicianRepository:
    # Crea un técnico > SQL: INSERT INTO
    def create(self, technician: Technician):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO technicians (name, email, active) VALUES (?,?,?)",
            (technician.name, technician.email, 1 if technician.active else 0)
        )

        conn.commit()

        technician_id = cursor.lastrowid

        conn.close()

        # Además devuelve un objeto del tipo Technician con los datos
        return Technician(
            id= technician_id,
            name=technician.name,
            email=technician.email,
            active=technician.active
        )
    # Busca todos los técnicos > SQL: SELECT * FROM technicians
    def find_all(self) -> List[Technician]:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM technicians")
        rows = cursor.fetchall()
        conn.close()
        # Convierte cada fila a objeto tipo Technician y lo devuelv (como Lista)
        return [self.map_row_to_technician(row) for row in rows]

    # Busca un ticket por ID > SQL: SELECT * FROM technicians WHERE id = ?
    def find_by_id(self, technician_id:int) -> Optional[Technician]:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM technicians WHERE id = ?",
            (technician_id,)
        )
        row = cursor.fetchone()
        if row is None:
            return None
        conn.close()
        # Devuelve el técnico como un objeto tipo Technician
        return self.map_row_to_technician(row)

    # Desactiva un técnico > SQL: UPDATE technicians SET active = 0 WHERE id = ?
    def deactivate(self, technician_id: int) -> bool:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
             "UPDATE technicians SET active = 0 WHERE id = ?",
            (technician_id,)
        )
        conn.commit()
        updated = cursor.rowcount > 0
        conn.close()
        # Devuelve un booleano informando de operación o no exitosa
        return updated

    # Conversión de una fila de tabla technicians a formato de objeto Technician
    def map_row_to_technician(self, row: Row) -> Technician:
        return Technician(
            id = row[0],
            name=row[1],
            email=row[2],
            active=bool(row[3])
        )

# CLASE TicketRepository > Métodos (ejecutan SQL):
class TicketRepository:

    # Crea un ticket > SQL: INSERT INTO
    def create(self, ticket: Ticket):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO tickets (title, description, created_by,status,technician_id) VALUES (?,?,?,?,?)",
            (ticket.title, ticket.description, ticket.created_by,ticket.status.value, ticket.technician_id)
        )

        conn.commit()

        ticket_id = cursor.lastrowid

        conn.close()

        return Ticket(
            id = ticket_id,
            title=ticket.title,
            description=ticket.description,
            created_by=ticket.created_by,
            status=ticket.status,
            technician_id=ticket.technician_id
        )

    # Busca todos los tickets > SQL: SELECT * FROM tickets
    def find_all(self) -> List[Ticket]:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tickets")
        rows = cursor.fetchall()
        conn.close()
        return [self.map_row_to_ticket(row) for row in rows]

    # Busca un ticket por ID > SQL: SELECT * FROM tickets WHERE id = ?"
    def find_by_id(self, ticket_id:int) -> Optional[Ticket]:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM tickets WHERE id = ?",
            (ticket_id,)
        )
        row = cursor.fetchone()
        if row is None:
            return None
        conn.close()
        # Conversión de la fila de la BBDD a un objeto tipo Ticket y lo devuelve
        return self.map_row_to_ticket(row)

    # Método que actualiza el estado de un ticket por su ID > SQL: UPDATE tickets SET status = ? WHERE id = ?
    def update_status(self, ticket_id:int, status: TicketStatus) -> bool:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE tickets SET status = ? WHERE id = ?",
            (status.value, ticket_id)
        )
        conn.commit()
        update = cursor.rowcount > 0
        conn.close()
        return update
    # Método de asignación de un técnico a un ticket dados sus IDs >
    # > SQL: UPDATE tickets SET technician_id = ?, status = ? WHERE id = ?
    # Actualiza la tabla tickets
    def assign_technician(self, ticket_id: int, technician_id:int) -> bool:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE tickets SET technician_id = ?, status = ? WHERE id = ?",
            (technician_id, TicketStatus.IN_PROGRESS.value, ticket_id)
        )
        conn.commit()
        update = cursor.rowcount > 0
        conn.close()
        # Devuelve un booleano que indica el éxito o no de la operación
        return update

    # NUEVO MÉTODO: Liberar tickets en progreso al dar de baja a un técnico dado su ID
    # > SQL: UPDATE tickets SET status = ?, technician_id = NULL WHERE technician_id = ? AND status = ?
    def unassign_active_tickets_from_technician(self, technician_id: int) -> int:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE tickets SET status = ?, technician_id = NULL WHERE technician_id = ? AND status = ?",
            (TicketStatus.OPEN.value, technician_id, TicketStatus.IN_PROGRESS.value)
        )
        conn.commit()
        rows_affected = cursor.rowcount
        conn.close()
        # Devuelve el número de filas afectadas
        return rows_affected

    # Búsqueda de todos los tickets abiertos > SQL: SELECT * FROM tickets WHERE status = ?
    def find_open_tickets(self) -> List[Ticket]:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT *
            FROM tickets
            WHERE status = ?
        """, (TicketStatus.OPEN.value, ))
        rows = cursor.fetchall()
        conn.close()
        # Conversión de cada fila a un objeto Ticket y devolucion de todos como Lista
        return [self.map_row_to_ticket(row) for row in rows]

    # Método de Conversión de una fila sacada de tabla tickets a formato de objeto Ticket
    def map_row_to_ticket(self, row: Row) -> Ticket:
        print(row[0])
        return Ticket(
            id = row[0],
            title=row[1],
            description=row[2],
            created_by=row[3],
            status=TicketStatus(row[4]),
            technician_id=row[5]
        )