import streamlit as st
import google.generativeai as genai
import time
import base64
import re

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="Generador de Leads IA",
    page_icon="🎯",
    layout="centered"
)

# --- FUNCIÓN PARA CARGAR LA IMAGEN ---
def get_image_as_base64(file):
    try:
        with open(file, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except FileNotFoundError:
        st.error(f"Error: El archivo de imagen '{file}' no se encontró.")
        return None

# --- CONFIGURACIÓN DE LA API DE GEMINI ---
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except Exception as e:
    st.error("Error al configurar la API de Gemini.")
    st.stop()

# --- MANEJO DEL ESTADO DE LA PÁGINA ---
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'suggestions_list' not in st.session_state:
    st.session_state.suggestions_list = []
if 'user_description' not in st.session_state:
    st.session_state.user_description = ""


# --- FUNCIONES AUXILIARES ---
def change_page(page_name):
    st.session_state.page = page_name

def call_gemini_api(user_description):
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    prompt = f"""
    Basado en la siguiente descripción de una empresa, necesito que sugieras 5 tipos de negocios específicos que serían clientes potenciales ideales.
    Tu respuesta debe ser una lista clara y concisa en formato de puntos. No añadas explicaciones extra.

    Ejemplo de respuesta:
    - Tiendas de ropa boutique
    - Cafeterías de especialidad

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

def call_gemini_for_keywords(business_type, user_description):
    """Llama a la IA para sugerir keywords de filtrado específicas."""
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    prompt = f"""
    Eres un analista de datos especializado en encontrar clientes. Tu objetivo es identificar las palabras conceptuales más comunes y relevantes.

    **Contexto:**
    - Mi empresa vende: "{user_description}"
    - Busco este tipo de cliente: "{business_type}"

    **Tu Tarea:**
    Genera una lista de 5 a 7 palabras clave para filtrar. Estas palabras deben cumplir OBLIGATORIAMENTE las siguientes reglas:

    **Regla 1: UNA SOLA PALABRA.** Cada keyword debe ser una única palabra (ej. 'pienso' está bien, 'pienso natural' NO).
    **Regla 2: SIN MARCAS.** No incluyas nombres de marcas comerciales (ej. 'Royal Canin', 'Hills').
    **Regla 3: CONCEPTOS, NO PRODUCTOS ESPECÍFICOS.** Busca palabras que representen una categoría (ej. 'alimento'), no un producto ultra-específico (ej. 'dieta de prescripción').

    **Ejemplo Práctico:**
    - Si mi empresa vende "pienso para mascotas de alta calidad", y busco "Tiendas de mascotas"...
    - **Keywords CORRECTAS:** pienso, alimento, nutrición, comida, natural, premium, ecológico
    - **Keywords INCORRECTAS:** pienso veterinario, royal canin, dieta para perros

    **Formato de Salida:**
    Dame únicamente la lista de palabras clave en minúsculas, separadas por comas. Sin explicaciones.
    """
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        st.error(f"Ocurrió un error al generar keywords: {e}")
        return None

# --- VISTAS DE LA APLICACIÓN (PÁGINAS) ---

# Página 1: Landing Page
if st.session_state.page == 'home':
    img_base64 = get_image_as_base64("dpi.jpg")
    if img_base64:
        st.markdown(f'<div style="text-align: center;"><img src="data:image/jpeg;base64,{img_base64}" alt="DPI Logo" width="250"></div>', unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center;'>Generador de Leads con IA 🚀</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Potencia tu negocio encontrando los clientes perfectos para ti.</p>", unsafe_allow_html=True)
    st.write("")
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
    st.info("Cuanto más detallada sea tu descripción, mejores serán las sugerencias.")
    user_description = st.text_area("Describe tu empresa aquí:", height=150, placeholder="Ej: Vendemos piensos y accesorios de alta gama para mascotas...")
    if st.button("Generar ideas de negocio", type="primary"):
        if user_description:
            st.session_state.user_description = user_description
            with st.spinner("La IA está analizando tu empresa..."):
                suggestions_text = call_gemini_api(user_description)
                if suggestions_text:
                    clean_suggestions = re.findall(r'-\s*(.+)', suggestions_text)
                    st.session_state.suggestions_list = clean_suggestions
        else:
            st.warning("Por favor, describe tu empresa antes de continuar.")

    if st.session_state.suggestions_list:
        st.success("¡Hecho! Aquí tienes algunas ideas:")
        st.markdown("\n".join(f"- {s}" for s in st.session_state.suggestions_list))
        st.markdown("---")
        
        if st.button("✅ Usar estas ideas para la búsqueda", type="primary"):
            change_page('ai_results_to_search')
            st.rerun()

    if st.button("⬅️ Volver a elegir"):
        st.session_state.suggestions_list = []
        st.session_state.user_description = ""
        change_page('choice')
        st.rerun()

# Página 4: Perfeccionar Búsqueda con IA
elif st.session_state.page == 'ai_results_to_search':
    st.header("🎯 Perfecciona tu Búsqueda")
    
    # --- CAMBIO 1: CREAMOS UNA NUEVA LISTA CON LA OPCIÓN "TODAS" AL PRINCIPIO ---
    opcion_todas = "Buscar en todas las categorías sugeridas"
    opciones_display = [opcion_todas] + st.session_state.suggestions_list
    
    selected_option = st.selectbox(
        "Elige el tipo de negocio que quieres buscar:",
        options=opciones_display  # Usamos la nueva lista de opciones
    )
    
    location = st.text_input("Ubicación (Ciudad, País)", placeholder="Ej: Barcelona, España")

    st.markdown("---")

    st.subheader("Filtro por Palabras Clave (Opcional)")
    st.info("Añade palabras clave para encontrar negocios que las mencionen en su descripción. Déjalo en blanco si no quieres filtrar.")
    
    keywords = st.text_input("Keywords (separadas por comas)", placeholder="pienso, alimento, natural...")

    if st.button("🤖 Ayúdame a encontrar keywords"):
        # La lógica para generar keywords solo tiene sentido si se elige UNA categoría
        if selected_option != opcion_todas and st.session_state.user_description:
            with st.spinner(f"Buscando keywords para '{selected_option}'..."):
                suggested_keywords = call_gemini_for_keywords(selected_option, st.session_state.user_description)
                if suggested_keywords:
                    st.success("¡Sugerencia de keywords generada!")
                    st.code(suggested_keywords)
        elif selected_option == opcion_todas:
            st.warning("Para sugerir keywords, por favor, elige una categoría específica de la lista.")
        else:
            st.warning("Asegúrate de haber descrito tu empresa y elegido un tipo de negocio.")

    st.markdown("---")

    if st.button("Buscar Leads y Generar Excel", type="primary"):
        # --- CAMBIO 2: ADAPTAMOS EL MENSAJE SEGÚN LA OPCIÓN ELEGIDA ---
        if selected_option == opcion_todas:
            st.success(f"¡Funcionalidad en desarrollo! Se buscarían **TODAS** las categorías sugeridas en '{location}' con las keywords '{keywords}'.")
        else:
            st.success(f"¡Funcionalidad en desarrollo! Se buscarían '{selected_option}' en '{location}' con las keywords '{keywords}'.")

    if st.button("⬅️ Volver a las opciones"):
        change_page('choice')
        st.rerun()

# Página 5: Búsqueda Específica
elif st.session_state.page == 'specific_search':
    st.header("🔍 Búsqueda Específica de Negocios")
    st.info("Introduce un tipo de negocio y una ubicación para generar la lista de leads.")
    business_type = st.text_input("Tipo de negocio", placeholder="Ej: Restaurante, Taller mecánico")
    location = st.text_input("Ubicación (Ciudad, País)", placeholder="Ej: Madrid, España")
    if st.button("Buscar Leads y Generar Excel", type="primary"):
        st.success(f"¡Funcionalidad en desarrollo! Se buscarían '{business_type}' en '{location}'.")
    if st.button("⬅️ Volver a elegir"):
        change_page('choice')
        st.rerun()
