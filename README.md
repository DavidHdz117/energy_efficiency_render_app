# Predicción de carga de calefacción

Aplicación web desarrollada con Flask para estimar la carga de calefacción de
un edificio a partir de ocho características físicas originales.

## Proyecto

- **Dataset:** Energy Efficiency.
- **Variable objetivo:** `carga_calefaccion`.
- **Pipeline:** `pipeline_energy_efficiency.joblib`.
- **Entradas:** las ocho columnas originales del dataset, sin
  `carga_enfriamiento`.

El pipeline ya incluye el preprocesamiento, PCA y el modelo ganador. La
aplicación no entrena ningún modelo: únicamente carga el archivo guardado y lo
usa para generar predicciones.

## Ejecutar localmente

Abre una terminal dentro de esta carpeta y ejecuta:

```bash
python -m venv .venv
```

En Windows, activa el entorno:

```powershell
.\.venv\Scripts\Activate.ps1
```

Instala las dependencias:

```bash
pip install -r requirements.txt
```

Inicia la aplicación:

```bash
python app.py
```

Después abre `http://127.0.0.1:5000` en el navegador.

## Desplegar en Render

1. Sube esta carpeta a un repositorio de GitHub.
2. En Render crea un servicio **Web Service** y conecta el repositorio.
3. Configura los siguientes comandos:

   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`

4. Inicia el despliegue.

Si esta carpeta se encuentra dentro de un repositorio más grande, establece
`energy_efficiency_render_app` como **Root Directory** en Render.

## URL pública

Cuando Render termine el despliegue, copia la URL pública del servicio, pégala
en `URL_Render.txt` reemplazando el texto de ejemplo y guarda el archivo.

El archivo `pipeline_energy_efficiency.joblib` debe permanecer en la misma
carpeta que `app.py`. Si falta, ejecuta la última sección de la libreta para
generarlo antes de desplegar.
