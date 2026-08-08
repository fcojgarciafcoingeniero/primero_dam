# Importaciones
# Desde repository: clases que ejecutan el SQL (operaciones concretas en cada tabla)
from repository import TechnicianRepository, TicketRepository
# Desde models: los 3 tipos de datos de la app
from models import Ticket,TicketStatus,Technician
# List: para indicar que una variable/función usa como tipo de dato una lista
# Opitional: la variable o resultado de una función puede ser de un tipo específico o None
from typing import List, Optional

# Clase a llamar para ejecutar las acciones / servicio
class Service:
    def __init__(self):
        # Los atributos de las clases TechnicianRepository y TicketRepository
        # permitirán llamara a los métodos de estas que ejecutan las sentencias SQL
        self.technician_repository = TechnicianRepository()
        self.ticket_repository = TicketRepository()

    # Registrar un nuevo técnico
    def register_technician(self, name: str, email: str) -> Technician:
        # 1. Validar que el nombre no esté vacío ni sea solo espacios
        if not name or len(name.strip()) == 0:
            raise ValueError("ATENCIÓN: El nombre del técnico no puede estar vacío.")

        # 2. Validar que el correo contenga '@'
        if "@" not in email:
            raise ValueError("ATENCIÓN: El email del técnico debe contener el carácter '@'.")

        # 3. Creación de la entidad si pasa las validaciones
        technician = Technician(
            id=None,
            name=name,
            email=email
        )
        return self.technician_repository.create(technician)

    # Desactivación estricta de técnicos
    def deactivate_technician(self, technician_id: int) -> None:
        # Busca el técnico por ID
        technician = self.technician_repository.find_by_id(technician_id)
        if technician is None:
            raise ValueError(f"El técnico con ID {technician_id} no existe.")

        if not technician.active:
            raise ValueError(f"El técnico {technician.name} ya se encuentra inactivo.")

        # 1. Se liberan sus incidencias en progreso (vuelven a OPEN)
        self.ticket_repository.unassign_active_tickets_from_technician(technician_id)

        # 2. Se desactiva al técnico
        update = self.technician_repository.deactivate(technician_id)
        if not update:
            raise ValueError("No se pudo desactivar el técnico debido a un error en la base de datos.")

    # Registrar un nuevo ticket
    def create_ticket(self, title: str, description: str, created_by: str) -> Ticket:
        # 1. Validar que el título no esté vacío ni sea solo espacios
        if not title or len(title.strip()) == 0:
            raise ValueError("ATENCIÓN: El título del ticket no puede estar vacío.")

        # 2. Validar que el correo del creador contenga '@'
        if "@" not in created_by:
            raise ValueError("ATENCIÓN: El email del creador debe contener el carácter '@'.")

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

    # Asignar un ticket a un técnico
    def assign_ticket(self, ticket_id:int, technician_id:int) -> None:
        # Busca el ticket por ID
        ticket = self.ticket_repository.find_by_id(ticket_id)
        if ticket is None:
            raise ValueError(f"El ticket {ticket_id} no existe")
        # Busca el técnico por ID
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

    # Cerrar un ticket
    def close_ticket(self, ticket_id: int) -> None:
        # Busca por ID
        ticket = self.ticket_repository.find_by_id(ticket_id)

        # Validaciones de existencia y estado
        if ticket is None:
            raise ValueError(f"El ticket {ticket_id} no existe")
        if ticket.status == TicketStatus.CLOSED:
            raise ValueError("El ticket ya se encuentra cerrado")

        # NUEVA REGLA: Verificar que haya un técnico asignado
        if ticket.technician_id is None:
            raise ValueError("ATENCIÓN: No se puede cerrar un ticket sin un técnico asignado.")

        # Persistencia en base de datos
        update = self.ticket_repository.update_status(ticket_id, TicketStatus.CLOSED)
        if not update:
            raise ValueError("No se pudo cerrar el ticket debido a un error en la base de datos")

    # MÉTODOS QUE NO MODIFICAN LAS TABLAS DE LA BBDD
    # Búsqueda de todos los tickets
    def get_all_tickets(self) -> List[Ticket]:
        return self.ticket_repository.find_all()
    # Búsqueda de todos los técnicos
    def get_all_technician(self) -> List[Technician]:
        return self.technician_repository.find_all()
    # Búsqueda de todos los tickets abiertos
    def get_open_tickets(self) -> List[Ticket]:
        return self.ticket_repository.find_open_tickets()
    # Búsqueda de un ticket por ID
    def get_ticket_by_id(self, ticket_id: int) -> Optional[Ticket]:
        return self.ticket_repository.find_by_id(ticket_id)