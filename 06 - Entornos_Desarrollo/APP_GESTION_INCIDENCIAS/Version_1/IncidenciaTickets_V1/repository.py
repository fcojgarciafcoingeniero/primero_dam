from models import Technician, Ticket, TicketStatus
from db import get_connection
from typing import List, Optional
from sqlite3 import Row
#INSERTAR
#LISTAR
#TOMAR UNA FILA Y PASARLO A UN TICKET

class TechnicianRepository:
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

        return Technician(
            id= technician_id,
            name=technician.name,
            email=technician.email,
            active=technician.active
        )

    def find_all(self) -> List[Technician]:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM technicians")
        rows = cursor.fetchall()
        conn.close()
        return [self.map_row_to_technician(row) for row in rows]

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
        return self.map_row_to_technician(row)

    def map_row_to_technician(self, row: Row) -> Technician:
        return Technician(
            id = row[0],
            name=row[1],
            email=row[2],
            active=bool(row[3])
        )

class TicketRepository:
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

    def find_all(self) -> List[Ticket]:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tickets")
        rows = cursor.fetchall()
        conn.close()
        return [self.map_row_to_ticket(row) for row in rows]

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
        return self.map_row_to_ticket(row)

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
        return update

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

        return [self.map_row_to_ticket(row) for row in rows]
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