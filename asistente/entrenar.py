from pathlib import Path
import json
import joblib
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_FILE = BASE_DIR / "datos" / "ejemplos.csv"
MODEL_DIR = BASE_DIR / "modelo"
MODEL_FILE = MODEL_DIR / "reciclabot_modelo.joblib"
REPORT_FILE = MODEL_DIR / "reporte_entrenamiento.json"


def cargar_datos():
    tabla = pd.read_csv(DATA_FILE)
    textos = tabla["texto"].astype(str).tolist()
    etiquetas = tabla["categoria"].astype(str).tolist()
    return textos, etiquetas, tabla


def crear_modelo():
    return Pipeline([
        ("conteo_palabras", CountVectorizer(lowercase=True, ngram_range=(1, 2))),
        ("clasificador", MultinomialNB(alpha=0.7))
    ])


def main():
    textos, etiquetas, tabla = cargar_datos()
    modelo = crear_modelo()
    modelo.fit(textos, etiquetas)

    predicciones = modelo.predict(textos)
    precision = accuracy_score(etiquetas, predicciones)

    MODEL_DIR.mkdir(exist_ok=True)
    joblib.dump(modelo, MODEL_FILE)

    resumen = {
        "ejemplos_entrenamiento": len(tabla),
        "categorias": sorted(tabla["categoria"].unique().tolist()),
        "precision_sobre_dataset": round(float(precision), 4),
        "archivo_modelo": str(MODEL_FILE.name),
        "nota": "La precision reportada es sobre el dataset educativo usado para entrenar."
    }
    REPORT_FILE.write_text(json.dumps(resumen, indent=2, ensure_ascii=False), encoding="utf-8")
    print("Modelo entrenado correctamente.")
    print(f"Ejemplos usados: {resumen['ejemplos_entrenamiento']}")
    print(f"Categorías: {', '.join(resumen['categorias'])}")
    print(f"Modelo guardado en: {MODEL_FILE}")


if __name__ == "__main__":
    main()
