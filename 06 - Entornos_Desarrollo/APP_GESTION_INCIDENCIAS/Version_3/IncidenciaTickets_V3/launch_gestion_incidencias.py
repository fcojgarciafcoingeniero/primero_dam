################
# IMPORTACIONES
################

# Librería de Python que permite acceder a variables, parámetros y funciones específicos
# que interactúan de forma directa con el intérprete
import sys
# Módulo Operating System para comunicación con el SO en que se ejecutan la app
# realizar tareas de bajo nivel, especialmente la gestión de archivos, carpetas y rutas
import os
# Módulo para convertir rutas de texto a objeto inteligente con múltiples funciones
# Concretamente .home() para preguntar al SO ruta de la carpeta personal del usuario con sesión abierta
from pathlib import Path

# cli: módulo de Streamlit que contiene la interfaz de línea de comandos (CLI)
# Se usa en scripts de Python para ejecutar aplicaciones de forma programada
from streamlit.web import cli as stcli

# Importación de los archivos de backend para obligar a PyInstaller a incorporarlos en el ejecutable
# Entrará a leerlos y empaquetará sqlite3 y cualquier otra librería que se use
import db
import models
import repository
import service

###################
# PUNTO DE ENTRADA
###################
# Punto de entrada > solo se ejecuta si se viene de doble clic o ejecución directa del archivo por el usuario
if __name__ == '__main__':

    # ==============================================================
    # Creación previa de credenciales de Streamlit
    # ==============================================================
    try:
        # Cálculo de la ruta a la carpeta del usuario (Ej: C:\Users\Cliente)
        # mediante métido e Path y conversión a String
        ruta_usuario = str(Path.home())
        carpeta_streamlit = os.path.join(ruta_usuario, '.streamlit')

        # Creación de la carpeta oculta de credenciales de Streamlit si no existe
        os.makedirs(carpeta_streamlit, exist_ok=True)

        # Creación del archivo de configuración que Streamlit busca
        archivo_cred = os.path.join(carpeta_streamlit, 'credentials.toml')
        if not os.path.exists(archivo_cred):
            with open(archivo_cred, 'w') as f:
                f.write('[general]\nemail = ""\n')
    except Exception:
        # Si por algún motivo de permisos de Windows falla, se ignora
        pass
    # ==============================================================


    # Comprobación de si se está dentro del .exe (la carpeta secreta _MEIPASS)
    # Herramienta nativa de Python "get attribute"
    if getattr(sys, 'frozen', False):
        # Busca dentro del módulo sys,
        # intenta encontrar una variable llamada 'frozen'
        # y, si por algún motivo no existe, no da error y devuelve False

        # Si es un .exe, se coge la ruta secreta absoluta
        carpeta_base = sys._MEIPASS
    else:
        # Si se está en un script normal, se coge la ruta de esta carpeta
        carpeta_base = os.path.dirname(os.path.abspath(__file__))

    # Ruta donde se encuentra el script de la interfaz de la app
    ruta_script = os.path.join(carpeta_base, "gestion_incidencias.py")

    ######################################################
    # SIMULACIÓN DE EJECUCIÓN DE STREAMLIT DESDE TERMINAL
    ######################################################
    # Se pasa la ruta absoluta al motor de Streamlit
    # Simula la lectura de comando desde la terminal "streamlit run [ruta_absoluta]"
    sys.argv = [
        "streamlit",
        "run",
        ruta_script,
        # Oculta el botón de "Deploy" y las herramientas de desarrollador
        "--global.developmentMode=false",

        # Arranque de Streamlit en "modo máquina" y
        # que se salte cualquier tipo de bienvenida o recolección de estadísticas

        # Prohíbe a Streamlit recopilar datos de uso, lo que desactiva inmediatamente el mensaje del correo electrónico
        "--browser.gatherUsageStats=false",
        # Indica a Streamlit que se está ejecutando como un servidor de fondo sin pantalla de terminal interactiva, evitando que se quede esperando respuestas del teclado.
        # "--server.headless=true"
        "--theme.base=light"
    ]
    # stcli.main(): coge esas instrucciones y arranca el servidor de Streamlit
    # sys.exit: asegura liberación de memoria y cerrado del .exe al cerrar la ventana de la app
    sys.exit(stcli.main())