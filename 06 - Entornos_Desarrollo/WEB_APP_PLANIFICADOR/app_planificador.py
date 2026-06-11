# 0. Importación del framework y librerías utilizadas
import streamlit as st
import datetime
import time


# 1. CONFIGURACIÓN INICIAL DE LA PÁGINA WEB
st.set_page_config(page_title="Planificador diario de entrenamiento",page_icon="🏃️",layout="wide")

# 2. ENCABEZADOS Y TEXTO
st.title("PLANIFICADOR DIARIO DE ENTRENAMIENTO")
st.header("USUARIO")
st.subheader("Aplicación Para Planificar Tus Entrenos")

# 3. CÓDIGO EMBEBIDO
codigo = """
    #Importación de librería para uso de fechas
    import datetime
    """
st.code(codigo,language="python")

# 4. WIDGETS INTERACTIVOS
nombre = st.text_input("Nombre: ")
edad = st.number_input("Edad: ",min_value=0,max_value=120,value=18,step=1)

objetivo = st.radio("Selecciona tu objetivo:",
    ["Fuerza", "Resistencia", "Flexibilidad"],index=0)

ejercicios = st.multiselect("Elige los tipos de ejercicio:", ["Cardio","Pesas","Yoga","Pilates","HIIT"])

nivel = st.slider("Selecciona un nivel:",
    min_value=1,      # Valor mínimo
    max_value=10,     # Valor máximo
    value=5           # Valor por defecto
)

fecha = st.date_input("Fecha del entreno:",value=datetime.date.today())

if "rutinas_registradas" not in st.session_state:
    st.session_state.rutinas_registradas = 0

if st.button("Iniciar rutina"):
    st.session_state.rutinas_registradas += 1

    progreso = st.progress(0,"Descargando plan")

    for porcentaje in range(101):
        time.sleep(0.01)
        progreso.progress(porcentaje,"Descargando plan")
    progreso.progress(porcentaje, "Plan Descargado")

    st.success(
        f"Rutina iniciada"
        f"Total de rutinas registradas: {st.session_state.rutinas_registradas}"
    )

# 6. MULTIMEDIA
st.divider()
st.image("https://images.unsplash.com/photo-1534438327276-14e5300c3a48?auto=format&fit=crop&q=80&w=1280",
         caption="Tu zona de entrenamiento",
         use_container_width=True)

st.write("🎵 Audio Motivacional:")
st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3")

st.write("📺 Vídeo Demostrativo:")
st.video("https://www.youtube.com/watch?v=Mx_zIequTsc")

st.divider()

# 7. DISEÑO Y CONTENEDORES
columna_izq, columna_dcha = st.columns(2)

with columna_izq:
    st.info(f"""
        *Resumen de Tus Datos:**
        Nombre: {nombre if nombre else "No proporcionado"}
        
        Edad: {edad}
        
        Objetivo: {objetivo}
        
        Nivel: {nivel}/10
        
        Fecha: {fecha}
        
        Ejercicios: {", ".join(ejercicios) if ejercicios else "Ninguno"}
        """)

with columna_dcha:

    if objetivo == "Fuerza":
        tip = "💪 Sugerencia: Prioriza el descanso entre series pesadas (2-3 min) para recuperación."
    elif objetivo == "Resistencia":
        tip = "🏃 Sugerencia: Mantén una hidratación constante."
    else:
        tip = "🧘 Sugerencia: No bloquees la respiración durante el estiramiento."

    st.warning(tip)

with st.expander("Consejos adicionales para tu entreno"):
    st.write("""
    - Estiramientos:Realiza estiramientos dinámicos antes de empezar.
    - Hidratación: mantén una buena ingesa de líquido durante toda la sesión.
    - Tiempos de descanso: Respeta los tiempos establecidos.
    - Seguridad: Si sientes dolor agudo, detén el ejercicio inmediatamente.
    """)

# 8. MENSAJE FINAL
st.success("¡Rutina planificada con éxito!")