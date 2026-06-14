from pathlib import Path
import json
import random
import joblib
import unicodedata

BASE_DIR = Path(__file__).resolve().parents[1]
MODEL_FILE = BASE_DIR / "modelo" / "reciclabot_modelo.joblib"
RESPONSES_FILE = BASE_DIR / "datos" / "respuestas.json"


def normalizar(texto: str) -> str:
    texto = texto.lower().strip()
    texto = unicodedata.normalize("NFD", texto)
    texto = "".join(letra for letra in texto if unicodedata.category(letra) != "Mn")
    return texto


def cargar_respuestas():
    return json.loads(RESPONSES_FILE.read_text(encoding="utf-8"))


def cargar_modelo():
    if not MODEL_FILE.exists():
        raise FileNotFoundError("Primero entrena el modelo con: python asistente/entrenar.py")
    return joblib.load(MODEL_FILE)


RESPUESTAS = cargar_respuestas()
MODELO = cargar_modelo()


def clasificar_por_reglas(texto: str):
    t = normalizar(texto)

    reglas = [
        ("aceite", ["aceite", "grasa liquida", "freir", "fritura"]),
        ("pilas_baterias", ["pila", "pilas", "bateria", "baterias", "power bank"]),
        ("medicamento", ["medicina", "medicamento", "pastilla", "jarabe", "antibiotico", "caducado"]),
        ("electronico", ["celular", "telefono", "cargador", "cable usb", "audifono", "teclado", "mouse", "control remoto", "electronico", "tarjeta electronica", "laptop", "tablet"]),
        ("peligroso", ["tubo fluorescente", "foco ahorrador", "pintura", "solvente", "aerosol", "insecticida", "veneno", "quimico"]),
        ("sanitario", ["panal", "toalla sanitaria", "papel higienico", "cubrebocas", "guantes", "jeringa", "curita", "servilleta sucia"]),
        ("tetra_pak", ["tetra pak", "tetrapak", "caja de leche", "envase de leche", "envase de jugo", "carton de leche"]),
        ("vidrio", ["botella de vidrio", "frasco de vidrio", "vaso de vidrio", "vidrio", "cristal", "tarro de vidrio", "botella de vino", "botella de cerveza"]),
        ("plastico", ["botella de plastico", "plastico", "plastica", "pet", "bolsa", "envase de shampoo", "envase de detergente", "garrafon", "tapa de plastico", "vaso de plastico"]),
        ("papel_carton", ["papel", "carton", "hoja", "libreta", "cuaderno", "periodico", "revista", "caja", "folder", "cartulina"]),
        ("metal", ["lata", "aluminio", "metal", "cobre", "clavo", "tornillo", "chatarra", "fierro", "alambre"]),
        ("organico", ["comida", "cascara", "platano", "huevo", "cafe", "fruta", "verdura", "hueso", "pan duro", "bolsa de te"]),
        ("textil", ["ropa", "camisa", "pantalon", "zapato", "tela", "trapo", "calcetin"]),
        ("no_reciclable", ["unicel", "envoltura de papas", "bolsa metalizada", "chicle", "colilla", "ceramica", "espejo"])
    ]

    for categoria, palabras in reglas:
        for palabra in palabras:
            if palabra in t:
                return categoria

    return None


def responder(mensaje_usuario: str) -> dict:
    texto = (mensaje_usuario or "").strip()

    if not texto:
        return {
            "categoria": "fallback",
            "confianza": 0.0,
            "respuesta": random.choice(RESPUESTAS["fallback"])
        }

    categoria_regla = clasificar_por_reglas(texto)

    if categoria_regla:
        return {
            "categoria": categoria_regla,
            "confianza": 1.0,
            "respuesta": random.choice(RESPUESTAS[categoria_regla])
        }

    categoria = MODELO.predict([texto])[0]
    confianza = 1.0

    clasificador = MODELO.named_steps["clasificador"]
    if hasattr(clasificador, "predict_proba"):
        probabilidades = MODELO.predict_proba([texto])[0]
        confianza = float(max(probabilidades))

    if confianza < 0.45:
        categoria = "fallback"

    return {
        "categoria": categoria,
        "confianza": round(confianza, 3),
        "respuesta": random.choice(RESPUESTAS.get(categoria, RESPUESTAS["fallback"]))
    }
