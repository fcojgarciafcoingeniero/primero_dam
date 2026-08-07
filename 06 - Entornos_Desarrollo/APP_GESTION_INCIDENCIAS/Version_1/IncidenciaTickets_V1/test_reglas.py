import os
from service2 import Service
from db import init_db


def test_reglas_negocio() -> None:
    print("=" * 60)
    print(" INICIANDO AUDITORÍA DE REGLAS DE NEGOCIO (RUTAS NEGATIVAS)")
    print("=" * 60 + "\n")

    # 0. Preparación del entorno
    if not os.path.exists("claseExperiencial.db"):
        init_db()
    service = Service()

    # ---------------------------------------------------------
    # PRUEBA 1: Título vacío o con espacios
    # ---------------------------------------------------------
    print("--- PRUEBA 1: Título de incidencia vacío ---")
    try:
        # Intentamos enviar un título compuesto solo por espacios
        service.create_ticket("   ", "El teclado no funciona", "usuario@empresa.com")
        print("❌ FALLO DE SEGURIDAD: El ticket se creó ignorando la regla.")
    except ValueError as error:
        # Si entra aquí, significa que nuestro 'raise ValueError' funcionó
        print(f"✅ BLOQUEO EXITOSO: {error}\n")

    # ---------------------------------------------------------
    # PRUEBA 2: Formato de email inválido
    # ---------------------------------------------------------
    print("--- PRUEBA 2: Email sin carácter especial (@) ---")
    try:
        # Intentamos enviar un email sin el arroba
        service.create_ticket("Fallo de red", "No hay internet", "usuario.empresa.com")
        print("❌ FALLO DE SEGURIDAD: El ticket se creó ignorando la regla.")
    except ValueError as error:
        print(f"✅ BLOQUEO EXITOSO: {error}\n")

    # ---------------------------------------------------------
    # PRUEBA 3: Cierre de ticket sin técnico asignado
    # ---------------------------------------------------------
    print("--- PRUEBA 3: Cerrar incidencia no asignada ---")
    try:
        # Primero, creamos un ticket válido para tener un registro real sobre el que operar
        ticket_valido = service.create_ticket("Pantalla azul", "El PC no arranca", "admin@empresa.com")
        print(f"  > (Preparación) Ticket ID {ticket_valido.id} creado con éxito.")
        print(f"  > Intentando forzar el cierre del Ticket ID {ticket_valido.id}...")

        # Ahora, intentamos cerrarlo inmediatamente, SIN invocar a 'assign_ticket' previamente
        service.close_ticket(ticket_valido.id)

        print("❌ FALLO DE SEGURIDAD: El ticket se cerró saltándose el flujo operativo.")
    except ValueError as error:
        print(f"✅ BLOQUEO EXITOSO: {error}\n")


if __name__ == "__main__":
    test_reglas_negocio()