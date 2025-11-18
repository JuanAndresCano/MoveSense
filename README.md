# MoveSense

[Video Entrega 3](https://youtu.be/QlplxCFysmI?si=SNXwyeDAkLsK0a-1)

## Project Overview

MoveSense es un sistema de reconocimiento de actividades humanas que opera en tiempo real y calcula ángulos articulares clave usando MediaPipe Pose. El proyecto culmina en la Entrega 3 con un demo en vivo y artefactos reproducibles.

## Project Status

Entrega 3 completada (demo funcional y documentación consolidada).

## Contributing Members

- Juan Andrés Cano Ramírez — https://github.com/JuanAndresCano
- Pablo Guzmán Alarcón — https://github.com/Pableis05

## Core Components

- Dataset tabular con 132 `landmarks` procesados (`Entrega 2/landmarks_data.csv`).
- Paquete de inferencia en `Entrega 3/deployment/` con pipelines exportados (`activity_rf.joblib`, `activity_pca60_svm.joblib`).
- Documentación técnica en `Entrega 3/docs/` (evaluación de resultados, reducción de características, despliegue, impacto).
- Videos de funcionalidades en `Entrega 3/videosFuncionalidades/`.

## Methods & Models

- Extracción de landmarks con MediaPipe Pose y normalización de coordenadas.
- Baseline: `RandomForestClassifier` (132 features, `class_weight='balanced'`).
- Pipeline final: `Imputer → StandardScaler → PCA(60) → SVM RBF` optimizado con `StratifiedKFold` (5 folds).
- Experimentos adicionales de reducción: importancias de RandomForest, `SelectKBest`, análisis de varianza explicada de PCA.
- Métricas monitorizadas: accuracy, macro F1, matrices de confusión agregadas, latencia por muestra.

## Tech Stack

- Python 3.10
- scikit-learn, pandas, numpy, joblib
- MediaPipe, OpenCV (captura y overlay en tiempo real)
- matplotlib, seaborn (visualización)

## Reproducir Experimentos

- Notebooks principales en `Entrega 3/notebooks/` (`evaluation.ipynb`, `feature_reduction.ipynb`).
- Artefactos de métricas y reportes en `Entrega 3/artifacts/`.
- Para repetir la exportación de modelos:
  - `python "Entrega 3/deployment/export_artifacts.py"`
- Para ejecutar el demo en vivo:
  - `pip install -r "Entrega 3/deployment/requirements.txt"`
  - `python "Entrega 3/deployment/realtime_app.py" --models-dir "Entrega 3/deployment/models" --camera-index 0`

## Documentation Highlights

- `Entrega 3/docs/evaluacion_resultados.md`: compara RandomForest vs. PCA+SVM (metricas y latencia).
- `Entrega 3/docs/feature_reduction.md`: resume estrategias de selección de características.
- `Entrega 3/docs/despliegue.md`: guía paso a paso del demo y dependencias.
- `Entrega 3/docs/impacto_final.md`: impactos y consideraciones éticas de la solución.

