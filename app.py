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
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except Exception as e:
    st.error("Error al configurar la API de Gemini. Asegúrate de que tu API key está en el archivo .streamlit/secrets.toml")
    st.stop()

# --- MANEJO DEL ESTADO DE LA PÁGINA ---
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# --- FUNCIONES ---
def change_page(page_name):
    st.session_state.page = page_name

def call_gemini_api(user_description):
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
    # --- INICIO DE LA SOLUCIÓN DEFINITIVA DE CENTRADO ---

    # 1. Centrar el logo con control de tamaño usando HTML/CSS dentro de Markdown.
    #    - Le damos un ancho fijo de 200px (puedes cambiarlo).
    #    - 'display: block' y 'margin: auto' son el truco CSS estándar para centrar imágenes.
    st.markdown(
        f"""
        <div style="text-align: center;">
            <img src="data:image/jpeg;base64,{base64.b64encode(open("dpi.jpg", "rb").read()).decode()}" alt="DPI Logo" width="200">
        </div>
        """,
        unsafe_allow_html=True
    )

    # 2. Centrar el texto (esto ya estaba bien).
    st.markdown("<h1 style='text-align: center;'>Generador de Leads con IA 🚀</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Potencia tu negocio encontrando los clientes perfectos para ti.</p>", unsafe_allow_html=True)
    
    st.write("") # Espacio en blanco
    
    # 3. Centrar el botón (el truco de las columnas funciona perfecto para botones).
    col1_btn, col2_btn, col3_btn = st.columns([1, 2, 1])
    with col2_btn:
        if st.button("✨ ¡Comenzar ahora!", use_container_width=True, type="primary"):
            change_page('choice')
            st.rerun()

    # --- FIN DE LA SOLUCIÓN ---

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

    user_description = st.text_area("Describe tu empresa aquí:", height=150, placeholder="Ej: Somos una empresa que vende software de contabilidad en la nube...")

    if st.button("Generar ideas de negocio", type="primary"):
        if user_description:
            with st.spinner("La IA está analizando tu empresa..."):
                suggestions = call_gemini_api(user_description)
            
            if suggestions:
                st.success("¡Hecho! Aquí tienes algunas ideas:")
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
    st.info("Introduce un tipo de negocio y una ubicación para generar la lista de leads.")

    business_type = st.text_input("Tipo de negocio", placeholder="Ej: Restaurante, Tienda de ropa")
    location = st.text_input("Ubicación (Ciudad, País)", placeholder="Ej: Madrid, España")

    if st.button("Buscar Leads y Generar Excel", type="primary"):
        st.success(f"¡Funcionalidad en desarrollo! Aquí se buscarían '{business_type}' en '{location}'.")
        
    if st.button("⬅️ Volver a elegir"):
        change_page('choice')
        st.rerun()
