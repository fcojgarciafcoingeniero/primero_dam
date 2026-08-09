# ==========================================
# 0. IMPORTACIONES
# ==========================================
import streamlit as st
from streamlit_option_menu import option_menu # Importación de librería para opciones de menú
# En este caso se emplea para el diseño de pestañas
from service import Service
from db import init_db

import os
import sys
def obtener_ruta(archivo):
    """Permite que el código encuentre archivos ocultos dentro del .exe"""
    if getattr(sys, 'frozen', False):
        return os.path.join(sys._MEIPASS, archivo)
    return archivo


# ==========================================
# 1. CONFIGURACIÓN E INICIALIZACIÓN
# ==========================================
# Configuración por defecto de la página
st.set_page_config(
    page_title="Gestor de Incidencias",
    page_icon="🎫",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Inicialización segura de la BBDD; se delega al motor de SQLite
init_db()

# Instanciación del servicio y guardado en el estado de la sesión
if 'service' not in st.session_state:
    st.session_state.service = Service()

service = st.session_state.service


# ==========================================
# 2. VENTANAS MODALES (DIALOGS)
# ==========================================
#Ventana de confirmación de baja de un técnico

# Decorador para definir una función asociada a ventana de diálogo
@st.dialog("⚠️ Confirmar Baja de Técnico")

# Función asociada a esa ventana:
def dialog_confirmar_baja(id_tecnico, nombre_tecnico):
    st.warning(f"¿Estás completamente seguro de que deseas desactivar a **{nombre_tecnico}**?")
    st.write("Todas sus incidencias en progreso serán desasignadas y volverán a la cola en estado OPEN.")

    col_yes, col_no = st.columns(2)
    with col_yes:
        # Se presiona SI
        if st.button("SI", type="primary", width="stretch"):
            try:
                # Llamada al método para cambiar el estado de un técnico a desactivado
                # Actualizando la BBDD
                st.session_state.service.deactivate_technician(id_tecnico)
                st.rerun() # Re-ejecución de todo el script de Python
            # Captura de errores desde service.py
            except ValueError as e:
                st.error(str(e))
    with col_no:
        # Se presiona CANCELAR
        if st.button("NO, cancelar", width="stretch"):
            st.rerun() # Re-ejecución de todo el script de Python


# ==========================================
# 3. CARGA DEL ARCHIVO CSS PERSONALIZADO
# ==========================================

# Definición de una función para llevar a cabo la carga del archivo
def load_local_css(file_name):
    # Cálculo de la ruta absoluta dependiendo de si es un .exe o un script normal
    if getattr(sys, 'frozen', False):
        carpeta_base = sys._MEIPASS
    else:
        carpeta_base = os.path.dirname(os.path.abspath(__file__))

    # Unión de la ruta base con el nombre del archivo CSS
    ruta_css = os.path.join(carpeta_base, file_name)

    try:
        # Apertura y solo lectura del archivo; guardado en una variable del texto contenido
        with open(ruta_css, "r", encoding="utf-8") as f:
        # markdown carga el texto en la página entre las etiquetas <style>
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    # Manejo de error en caso de no encontrar el archivo
    except FileNotFoundError:
        st.warning(f"No se encontró el archivo CSS en: {ruta_css}")

# Ejecución de la función para cargar el archivo (pasado como parámetro)
load_local_css("style.css")


# ==========================================
# 4. CABECERA
# ==========================================
# Título de la APP, equivalente a un h1
st.title("🎫 SISTEMA DE GESTIÓN DE INCIDENCIAS")
# Línea divisoria horizontal
st.markdown("<hr>", unsafe_allow_html=True)


# ==========================================
# 5. MENÚ DE NAVEGACIÓN ("PESTAÑAS")
# ==========================================
selected = option_menu(
    # Devuelve el texto de la selección y lo guarda
    # en la variable selected

    # Oculta el título del Menú (ya tenemos el st.title)
    menu_title=None,
    # Textos de las pestañas
    options=["Ver Incidencias", "Técnicos", "Gestión y Asignación"],
    # Iconos de la librería Bootstrap Icons
    icons=["card-list", "person-badge", "gear"],
    # Pestaña por defecto al abrir app > 0 = la primera
    default_index=0,
    # Fuerza a mostrar el menú en horizontal (no vertical) = barra de pestañas
    orientation="horizontal",
    # Diccionario de estilos
    styles={
        # Contenedor principal de las pestañas
        "container": {
            "padding": "0",
            "background-color": "#c8d6e5",
            "border": "none",
            "box-shadow": "none",
            "max-width": "100%",
            "margin-bottom": "-2px",
            "position": "relative",
            "z-index": "10"
        },
        # Envoltura de todas las pestañas
        "nav": {
            "background-color": "#c8d6e5",
            "justify-content": "flex-start",
            "margin": "0",
            "padding": "0"
        },
        # Cada elemento / pestaña de navegación
        "nav-item": {
            "flex": "0 0 auto",
            "margin-right": "5px"
        },
        # Zona interactiva (de clic) real en la pestaña (todas)
        "nav-link": {
            "font-size": "1.05rem",
            "font-weight": "600",
            "color": "#475569",
            "background-color": "#e2e8f0",
            "border": "1px solid #64748b",
            "border-bottom": "1px solid #64748b",
            "border-radius": "8px 8px 0 0",
            "padding": "10px 20px"
        },
        # Zona interactiva (de clic) real en la pestaña (la seleccionada)
        "nav-link-selected": {
            "background-color": "#ffffff",
            "color": "#000000",
            "border-bottom": "2px solid #f1f5f9",
            "font-weight": "700"
        }
    }
)

# ==========================================
# 6. CONTENIDO DE LAS PESTAÑAS
# ==========================================
# Contenedor grande que contiene todas las operaciones/opciones
with st.container():
    # Inyección de un identificador del contenedor para darle estilo en CSS
    st.markdown("<div id='recuadro-principal'></div>", unsafe_allow_html=True)

    # ----------------------------------------
    # PESTAÑA 1: VER INCIDENCIAS
    # ----------------------------------------
    if selected == "Ver Incidencias":
        col1, col2 = st.columns([1.5, 1])

        # Columna de la izquierda: listado de tickets
        with col1:
            st.subheader("Listado de Tickets")

            # Botones de filtrado
            filtro = st.radio("Filtrar por estado:", ["Todos", "Abiertos (OPEN)"], horizontal=True,
                              label_visibility="collapsed")
            # Llamada a service para recuperar los tickets que cumplen el filtro
            tickets = service.get_all_tickets() if filtro == "Todos" else service.get_open_tickets()
            # Si hay tickets
            if tickets:
                # Desempaquetado y creación de diccionario válido para Streamlit
                datos_tickets = [{**t.__dict__, "status": t.status.value} for t in tickets]
                # Pintado de los datos como tabla
                st.dataframe(datos_tickets, width="stretch")
            else:
                st.info("No hay tickets que mostrar.")

        # Columna de la derecha: creación de un nuevo ticket
        with col2:
            st.subheader("➕ Nuevo Ticket")

            # Formulario
            with st.form("form_nuevo_ticket", clear_on_submit=True):
                titulo = st.text_input("Título de la incidencia")
                desc = st.text_area("Descripción detallada")
                email = st.text_input("Email del solicitante")

                # Botón de envio del formulario
                submit_ticket = st.form_submit_button("Crear Ticket", type="primary")

                # Al clicar el botón de envío
                if submit_ticket:
                    try:
                        # Llamada a service para crear un nuevo ticket
                        nuevo_ticket = service.create_ticket(titulo, desc, email)
                        st.success(f"Ticket #{nuevo_ticket.id} creado con éxito.")
                        st.rerun()
                    # Manejo de error en caso de algún formato de dato no válido
                    except ValueError as e:
                        st.error(str(e))

    # ----------------------------------------
    # PESTAÑA 2: TÉCNICOS
    # ----------------------------------------
    elif selected == "Técnicos":
        col1, col2 = st.columns([1.5, 1])

        # Columna de la izquierda: listado de técnicos y apartado de bajas
        with col1:
            st.subheader("👨‍🔧 Plantilla de Técnicos")
            # Llamada al service para recuperar todos los técnicos de la BBDD
            tecnicos = service.get_all_technician()

            # Si hay técnicos
            if tecnicos:
                # Conversión a diccionario válido para Streamlit y muestra en tabla
                st.dataframe([t.__dict__ for t in tecnicos], width="stretch")

                # SECCIÓN DE BAJA DE TÉCNICO
                st.markdown("#### ❌ Dar de baja a un técnico")
                # Nueva lista con "solo técnicos en activo"
                tecnicos_activos = [t for t in tecnicos if t.active]

                # Si hay técnicos en activo
                if tecnicos_activos:
                    # Creación de un formulario
                    with st.form("form_baja_tecnico"):
                        # Selector desplegable
                        # Almacena el ID de la selección
                        # aunque en pantalla muestra el nombre (gracias a la función lambda)
                        tecnico_id_baja = st.selectbox(
                            "Selecciona el técnico a desactivar:",
                            [t.id for t in tecnicos_activos],
                            format_func=lambda x: next(t.name for t in tecnicos_activos if t.id == x)
                        )

                        # Botón de envío de formulario para dar de baja
                        if st.form_submit_button("Dar de Baja", type="primary"):
                            nombre_tecnico = next(t.name for t in tecnicos_activos if t.id == tecnico_id_baja)
                            # Se pasa el ID y el nombre del técnico a la ventana modal programada anteriormente
                            dialog_confirmar_baja(tecnico_id_baja, nombre_tecnico)
                # Si NO hay técnicos en activo
                else:
                    st.info("No hay técnicos activos actualmente.")
            # Si NO hay técnicos
            else:
                st.info("No hay técnicos registrados.")

        # Columna de la derecha: creación de un nuevo técnico
        with col2:
            st.subheader("➕ Nuevo Técnico")
            # Formulario
            with st.form("form_nuevo_tecnico", clear_on_submit=True):
                nombre = st.text_input("Nombre completo")
                email_tech = st.text_input("Correo electrónico")
                submit_tech = st.form_submit_button("Registrar Técnico", type="primary")

                # Si se clica el botón de envío
                if submit_tech:
                    try:
                        # Llamada al service para registrar el nuevo técnico
                        nuevo_tecnico = service.register_technician(nombre, email_tech)
                        st.success(f"Técnico {nuevo_tecnico.name} registrado.")
                        # Reinicio de la app
                        st.rerun()
                    # Manejo de errores o excepciones (reglas de negocio)
                    except Exception as e:
                        st.error(f"Error: {e}")

    # ----------------------------------------
    # PESTAÑA 3: GESTIÓN Y ASIGNACIÓN
    # ----------------------------------------
    elif selected == "Gestión y Asignación":
        st.subheader("⚙️ Acciones Operativas")

        # Llamada al service para extraer todos los tickets y todos los técnicos de la BBDD
        todos_tickets = service.get_all_tickets()
        todos_tecnicos = service.get_all_technician()

        # Nueva lista con "solo los técnicos en activo"
        tecnicos_activos = [t for t in todos_tecnicos if t.active]

        # Caso de haber tickets y técnicos en la BBDD
        if todos_tickets and tecnicos_activos:
            # 2 columnas: una para el panel de Asignación y otra para el panel de Cierre de Tickets
            col_asig, col_cierre = st.columns(2)

            # Panel de Asignación
            with col_asig:
                # Formulario
                with st.form("form_asignar_ticket"):
                    st.markdown("#### 🔄 Asignar Técnico a Ticket")
                    # Desplegable para seleccionar el ticket a asignar
                    ticket_id_asignar = st.selectbox("Selecciona Ticket:", [t.id for t in todos_tickets])
                    # Desplegable para seleccionar el técnico a asignar
                    # (mediante ID, pero mostrando en pantalla el nombre)
                    tecnico_id_asignar = st.selectbox(
                        "Selecciona Técnico:",
                        [t.id for t in tecnicos_activos],
                        format_func=lambda x: next(t.name for t in tecnicos_activos if t.id == x)
                    )

                    # Botón de envío
                    if st.form_submit_button("Asignar Ticket", type="primary"):
                        try:
                            # Llamada al service para la asignación
                            service.assign_ticket(ticket_id_asignar, tecnico_id_asignar)
                            st.success("¡Asignación realizada con éxito!")
                            st.rerun() # Reinicio de la app
                        except ValueError as e:
                            st.warning(str(e))

            # Panel de Cierre
            with col_cierre:
                # Formulario
                with st.form("form_cerrar_ticket"):
                    st.markdown("#### 🔒 Cerrar Ticket")
                    # Desplegable para selección de ticket
                    ticket_id_cerrar = st.selectbox("Selecciona Ticket a cerrar:", [t.id for t in todos_tickets])

                    # Si se clica el botón
                    if st.form_submit_button("Cerrar Ticket", type="primary"):
                        try:
                            # Llamada al service para cerrar el ticket
                            service.close_ticket(ticket_id_cerrar)
                            st.success("¡Ticket cerrado correctamente!")
                            st.rerun() # Reinicio de la app
                        except ValueError as e:
                            st.error(str(e))
        else:
            st.warning("Debe haber al menos un ticket y un técnico registrados para realizar asignaciones.")