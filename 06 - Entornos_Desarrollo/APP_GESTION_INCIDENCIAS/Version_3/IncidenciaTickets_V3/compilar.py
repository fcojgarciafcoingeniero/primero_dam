################
# IMPORTACIONES
################
# Módulo principal de ejecución interno de la librería PyInstaller
import PyInstaller.__main__
# Módulo Operating System para comunicación con el SO en que se ejecutan la app
# realizar tareas de bajo nivel, especialmente la gestión de archivos, carpetas y rutas
import os

################
# RUTAS
################
# Calcula la ruta absoluta exacta de la carpeta donde está tu proyecto en el disco duro
directorio_actual = os.path.abspath(os.path.dirname(__file__))

# Construye las rutas absolutas completas para asegurar que PyInstaller las encuentre sí o sí
ruta_app = os.path.join(directorio_actual, 'gestion_incidencias.py')
ruta_css = os.path.join(directorio_actual, 'style.css')

########################
# LLAMADA A PYINSTALLER
########################
# Llama al motor de PyInstaller pasándole una lista con todas las instrucciones de empaquetado
PyInstaller.__main__.run([
    'launch_gestion_incidencias.py', # Archivo principal que arrancará el .exe
    '--onefile', # Agrupa todo el proyecto en un único archivo ejecutable
    '--windowed', # Oculta la consola negra de Windows al hacer doble clic
    '--collect-all', 'streamlit', # Empaqueta el motor, dependencias y componentes visuales de Streamlit
    '--collect-all', 'streamlit_option_menu', # Empaqueta el código y los recursos web (frontend) del menú
    '--add-data', f'{ruta_app};.', # Incrusta el archivo principal de la interfaz dentro del .exe (en la raíz '.')
    '--add-data', f'{ruta_css};.' # Incrusta la hoja de estilos CSS dentro del .exe
])