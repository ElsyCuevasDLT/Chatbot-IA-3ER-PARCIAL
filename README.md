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

Entrar a la carpeta del proyecto:

```bash
cd /workspaces/PROYECTO-IA/ReciclaBot_ProyIA_23310379
```

Instalar dependencias:

```bash
pip install -r requirements.txt
```

Entrenar el modelo:

```bash
python asistente/entrenar.py
```

Ejecutar la aplicación:

```bash
streamlit run app.py
```

En GitHub Codespaces, abrir el puerto **8501** desde la pestaña **PUERTOS**.

## Forma rápida

Si el modelo ya fue entrenado:

```bash
cd /workspaces/PROYECTO-IA/ReciclaBot_ProyIA_23310379
streamlit run app.py
```

## Ejemplos

```text
botella de plastico
caja de carton
pila usada
celular viejo
aceite de cocina usado
vidrio roto
lata de aluminio
```