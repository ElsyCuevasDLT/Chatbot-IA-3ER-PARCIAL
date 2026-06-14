from pathlib import Path
import pandas as pd
import joblib
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_FILE = BASE_DIR / "datos" / "ejemplos.csv"
MODEL_DIR = BASE_DIR / "modelo"
MODEL_FILE = MODEL_DIR / "reciclabot_modelo.joblib"

MODEL_DIR.mkdir(exist_ok=True)

df = pd.read_csv(DATA_FILE)

x = df["texto"].astype(str)
y = df["categoria"].astype(str)

modelo = Pipeline([
    ("vectorizador", CountVectorizer(
        lowercase=True,
        strip_accents="unicode",
        ngram_range=(1, 3)
    )),
    ("clasificador", MultinomialNB(alpha=0.25))
])

modelo.fit(x, y)

pred = modelo.predict(x)
print(classification_report(y, pred, zero_division=0))

joblib.dump(modelo, MODEL_FILE)
print(f"Modelo guardado en: {MODEL_FILE}")
