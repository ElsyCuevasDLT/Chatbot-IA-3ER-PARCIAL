# ReciclaBot - Proyecto IA

**Autora:** Elsy Valeria Cuevas de la Torre  
**Registro:** 23310379  
**Proyecto:** Chatbot educativo para separar residuos

## Descripción

ReciclaBot es un chatbot hecho en Python que ayuda a identificar cómo separar residuos comunes como plástico, papel, cartón, vidrio, metal, orgánico, pilas, aceite usado y electrónicos.

El usuario escribe un residuo y el bot responde con una recomendación de separación.

## Tecnologías usadas

- Python
- Streamlit
- Scikit-learn
- Pandas
- Joblib

## Cómo correrlo

copia y pega esto en la terminal

cat > app.py <<'PY'
import streamlit as st
from asistente.motor import responder

st.set_page_config(
    page_title="ReciclaBot",
    page_icon="♻️",
    layout="centered"
)

st.title("♻️ ReciclaBot")
st.write("Chatbot educativo para clasificar residuos y dar recomendaciones de separación.")

st.markdown("""
Ejemplos que puedes probar:
- botella de plástico
- botella de vidrio
- caja de cartón
- aceite de cocina usado
- pila usada
- celular viejo
- medicamento caducado
- foco ahorrador
""")

if "historial" not in st.session_state:
    st.session_state.historial = []

mensaje = st.chat_input("Escribe aquí tu residuo...")

if mensaje:
    resultado = responder(mensaje)

    st.session_state.historial.append({
        "usuario": mensaje,
        "respuesta": resultado["respuesta"],
        "categoria": resultado["categoria"],
        "confianza": resultado["confianza"]
    })

for item in st.session_state.historial:
    with st.chat_message("user"):
        st.write(item["usuario"])

    with st.chat_message("assistant"):
        st.write(item["respuesta"])
        st.caption(f"Categoría detectada: {item['categoria']} | Confianza: {item['confianza']}")
PY

streamlit run app.py --server.address 0.0.0.0 --server.port 8501