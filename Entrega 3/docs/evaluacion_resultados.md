# Evaluación de resultados — Entrega 3

## Configuración
- Dataset: `Entrega 2/landmarks_data.csv` (13 035 filas, 132 features).
- Validación: `StratifiedKFold` con 5 folds, semillas fijas (`random_state=42`).
- Modelos comparados:
  1. `RandomForestClassifier` baseline (132 features original, 400 árboles, `class_weight='balanced'`).
  2. Pipeline `Imputer → StandardScaler → PCA(60) → SVM RBF (C=10, γ=0.01, class_weight='balanced')`.
- Cuaderno de referencia: `Entrega 3/notebooks/evaluation.ipynb`.
- Artefactos: `Entrega 3/artifacts/evaluacion/`.

## Resultados de cross-validation (5 folds)

| Modelo | Accuracy (media ± std) | Macro F1 (media ± std) |
| --- | --- | --- |
| RandomForest (132f) | 0.9895 ± 0.0015 | 0.9913 ± 0.0014 |
| PCA(60) + SVM | 0.9881 ± 0.0020 | 0.9892 ± 0.0021 |

- Al promediar los folds, el RandomForest completo aún supera marginalmente al pipeline PCA+SVM (≈0.14 pp en macro F1). No obstante, la brecha es pequeña y las desviaciones estándar se solapan.
- Reportes por clase:
  - `cv_rf_report.csv`: F1 ≥ 0.98 en todas las clases; `sentarse` y `pararse` alcanzan ≈0.997.
  - `cv_pca60_report.csv`: F1 ≥ 0.98 salvo `girar` (0.981) y ligera caída en `pararse` (0.993).
  - Frentes de mejora: la reducción con PCA penaliza levemente `pararse` y `girar`; conviene revisar hiperparámetros del SVM o entrenar un clasificador adicional sobre las componentes PCA.

## Matrices de confusión agregadas
- `artifacts/evaluacion/cv_rf_confusion.png` y `cv_rf_confusion_normalized.png`: el RF mantiene un conteo mínimo de errores, con confusiones residuales entre `girar` y `adelante`.
- `artifacts/evaluacion/cv_pca_confusion.png` y versión normalizada: los errores aumentan ligeramente en `girar`, confirmando lo observado en las métricas.

## Latencia de inferencia (200 muestras)

| Pipeline | Tiempo medio por batch (s) | std | Tiempo por muestra (ms) |
| --- | --- | --- | --- |
| RandomForest (132f) | 0.1412 | 0.0076 | 0.71 |
| PCA(60) + SVM | 0.0782 | 0.0067 | 0.39 |

- Los tiempos provienen de `latency_report.json`. Ambos pipelines fueron ajustados sobre el dataset completo antes de medir.
- El pipeline PCA+SVM reduce aprox. 45 % la latencia frente al RF (0.39 ms vs. 0.71 ms por muestra en el entorno de prueba). Esta ganancia respalda el uso de PCA para despliegue en tiempo real.

## Conclusiones
- Validación cruzada confirma que ambos enfoques generalizan bien (accuracy ≈0.99). El RF original sigue siendo el más preciso, pero la versión PCA+SVM ofrece desempeño cercano con menor latencia.
- Recomendación operacional: mantener dos variantes
  - **Alta precisión**: RandomForest 132 features (para análisis offline o cuando no hay restricciones de tiempo).
  - **Tiempo real**: PCA(60) + SVM (balance desempeño/latencia, menor tamaño de feature vector).
