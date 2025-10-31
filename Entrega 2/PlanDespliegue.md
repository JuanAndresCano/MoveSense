# Plan de despliegue

## Objetivo
Ejecución en tiempo real con cámara: inferencia de actividad + overlay de indicadores posturales.

## Arquitectura runtime
1) Captura (OpenCV) -> 2) Pose (MediaPipe) -> 3) Features en ventana deslizante (p.ej., 1–2 s) -> 4) Clasificador -> 5) Overlay (ángulos, inclinación, etiqueta) -> 6) Visualización/stream.

## Rendimiento esperado
- Target: >= 20 FPS en laptop estándar; latencia < 50 ms por frame para pose+clasificador (optimizable según hardware).

## Empaquetado
- Serialización: `model.joblib` y `scaler.joblib`.
- Requisitos: `requirements.txt` (opencv-python, mediapipe, numpy, pandas, scikit-learn, xgboost opcional).
- Script principal: `app/realtime_inference.py` (por crear en la siguiente fase).

## UI mínima
- Ventana con video + esqueletos + etiqueta + valores de ángulos/inclinación.
- Indicador de confianza y estabilidad (suavizado exponencial sobre logits/probabilidades opcional).

## Configuración
- YAML/JSON con: fuente de cámara, tamaño de ventana, umbral de confianza, rutas a artefactos.

## Observabilidad
- Logs de latencia y FPS; opción de grabar muestras problemáticas.

## Riesgos y mitigación
- Oclusiones/iluminación: fallback a predicción anterior y advertencia de baja confianza.
- Desbalance operacional: recalibración con datos nuevos y validación periódica.
