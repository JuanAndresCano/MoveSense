# MoveSense — Despliegue en tiempo real

Este módulo contiene los artefactos y scripts necesarios para ejecutar la demo en tiempo real con cámara web.

## Contenido

- `export_artifacts.py`: ajusta los modelos sobre `Entrega 2/landmarks_data.csv` y exporta los pipelines (`activity_pca60_svm.joblib`, `activity_rf.joblib`), el `LabelEncoder` y la lista de features.
- `realtime_app.py`: aplicación GUI (OpenCV) que captura video, ejecuta la clasificación de actividad y muestra ángulos articulares.
- `requirements.txt`: dependencias para montar el entorno de despliegue.
- `models/`: carpeta que se crea al ejecutar `export_artifacts.py`.

## Instalación de dependencias

```bash
cd "Entrega 3/deployment"
pip install -r requirements.txt
```

## Generar artefactos

1. Verifica que `Entrega 2/landmarks_data.csv` exista en la ruta indicada.
2. Ejecuta:
   ```bash
   python export_artifacts.py
   ```
3. Se generará `models/` con:
   - `activity_pca60_svm.joblib`
   - `activity_rf.joblib`
   - `label_encoder.joblib`
   - `feature_names.json`
   - `metadata.json`

## Ejecutar demo en tiempo real

```bash
python realtime_app.py --models-dir models --camera-index 0
```

Si ejecutas el script desde la raíz del proyecto, usa `--models-dir "Entrega 3/deployment/models"`.

Opciones útiles:
- `--camera-index`: índice de cámara (default 0).
- `--confidence-history`: tamaño de la ventana de suavizado de etiquetas (default 8).

La interfaz muestra:
- Actividad predicha (suavizada)
- Confianza aproximada
- FPS estimado
- Ángulos principales: rodillas, codos e inclinación del tronco

## Mantenimiento
- Para actualizar los modelos tras recolectar nuevos datos, vuelve a ejecutar `export_artifacts.py`.
- Los artefactos `.joblib` y archivos JSON deben viajar junto con `realtime_app.py` cuando implementes la demo en otro equipo.
