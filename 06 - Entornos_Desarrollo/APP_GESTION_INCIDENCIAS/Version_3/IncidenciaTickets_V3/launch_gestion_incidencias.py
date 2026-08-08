################
# IMPORTACIONES
################

# Librería de Python que permite acceder a variables, parámetros y funciones específicos
# que interactúan de forma directa con el intérprete
import sys
# Módulo Operating System para comunicación con el SO en que se ejecutan la app
# realizar tareas de bajo nivel, especialmente la gestión de archivos, carpetas y rutas
import os
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
    sys.argv = ["streamlit", "run", ruta_script, "--global.developmentMode=false"]
    # stcli.main(): coge esas instrucciones y arranca el servidor de Streamlit
    # sys.exit: asegura liberación de memoria y cerrado del .exe al cerrar la ventana de la app
    sys.exit(stcli.main())