from repository import TechnicianRepository, TicketRepository
from models import Ticket,TicketStatus,Technician
from typing import List, Optional
class Service:
    def __init__(self):
        self.technician_repository = TechnicianRepository()
        self.ticket_repository = TicketRepository()

    def register_technician(self, name: str, email: str) -> Technician:
        technician = Technician(
            id = None,
            name=name,
            email=email
        )
        return self.technician_repository.create(technician)

    def create_ticket(self, title: str, description: str, created_by: str) -> Ticket:
        # 1. Validar que el título no esté vacío ni sea solo espacios
        if not title or len(title.strip()) == 0:
            raise ValueError("Regla de negocio fallida: El título del ticket no puede estar vacío.")

        # 2. Validar que el correo del creador contenga '@'
        if "@" not in created_by:
            raise ValueError("Regla de negocio fallida: El email del creador debe contener el carácter '@'.")

        # 3. Creación de la entidad si pasa las validaciones
        ticket = Ticket(
            id=None,
            title=title,
            description=description,
            created_by=created_by,
            status=TicketStatus.OPEN,
            technician_id=None
        )

        return self.ticket_repository.create(ticket)

    def assign_ticket(self, ticket_id:int, technician_id:int) -> None:
        ticket = self.ticket_repository.find_by_id(ticket_id)
        if ticket is None:
            raise ValueError(f"El ticket {ticket_id} no existe")
        technician = self.technician_repository.find_by_id(technician_id)

        if technician is None:
            raise ValueError(f"El tecnico {technician_id} no existe")
        if not technician.active:
            raise ValueError("El tecnico no esta activo")
        if ticket.status == TicketStatus.CLOSED:
            raise ValueError("No se puede asignar un ticket cerrado")

        update = self.ticket_repository.assign_technician(ticket_id, technician_id)
        if not update:
            raise ValueError("No se ha podido asignar un ticket")

    def close_ticket(self, ticket_id: int) -> None:
        ticket = self.ticket_repository.find_by_id(ticket_id)

        # Validaciones de existencia y estado (Ya estaban correctas)
        if ticket is None:
            raise ValueError(f"El ticket {ticket_id} no existe")
        if ticket.status == TicketStatus.CLOSED:
            raise ValueError("El ticket ya se encuentra cerrado")

        # NUEVA REGLA: Verificar que haya un técnico asignado
        if ticket.technician_id is None:
            raise ValueError("Regla de negocio fallida: No se puede cerrar un ticket sin un técnico asignado.")

        # Persistencia en base de datos
        update = self.ticket_repository.update_status(ticket_id, TicketStatus.CLOSED)
        if not update:
            raise ValueError("No se pudo cerrar el ticket debido a un error en la base de datos")

    def get_all_tickets(self) -> List[Ticket]:
        return self.ticket_repository.find_all()

    def get_all_technician(self) -> List[Technician]:
        return self.technician_repository.find_all()

    def get_open_tickets(self) -> List[Ticket]:
        return self.ticket_repository.find_open_tickets()

    def get_ticket_by_id(self, ticket_id: int) -> Optional[Ticket]:
        return self.ticket_repository.find_by_id(ticket_id)