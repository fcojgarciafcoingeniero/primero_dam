from enum import Enum
from dataclasses import dataclass
from typing import Optional

class TicketStatus(Enum):
    OPEN = "OPEN"
    IN_PROGRESS = "IN_PROGRESS"
    CLOSED = "CLOSED"

@dataclass
class Technician:
    id: Optional[int]
    name: str
    email: str
    active: bool = True

@dataclass
class Ticket:
    id: Optional[int]
    title: str
    description: str
    created_by: str
    status: TicketStatus
    technician_id: Optional[int] = None