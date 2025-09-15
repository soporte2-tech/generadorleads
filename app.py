import streamlit as st
import google.generativeai as genai
import time

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="Generador de Leads IA",
    page_icon="🎯",
    layout="centered"
)

# --- CONFIGURACIÓN DE LA API DE GEMINI ---
# Cargar la API Key desde los secretos de Streamlit
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except Exception as e:
    st.error("Error al configurar la API de Gemini. Asegúrate de que tu API key está en el archivo .streamlit/secrets.toml")
    st.stop()

# --- MANEJO DEL ESTADO DE LA PÁGINA ---
# Usamos st.session_state para movernos entre las "páginas" de la app.
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# --- FUNCIONES ---
def change_page(page_name):
    """Función para cambiar el estado de la página."""
    st.session_state.page = page_name

def call_gemini_api(user_description):
    """Función para llamar a la API de Gemini y obtener sugerencias."""
    model = genai.GenerativeModel('gemini-pro')
    prompt = f"""
    Basado en la siguiente descripción de una empresa, necesito que sugieras 5 tipos de negocios específicos que serían clientes potenciales ideales.
    Tu respuesta debe ser una lista clara y concisa. No añadas explicaciones extra, solo los nombres de los tipos de negocio.

    Ejemplo de respuesta:
    - Tiendas de ropa boutique
    - Cafeterías de especialidad
    - Agencias de marketing digital
    - Gimnasios y centros de yoga
    - Clínicas de fisioterapia

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
    st.image("https://streamlit.io/images/brand/streamlit-logo-secondary-colormark-darktext.png", width=200) # Reemplaza con la URL de tu logo
    st.title("Generador de Leads con IA 🚀")
    st.markdown("Potencia tu negocio encontrando los clientes perfectos para ti.")
    
    st.write("") # Espacio en blanco
    
    # Usamos columnas para centrar el botón
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        if st.button("✨ ¡Comenzar ahora!", use_container_width=True, type="primary"):
            change_page('choice')
            st.rerun() # Volver a ejecutar el script para mostrar la nueva página

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

    user_description = st.text_area("Describe tu empresa aquí:", height=150, placeholder="Ej: Somos una empresa que vende software de contabilidad en la nube para pequeñas y medianas empresas en España. Nuestro software automatiza la facturación y la gestión de impuestos.")

    if st.button("Generar ideas de negocio", type="primary"):
        if user_description:
            with st.spinner("La IA está analizando tu empresa y buscando los mejores clientes..."):
                suggestions = call_gemini_api(user_description)
            
            if suggestions:
                st.success("¡Hecho! Aquí tienes algunas ideas de negocios a los que podrías vender:")
                st.markdown(suggestions)
                st.markdown("---")
                st.write("Ahora puedes usar estas ideas en la búsqueda específica.")
        else:
            st.warning("Por favor, describe tu empresa antes de continuar.")

    if st.button("⬅️ Volver a elegir"):
        change_page('choice')
        st.rerun()

# (Placeholder) Página 4: Búsqueda Específica
elif st.session_state.page == 'specific_search':
    st.header("🔍 Búsqueda Específica de Negocios")
    st.info("Esta es la siguiente etapa. Aquí introducirás un tipo de negocio y una ubicación para generar la lista de leads.")

    business_type = st.text_input("Tipo de negocio", placeholder="Ej: Restaurante, Tienda de ropa, Taller mecánico")
    location = st.text_input("Ubicación (Ciudad, País)", placeholder="Ej: Madrid, España")

    if st.button("Buscar Leads y Generar Excel", type="primary"):
        st.success(f"¡Funcionalidad en desarrollo! Aquí se buscarían '{business_type}' en '{location}' y se generaría el Excel.")
        # Aquí iría la lógica para buscar los leads (usando otra API como Google Places)
        # y luego generar y ofrecer la descarga del archivo Excel.

    if st.button("⬅️ Volver a elegir"):
        change_page('choice')
        st.rerun()
