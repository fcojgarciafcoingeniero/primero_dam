import os
from service import Service
from db import init_db


def pause_and_prompt() -> None:
    """
    Interrumpe el flujo de ejecución temporalmente.
    Permite al usuario auditar la base de datos en SQLite antes de continuar.
    """
    input("\n[Pausa] Operación finalizada. Presione [ENTER] para continuar al siguiente paso...")
    print("\n" + "=" * 80 + "\n")


def print_step_header(step_number: int, description: str) -> None:
    """Imprime un encabezado formal para cada acción secuencial."""
    print(f"--- PASO {step_number}: {description} ---")


def main() -> None:
    # ---------------------------------------------------------
    # PASO 1: Inicialización de la Infraestructura
    # ---------------------------------------------------------
    print_step_header(1, "Inicialización de la base de datos (Creación de tablas)")
    if os.path.exists("claseExperiencial.db"):
        print("Aviso: El archivo 'claseExperiencial.db' ya existe.")
        print("Para evitar errores de creación de tablas, asegúrese de haberlo borrado antes de esta prueba.")
    else:
        init_db()
        print("> Tablas 'technicians' y 'tickets' creadas exitosamente en el esquema relacional.")

    pause_and_prompt()

    # Instanciación de la capa de Lógica de Negocio
    service = Service()

    # ---------------------------------------------------------
    # PASO 2: Creación de Entidades (Técnicos)
    # ---------------------------------------------------------
    print_step_header(2, "Registro de técnicos operativos en el sistema")
    tech1 = service.register_technician("Ana García", "ana@techsolutions.com")
    tech2 = service.register_technician("Luis Pérez", "luis@techsolutions.com")
    print(f"> Entidad persistida: {tech1}")
    print(f"> Entidad persistida: {tech2}")

    pause_and_prompt()

    # ---------------------------------------------------------
    # PASO 3: Lectura General (Técnicos)
    # ---------------------------------------------------------
    print_step_header(3, "Consulta del listado completo de técnicos")
    all_techs = service.get_all_technician()
    for t in all_techs:
        print(f"  - {t}")

    pause_and_prompt()

    # ---------------------------------------------------------
    # PASO 4: Creación de Entidades (Tickets)
    # ---------------------------------------------------------
    print_step_header(4, "Registro de nuevas incidencias (Estado inicial: OPEN)")
    ticket1 = service.create_ticket("Fallo en red", "Pérdida de paquetes en planta baja", "empleado1@empresa.com")
    ticket2 = service.create_ticket("Hardware dañado", "Teclado sin respuesta", "empleado2@empresa.com")
    print(f"> Entidad persistida: {ticket1}")
    print(f"> Entidad persistida: {ticket2}")

    pause_and_prompt()

    # ---------------------------------------------------------
    # PASO 5: Lectura Filtrada (Tickets Abiertos)
    # ---------------------------------------------------------
    print_step_header(5, "Consulta de incidencias pendientes (Tickets ABIERTOS)")
    open_tickets = service.get_open_tickets()
    for t in open_tickets:
        print(f"  - {t}")

    pause_and_prompt()

    # ---------------------------------------------------------
    # PASO 6: Modificación / Regla de Negocio (Asignación)
    # ---------------------------------------------------------
    print_step_header(6, "Asignación de un técnico a una incidencia")
    print(f"> Asignando el Ticket ID {ticket1.id} al Técnico ID {tech1.id}...")
    service.assign_ticket(ticket1.id, tech1.id)
    print("> Operación exitosa. El estado en base de datos debe ser ahora IN_PROGRESS y contener la clave foránea.")

    pause_and_prompt()

    # ---------------------------------------------------------
    # PASO 7: Búsqueda por Identificador
    # ---------------------------------------------------------
    print_step_header(7, "Recuperación de entidad específica por ID")
    updated_ticket = service.get_ticket_by_id(ticket1.id)
    print(f"> Estado actual de la entidad modificada: {updated_ticket}")

    pause_and_prompt()

    # ---------------------------------------------------------
    # PASO 8: Modificación / Regla de Negocio (Cierre)
    # ---------------------------------------------------------
    print_step_header(8, "Cierre de incidencia completada")
    print(f"> Procesando cierre para el Ticket ID {ticket1.id}...")
    service.close_ticket(ticket1.id)
    print("> Operación exitosa. El estado en base de datos debe ser ahora CLOSED.")

    pause_and_prompt()

    # ---------------------------------------------------------
    # PASO 9: Lectura General y Verificación Final
    # ---------------------------------------------------------
    print_step_header(9, "Consulta del listado completo de incidencias (Auditoría final)")
    final_tickets = service.get_all_tickets()
    for t in final_tickets:
        print(f"  - {t}")

    print("\n>>> Secuencia de pruebas completada. <<<")


if __name__ == "__main__":
    main()