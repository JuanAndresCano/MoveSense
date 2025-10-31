# Modelado y entrenamiento

## Objetivo
Clasificar 5 actividades usando características derivadas de landmarks y evaluar analítica postural asociada.

## Conjuntos y validación
- División por sujeto (GroupKFold o LOSO) para evitar fuga de identidad.
- Train/Valid para tuning; Test final separado.

## Conjunto de características (base)
- Ángulos: `left_knee_deg`, `right_knee_deg`, `left_hip_deg`, `right_hip_deg`, `trunk_incl_deg`.
- Velocidades: `*_wrist_speed`, `*_knee_speed`, `*_ankle_speed`.
- Opcional: estadísticas por ventana (media, std, p95, IQR) y deltas.

## Modelos candidatos
- SVM (RBF): buena frontera no lineal en tabular de tamaño moderado.
- Random Forest: robusto, interpretable (importancias), poco tuning.
- XGBoost: fuerte en tabular, admite desbalance y early stopping.

## Preprocesamiento por modelo
- SVM: estandarización obligatoria.
- RF/XGB: estandarización opcional.
- Manejo de clase minoritaria: `class_weight=balanced` (SVM/RF) o `scale_pos_weight` (XGB) si aplica.

## Búsqueda de hiperparámetros (sugerida)
- SVM (RBF): `C` en {0.1, 1, 10, 100}, `gamma` en {1e-3, 1e-2, 1e-1, 1}.
- RandomForest: `n_estimators` {200, 400, 800}, `max_depth` {None, 10, 20}, `min_samples_leaf` {1, 2, 4}.
- XGBoost: `n_estimators` {300, 600, 900}, `max_depth` {3, 5, 7}, `learning_rate` {0.03, 0.1}, `subsample` {0.7, 1.0}, `colsample_bytree` {0.7, 1.0}. Early stopping con `eval_set`.

## Métricas
- Principales: accuracy, macro F1, matriz de confusión; F1 por clase.
- Robustez: varianza por sujeto y condición; tasa de frames con pose válida.
- Tiempo real: latencia media por frame y FPS en pipeline final.

## Reproducibilidad
- Fijar semillas, registrar versiones, guardar `scaler.joblib` y `model.joblib`.

## Entregables (Colabs a crear luego)
- `train_baselines.ipynb`: baseline SVM/RF, validación por sujeto, métricas.
- `tune_xgboost.ipynb`: tuning/early stopping y comparación contra baseline.
- `eval_test.ipynb`: evaluación final en test y curvas/figuras.
