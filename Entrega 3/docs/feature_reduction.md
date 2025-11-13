# Reducción de características

## Panorama de datos
- Fuente: `Entrega 2/landmarks_data.csv` con 13 035 registros y 132 features tabulares derivados de landmarks (x, y, z, visibilidad).
- Clases balanceadas respecto a Entrega 2: `adelante`, `atrás`, `girar`, `pararse`, `sentarse` (mínimo 170 muestras por clase).
- Split utilizado: 80/20 estratificado (`train_test_split`, `random_state=42`).

## Baseline reproducido
- Modelo: `RandomForestClassifier` (400 árboles, `class_weight='balanced'`).
- Resultado con las 132 variables originales: accuracy 0.982, macro F1 0.985.
- El reporte completo se exportó a `Entrega 3/artifacts/baseline_classification_report.csv`.

## Estrategias evaluadas

### 1. Importancia por RandomForest (filtering)
- Se calcularon importancias y se re-entrenó el bosque con los top K features (20–100).
- Comportamiento:
  - K=20 → accuracy 0.967, macro F1 0.973.
  - K=80 → accuracy 0.981, macro F1 0.984.
  - K=100 → accuracy 0.981, macro F1 0.984 (prácticamente idéntico al baseline).
- Top 10 atributos más relevantes: `31_x`, `25_x`, `27_x`, `26_z`, `29_x`, `19_v`, `21_v`, `17_v`, `0_z`, `32_y`.
- Conclusión: el modelo mantiene desempeño >0.98 con ≈60–100 features, pero no supera el baseline.

### 2. Selección univariada (`SelectKBest`)
- Score functions: ANOVA F y Mutual Information, con un SVM RBF posterior.
- Métricas claves:
  - ANOVA K=100 → accuracy 0.979, macro F1 0.982.
  - Mutual Info K=100 → accuracy 0.979, macro F1 0.983.
  - K≤60 degrada apreciablemente (accuracy ≤0.934).
- Guardados en `artifacts/anova_results.csv` y `artifacts/mutual_info_results.csv`.
- Conclusión: no logra mejoras significativas frente al baseline y requiere ≥100 features para rendimiento alto.

### 3. PCA + SVM RBF
- Pipeline: imputación→estandarización→PCA→SVM.
- Resultados:
  - 40 componentes → accuracy 0.984, macro F1 0.983 (ya supera el baseline).
  - 60 componentes → accuracy 0.988, macro F1 0.990 con 99.96 % de varianza (mejor configuración).
  - 80–100 componentes mantienen ~0.988 sin beneficios adicionales.
- Variancia acumulada: 90 % con ~10 componentes, 99 % con 40.
- Métricas guardadas en `artifacts/pca_results.csv`.

- Figura: desempeño de PCA (accuracy y macro F1) vs. número de componentes (ver `artifacts/pca_performance.png`).

## Decisión
- Adoptaremos PCA con 60 componentes para los siguientes experimentos: ofrece la mejor métrica global (+0.5 pp accuracy vs. baseline) con una reducción efectiva del 55 % en dimensionalidad.
- Como respaldo interpretable, preservamos el ranking de importancias de RandomForest (para análisis de contribución y posibles versiones light ~60 features crudos).

