from pathlib import Path
import json
import random
import joblib

BASE_DIR = Path(__file__).resolve().parents[1]
MODEL_FILE = BASE_DIR / "modelo" / "reciclabot_modelo.joblib"
RESPONSES_FILE = BASE_DIR / "datos" / "respuestas.json"


def _cargar_respuestas():
    return json.loads(RESPONSES_FILE.read_text(encoding="utf-8"))


def _cargar_modelo():
    if not MODEL_FILE.exists():
        raise FileNotFoundError(
            "No se encontró el modelo. Ejecuta primero: python asistente/entrenar.py"
        )
    return joblib.load(MODEL_FILE)


RESPUESTAS = _cargar_respuestas()
MODELO = _cargar_modelo()


def responder(mensaje_usuario: str) -> dict:
    texto = (mensaje_usuario or "").strip()
    if not texto:
        return {"categoria": "fallback", "confianza": 0.0, "respuesta": random.choice(RESPUESTAS["fallback"])}

    categoria = MODELO.predict([texto])[0]
    confianza = 1.0

    if hasattr(MODELO.named_steps["clasificador"], "predict_proba"):
        probabilidades = MODELO.predict_proba([texto])[0]
        confianza = float(max(probabilidades))

    if confianza < 0.28:
        categoria = "fallback"

    respuesta = random.choice(RESPUESTAS.get(categoria, RESPUESTAS["fallback"]))
    return {"categoria": categoria, "confianza": round(confianza, 3), "respuesta": respuesta}
