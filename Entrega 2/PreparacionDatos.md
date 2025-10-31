# Preparación de datos

## Pipeline (alto nivel)
1) Extracción de pose (MediaPipe) por frame -> landmarks normalizados por tamaño de torso y centrados en cadera media.
2) Suavizado temporal (Savitzky-Golay) para robustez a ruido.
3) Ingeniería de características:
   - Ángulos: rodillas, caderas; inclinación del tronco.
   - Velocidades: muñecas, rodillas, tobillos.
   - Simetrías izquierda/derecha; magnitudes y derivados simples.
4) Alineación con anotaciones (CSV por intervalos o frame) -> columna `label`.
5) Splits: train/valid/test por sujeto (evitar fuga de identidad).
6) Estandarización (fit en train, aplicar a valid/test). Guardar `features.csv`/parquet.

## Tratamiento de casos especiales
- Landmarks ausentes/oclusiones: interpolación temporal corta; descartar tramos muy largos.
- Duraciones variables: recorte/padding solo si se requiere por modelo; preferir agregaciones por ventana para modelos tabulares.
- Desbalance: muestreo estratificado por clase; ponderación en entrenamiento.

## Aumentación (sobre características, opcional)
- Time-warping suave, jitter leve, flips izquierda<->derecha cuando semánticamente válido.

## Estructura de artefactos
- `Exports/features_v1.parquet` (train/valid/test etiquetados).
- `Exports/scaler.joblib` (si se usa estandarización).

## Validación de calidad
- % de frames con pose válida, % de muestras por clase/sujeto, revisión manual de series y ángulos.
