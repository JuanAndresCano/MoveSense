# MoveSense — Reporte Final

## Abstract
MoveSense desarrolla un sistema para reconocer cinco actividades humanas básicas y estimar ángulos articulares en tiempo real a partir de landmarks de pose. En esta entrega final se optimizaron las características mediante PCA, se evaluaron los modelos con validación cruzada, se construyó un prototipo de despliegue y se analizó el impacto contextual. El RandomForest baseline alcanza accuracy 0.989 y macro F1 0.991, mientras que el pipeline PCA(60)+SVM logra 0.988/0.989 con una latencia 45 % menor. Además, se documentan riesgos éticos, recomendaciones y un plan de entrega para el “cliente”.

## 1. Introducción
- **Problema**: asistir el análisis postural y la clasificación de actividades básicas (caminar adelante/atrás, girar, sentarse, pararse) mediante visión por computador.
- **Motivación**: ofrecer retroalimentación rápida y cuantitativa en entornos educativos o de entrenamiento, sin requerir sensores intrusivos.
- **Objetivos**: (i) construir dataset propio con landmarks de MediaPipe, (ii) evaluar modelos supervisados, (iii) reducir dimensionalidad para mejorar latencia, (iv) desplegar un prototipo en tiempo real y (v) documentar impacto ético.

## 2. Marco teórico
- **Estimación de pose**: MediaPipe Pose (landmarks 2.5D, x/y/z/visibilidad). Referencias a trabajos de Google, OpenPose y aplicaciones en análisis de movimiento.
- **Clasificación de actividades**: modelos supervisados tabulares (RandomForest, SVM, XGBoost). Resumen de métricas (accuracy, F1, macro F1) y validación por sujeto/cuasi-sujeto.
- **Reducción de características**: técnicas filter (importancias RF), wrapper (SelectKBest) y PCA. Discusión breve sobre ventajas y compromisos.

## 3. Metodología
- **Metodología CRISP-DM adaptada**: fases de entendimiento, adquisición, preparación, modelado, evaluación y despliegue.
- **Datasets**: videos propios (carpeta `Videos_IA`), extracción de landmarks → `landmarks_data.csv`. Referencia a datasets públicos considerados (Entrega 1/Docs/DataSets.md).
- **Preparación de datos**: imputación de landmarks, normalización, cálculo de características auxiliares (ángulos, velocidades). Notebook `feature_reduction.ipynb`.
- **Modelado**:
  - Baseline tabular con RandomForest, SVM y Regresión Logística.
  - Reducción de características (RF importances, SelectKBest, PCA) y selección final de PCA(60).
- **Evaluación**: `evaluation.ipynb` con `StratifiedKFold` (k=5), tablas de métricas y matrices de confusión.
- **Despliegue**: scripts `export_artifacts.py` y `realtime_app.py`, interfaz OpenCV.

## 4. Resultados
- **Comparación principal (tabla)**:

  | Modelo | Accuracy | Macro F1 | Latencia (ms/muestra) |
  | --- | --- | --- | --- |
  | RandomForest 132 features | 0.9895 ± 0.0015 | 0.9913 ± 0.0014 | 0.71 |
  | PCA(60) + SVM | 0.9881 ± 0.0020 | 0.9892 ± 0.0021 | 0.39 |

- **Curvas y figuras**:
  - `artifacts/pca_performance.png`: impacto de # componentes en desempeño.
  - Matrices de confusión agregadas (`artifacts/evaluacion/...`).
- **Análisis por clase**: F1 ≥ 0.98 en todas las clases; `girar` y `pararse` presentan la brecha más notable en la variante PCA.
- **Despliegue**: demo OpenCV funcional con ángulos (rodillas, codos, tronco), FPS y suavizado de etiquetas.

## 5. Análisis de resultados
- **Interpretación**: PCA reduce 55 % las features sin comprometer significativamente la precisión, permite latencias menores y favorece el despliegue.
- **Comparación con literatura**: referencia a estudios con MediaPipe/OpenPose que reportan métricas similares para acciones básicas (indicando que MoveSense alcanza resultados competitivos con dataset reducido).
- **Limitaciones**: diversidad limitada de sujetos, dependencia de condiciones de iluminación y precisión de MediaPipe. Requiere calibrar umbrales de confianza y mejorar robustez ante oclusiones.
- **Validación**: discutir cómo el split estratificado puede sobreestimar generalización si los sujetos se repiten; sugerencia de futura evaluación leave-one-subject-out.

## 6. Conclusiones y trabajo futuro
- **Logros**: dataset propio procesado, pipelines reproducibles, reducción de características efectiva, demo en tiempo real, análisis ético documentado.
- **Trabajo futuro**:
  - Aumentar diversidad del dataset (más sujetos, ángulos de cámara, ropa, iluminación).
  - Ajustar hiperparámetros de SVM y evaluar XGBoost sobre PCA.
  - Integrar detección de confianza baja en UI y registro de sesiones.
  - Preparar versión empaquetada (PyInstaller/contenerizada) y pruebas en hardware objetivo.
  - Extender métricas a análisis temporal (duración de transiciones, estabilidad postural).

## 7. Impacto contextual
Resumen de `docs/impacto_final.md`: beneficios, riesgos, mitigaciones y recomendaciones. Destacar protocolos de consentimiento, transparencia y plan de monitoreo.

## Referencias
- [1] Google Research, MediaPipe Pose Documentation, 2024.
- [2] C. Cao et al., "OpenPose: Realtime Multi-Person 2D Pose Estimation", CVPR, 2017.
- [3] A. S. Morse et al., "Human Activity Recognition Using Landmarks", Sensors, 2022.
- [4] Documentos internos del proyecto (Entrega 1/Docs/DataSets.md, Entrega 2/ModeladoYEntrenamiento.md, etc.).
