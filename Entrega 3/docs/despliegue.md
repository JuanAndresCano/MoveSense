# Despliegue en tiempo real — MoveSense

## Objetivo
Implementar una interfaz sencilla (OpenCV) que muestre en tiempo real la actividad reconocida y ángulos articulares clave usando los modelos generados en la Entrega 3.

## Artefactos y estructura
- `Entrega 3/deployment/export_artifacts.py`: genera los pipelines y artefactos necesarios (`models/`).
- `Entrega 3/deployment/realtime_app.py`: aplicación principal de inferencia.
- `Entrega 3/deployment/README.md`: instrucciones detalladas para instalación y ejecución.
- `Entrega 3/deployment/models/` (generado):
  - `activity_pca60_svm.joblib`
  - `activity_rf.joblib`
  - `label_encoder.joblib`
  - `feature_names.json`
  - `metadata.json`

## Flujo del demo
1. Captura frames de cámara (`cv2.VideoCapture`).
2. Estima landmarks corporales con MediaPipe Pose.
3. Construye el vector de 132 features (x, y, z, visibility) alineado con el dataset.
4. Ejecuta el pipeline PCA(60)+SVM (suaviza etiquetas con ventana configurable).
5. Calcula ángulos de rodillas, codos e inclinación del tronco.
6. Dibuja landmarks + overlay con actividad, confianza, FPS y ángulos.

## Requisitos de ejecución
- Python ≥ 3.10
- Instalar dependencias con `pip install -r "Entrega 3/deployment/requirements.txt"`.
- Cámara accesible desde el sistema.

## Uso básico
```bash
# 1. Generar artefactos
python Entrega 3/deployment/export_artifacts.py

# 2. Ejecutar demo
python Entrega 3/deployment/realtime_app.py --models-dir "Entrega 3/deployment/models" --camera-index 0
```

Opciones:
- `--models-dir`: ruta al directorio de modelos (`models/`).
- `--camera-index`: índice de la cámara (default 0).
- `--confidence-history`: tamaño de ventana para suavizado de etiquetas.

Si ejecutas el script desde `Entrega 3/deployment`, utiliza `python realtime_app.py --models-dir models --camera-index 0`.


