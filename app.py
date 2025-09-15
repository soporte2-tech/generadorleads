import streamlit as st
import google.generativeai as genai
import time
import base64 # Importante: esta librería es necesaria para la imagen

# --- CONFIGURACIÓN DE LA PÁGINA ---
# Usamos layout="centered" para tener un contenedor principal centrado.
st.set_page_config(
    page_title="Generador de Leads IA",
    page_icon="🎯",
    layout="centered"
)

# --- FUNCIÓN PARA CARGAR LA IMAGEN LOCAL COMO BASE64 ---
# Esta es la forma más robusta de mostrar imágenes locales en Streamlit Cloud.
def get_image_as_base64(file):
    try:
        with open(file, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except FileNotFoundError:
        st.error(f"Error: El archivo de imagen '{file}' no se encontró. Asegúrate de que está en la misma carpeta que app.py.")
        return None

# --- CONFIGURACIÓN DE LA API DE GEMINI ---
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except Exception as e:
    st.error("Error al configurar la API de Gemini. Asegúrate de que tu API key está en .streamlit/secrets.toml")
    st.stop()

# --- MANEJO DEL ESTADO DE LA PÁGINA ---
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# --- FUNCIONES AUXILIARES ---
def change_page(page_name):
    """Función para cambiar el estado de la página."""
    st.session_state.page = page_name

def call_gemini_api(user_description):
    """Función para llamar a la API de Gemini y obtener sugerencias."""
    model = genai.GenerativeModel('gemini-pro')
    prompt = f"""
    Basado en la siguiente descripción de una empresa, necesito que sugieras 5 tipos de negocios específicos que serían clientes potenciales ideales.
    Tu respuesta debe ser una lista clara y concisa en formato de puntos. No añadas explicaciones extra.

    Ejemplo de respuesta:
    - Tiendas de ropa boutique
    - Cafeterías de especialidad
    - Agencias de marketing digital

    Descripción de la empresa del usuario:
    "{user_description}"

    Tipos de negocio potenciales:
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"Ocurrió un error al contactar con la IA: {e}")
        return None

# --- VISTAS DE LA APLICACIÓN (PÁGINAS) ---

# Página 1: Landing Page
if st.session_state.page == 'home':
    
    # 1. Cargar y mostrar el logo centrado con un tamaño específico.
    img_base64 = get_image_as_base64("dpi.jpg")
    if img_base64:
        st.markdown(
            f'<div style="text-align: center;"><img src="data:image/jpeg;base64,{img_base64}" alt="DPI Logo" width="250"></div>',
            unsafe_allow_html=True
        )

    # 2. Centrar el texto usando Markdown con HTML/CSS.
    st.markdown("<h1 style='text-align: center;'>Generador de Leads con IA 🚀</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Potencia tu negocio encontrando los clientes perfectos para ti.</p>", unsafe_allow_html=True)
    
    st.write("") # Espacio en blanco
    
    # 3. Centrar el botón usando el truco de las columnas.
    col1_btn, col2_btn, col3_btn = st.columns([1, 2, 1])
    with col2_btn:
        if st.button("✨ ¡Comenzar ahora!", use_container_width=True, type="primary"):
            change_page('choice')
            st.rerun()

# Página 2: Página de Elección
elif st.session_state.page == 'choice':
    st.header("¿Cómo quieres buscar tus leads?")
    st.markdown("Elige una opción para continuar:")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🎯 Tengo claro el tipo de negocio", use_container_width=True):
            change_page('specific_search')
            st.rerun()
    
    with col2:
        if st.button("🤖 ¡Quiero que la IA me ayude!", use_container_width=True):
            change_page('ai_help')
            st.rerun()
            
    if st.button("⬅️ Volver al inicio"):
        change_page('home')
        st.rerun()

# Página 3: Página de Ayuda de la IA
elif st.session_state.page == 'ai_help':
    st.header("🧠 Describe tu empresa a la IA")
    st.info("Cuanto más detallada sea tu descripción, mejores serán las sugerencias. ¿Qué vendes? ¿A quién le sirve tu producto o servicio?")

    user_description = st.text_area("Describe tu empresa aquí:", height=150, placeholder="Ej: Somos una empresa que vende software de contabilidad en la nube para pequeñas y medianas empresas en España...")

    if st.button("Generar ideas de negocio", type="primary"):
        if user_description:
            with st.spinner("La IA está analizando tu empresa y buscando los mejores clientes..."):
                suggestions = call_gemini_api(user_description)
            
            if suggestions:
                st.success("¡Hecho! Aquí tienes algunas ideas de negocios a los que podrías vender:")
                st.markdown(suggestions)
                st.markdown("---")
                st.info("Ahora puedes usar estas ideas en la búsqueda específica o volver para empezar de nuevo.")
        else:
            st.warning("Por favor, describe tu empresa antes de continuar.")

    if st.button("⬅️ Volver a elegir"):
        change_page('choice')
        st.rerun()

# Página 4: Búsqueda Específica (Placeholder)
elif st.session_state.page == 'specific_search':
    st.header("🔍 Búsqueda Específica de Negocios")
    st.info("Introduce un tipo de negocio y una ubicación para generar la lista de leads.")

    business_type = st.text_input("Tipo de negocio", placeholder="Ej: Restaurante, Tienda de ropa, Taller mecánico")
    location = st.text_input("Ubicación (Ciudad, País)", placeholder="Ej: Madrid, España")

    if st.button("Buscar Leads y Generar Excel", type="primary"):
        st.success(f"¡Funcionalidad en desarrollo! Aquí se buscarían '{business_type}' en '{location}' y se generaría el Excel.")
        # Aquí iría la lógica futura para buscar los leads y generar el archivo Excel.

    if st.button("⬅️ Volver a elegir"):
        change_page('choice')
        st.rerun()
