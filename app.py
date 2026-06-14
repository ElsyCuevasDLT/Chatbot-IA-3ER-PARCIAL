import streamlit as st
from asistente.motor import responder

st.set_page_config(page_title="ReciclaBot", page_icon="♻️", layout="centered")

st.markdown(
    """
    <style>
    .stApp {background: linear-gradient(180deg, #f4fff8 0%, #ffffff 60%);} 
    .titulo {font-size: 2.4rem; font-weight: 800; color: #1f6f43; margin-bottom: 0;}
    .subtitulo {color: #46675a; font-size: 1rem; margin-top: 0.2rem;}
    .tarjeta {background: #eafff1; border-left: 6px solid #2e9d5b; padding: 1rem; border-radius: 12px; margin: 1rem 0;}
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<p class="titulo">♻️ ReciclaBot</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitulo">Chatbot educativo para separar residuos correctamente.</p>', unsafe_allow_html=True)

st.markdown(
    '<div class="tarjeta">Escribe un residuo, por ejemplo: botella PET, caja de cartón, pila usada, celular viejo o aceite de cocina.</div>',
    unsafe_allow_html=True,
)

if "historial" not in st.session_state:
    st.session_state.historial = [
        {"rol": "assistant", "texto": "Hola, soy ReciclaBot. Dime qué residuo tienes y te digo cómo separarlo."}
    ]

for mensaje in st.session_state.historial:
    with st.chat_message(mensaje["rol"]):
        st.write(mensaje["texto"])

entrada = st.chat_input("Escribe aquí tu residuo...")

if entrada:
    st.session_state.historial.append({"rol": "user", "texto": entrada})
    salida = responder(entrada)
    texto_respuesta = f"{salida['respuesta']}\n\nCategoría detectada: **{salida['categoria']}** | Confianza: **{salida['confianza']}**"
    st.session_state.historial.append({"rol": "assistant", "texto": texto_respuesta})
    st.rerun()

with st.sidebar:
    st.header("Pruebas rápidas")
    st.write("- botella de plástico")
    st.write("- caja de cartón")
    st.write("- pila usada")
    st.write("- celular viejo")
    st.write("- aceite de cocina usado")
