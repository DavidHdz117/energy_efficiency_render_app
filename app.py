from pathlib import Path
import math

import joblib
import pandas as pd
from flask import Flask, render_template, request


BASE_DIR = Path(__file__).resolve().parent
PIPELINE_PATH = BASE_DIR / "pipeline_energy_efficiency.joblib"

COLUMNAS_ENTRADA = [
    "compacidad_relativa",
    "area_superficial",
    "area_muros",
    "area_techo",
    "altura_total",
    "orientacion",
    "area_ventanas",
    "distribucion_ventanas",
]

VALORES_PREDETERMINADOS = {
    "compacidad_relativa": "0.98",
    "area_superficial": "514.5",
    "area_muros": "294.0",
    "area_techo": "110.25",
    "altura_total": "7.0",
    "orientacion": "2",
    "area_ventanas": "0.10",
    "distribucion_ventanas": "1",
}

CAMPOS_FORMULARIO = [
    {
        "nombre": "compacidad_relativa",
        "etiqueta": "Compacidad relativa",
        "ayuda": "Valor de referencia del dataset: 0.62 a 0.98",
        "paso": "any",
    },
    {
        "nombre": "area_superficial",
        "etiqueta": "Área superficial",
        "ayuda": "Área total de la superficie del edificio, en m²",
        "paso": "any",
    },
    {
        "nombre": "area_muros",
        "etiqueta": "Área de muros",
        "ayuda": "Área total de los muros, en m²",
        "paso": "any",
    },
    {
        "nombre": "area_techo",
        "etiqueta": "Área del techo",
        "ayuda": "Área total del techo, en m²",
        "paso": "any",
    },
    {
        "nombre": "altura_total",
        "etiqueta": "Altura total",
        "ayuda": "Altura total del edificio, en metros",
        "paso": "any",
    },
    {
        "nombre": "orientacion",
        "etiqueta": "Orientación",
        "ayuda": "Código original del dataset: 2, 3, 4 o 5",
        "paso": "1",
    },
    {
        "nombre": "area_ventanas",
        "etiqueta": "Área de ventanas",
        "ayuda": "Proporción de área acristalada: 0.00 a 0.40",
        "paso": "any",
    },
    {
        "nombre": "distribucion_ventanas",
        "etiqueta": "Distribución de ventanas",
        "ayuda": "Código original del dataset: 0 a 5",
        "paso": "1",
    },
]

if not PIPELINE_PATH.exists():
    raise FileNotFoundError(
        "No se encontró pipeline_energy_efficiency.joblib. "
        "Ejecuta la última sección de la libreta para generarlo y colócalo "
        "en la misma carpeta que app.py."
    )

pipeline = joblib.load(PIPELINE_PATH)
app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    valores = VALORES_PREDETERMINADOS.copy()
    resultado = None
    error = None

    if request.method == "POST":
        valores = {
            columna: request.form.get(columna, "").strip()
            for columna in COLUMNAS_ENTRADA
        }

        if any(valor == "" for valor in valores.values()):
            error = "Completa todos los campos antes de generar la predicción."
        else:
            try:
                valores_numericos = {
                    columna: float(valores[columna])
                    for columna in COLUMNAS_ENTRADA
                }

                if not all(
                    math.isfinite(valor) for valor in valores_numericos.values()
                ):
                    raise ValueError
            except ValueError:
                error = (
                    "Todos los campos deben contener números válidos. "
                    "Usa punto para los valores decimales."
                )
            else:
                entrada = pd.DataFrame(
                    [[valores_numericos[columna] for columna in COLUMNAS_ENTRADA]],
                    columns=COLUMNAS_ENTRADA,
                )

                try:
                    prediccion = float(pipeline.predict(entrada)[0])
                    if not math.isfinite(prediccion):
                        raise ValueError("El pipeline devolvió un valor no válido.")
                    resultado = f"{prediccion:.2f}"
                except Exception:
                    app.logger.exception("Error al generar la predicción")
                    error = (
                        "No fue posible generar la predicción. "
                        "Revisa los valores e inténtalo nuevamente."
                    )

    return render_template(
        "index.html",
        campos=CAMPOS_FORMULARIO,
        valores=valores,
        resultado=resultado,
        error=error,
    )


if __name__ == "__main__":
    app.run(debug=True)
