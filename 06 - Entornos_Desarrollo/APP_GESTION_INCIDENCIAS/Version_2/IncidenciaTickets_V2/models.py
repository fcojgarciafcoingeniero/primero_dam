# Para creación de enumeraciones: grupo de nombres  vinculados a valores únicos
from enum import Enum
# Clase especial diseñada para guardar datos
# genera de forma automática métodos comunes
# __init__, __repr__, __eq__ ...
from dataclasses import dataclass
# Para indicar que una variable o resultado de una función puede ser de un tipo específico o None
from typing import Optional

# Estados posibles de un ticket
class TicketStatus(Enum):
    OPEN = "OPEN"
    IN_PROGRESS = "IN_PROGRESS"
    CLOSED = "CLOSED"

# Clase Technician > atributos: campos de la tabla
@dataclass # Los métodos comunes se generan automáticamente
class Technician:
    id: Optional[int]
    name: str
    email: str
    active: bool = True

# Clase Ticket > atributos: campos de la tabla
@dataclass # Los métodos comunes se generan automáticamente
class Ticket:
    id: Optional[int]
    title: str
    description: str
    created_by: str
    status: TicketStatus
    technician_id: Optional[int] = None