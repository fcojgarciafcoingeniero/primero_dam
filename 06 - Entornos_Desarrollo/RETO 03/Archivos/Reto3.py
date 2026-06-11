# Alumno: Francisco José García Franco
# Asignatura: Entornos de Desarrollo
# Módulo: 1º DAM UAX

#Importamos la librería stramlit para crear la página web
#Le damos alias st para hacer el código más claro
import streamlit as st

#Configuración inicial de la página
#EL título de la página contiene referencia al reto y el nombre del alumno
st.set_page_config(page_title="Reto 3 - Fco. José García Franco", page_icon="🌎", layout="wide")

# Título principal
st.title("Ciudades del mundo")
# Subtítulo
st.header("Imágenes y descripción")

# Creamos 3 columnas
columna1, columna2, columna3 = st.columns(3)
#Con with hacemos que la columna 1 trabaje como un contenedor
with columna1:
    st.image("img/Paris.jpg")
    #Con with creamos un contenedor para el elemento desplegable (expander)
    with st.expander("Paris"):
        st.write("Capital de Francia") #Contenido del desplegable

# Con with hacemos que la columna 2 trabaje como un contenedor
with columna2:
    st.image("img/New York.jpeg")
    # Con with creamos un contenedor para el elemento desplegable (expander)
    with st.expander("New York"):
        st.write("Ciudad de los rascacielos") #Contenido del desplegable

#Con with hacemos que la columna 3 trabaje como un contenedor
with columna3:
    st.image("img/Venecia.jpg")
    # Con with creamos un contenedor para el elemento desplegable (expander)
    with st.expander("Venecia"):
        st.write("Ciudad de los canales") #Contenido del desplegable