# Entrega 1 — MoveSense

## 1. Preguntas de interés
- ¿Podemos clasificar en tiempo real las actividades: caminar hacia la cámara, caminar de regreso, girar, sentarse y ponerse de pie?
- ¿Qué características derivadas de los landmarks (ángulos, velocidades, inclinación del tronco) discriminan mejor entre actividades?
- ¿Qué latencia y tasa de acierto puede alcanzar el sistema en ejecución en tiempo real en un equipo estándar?
- ¿Cómo varía el desempeño entre personas, alturas, indumentaria, iluminación y perspectivas?

## 2. Tipo de problema
- Clasificación supervisada multiclase de actividades humanas a partir de series temporales de keypoints/landmarks de pose.
- Analítica postural complementaria (estimación/seguimiento de ángulos articulares e inclinación del tronco) como tarea de regresión/medición auxiliar.
- Modalidad: visión por computador con extracción de pose (MediaPipe/OpenPose) y modelado clásico (SVM/Random Forest/XGBoost) sobre características tabulares.

## 3. Metodología (CRISP-DM adaptada)
1) Entendimiento del negocio/contexto: Asistencia para análisis postural y reconocimiento de actividades básicas en video/tiempo real.
2) Entendimiento de datos: Videos propios y datasets públicos con anotaciones de pose y/o etiquetas de actividad. Ver `Entrega 1/DataSets.md`.
3) Preparación de datos: extracción de landmarks (MediaPipe), normalización, filtrado/suavizado temporal, ingeniería de características (ángulos, velocidades, inclinación, simetrías izquierda/derecha), alineación con etiquetas.
4) Modelado: evaluación de varios clasificadores supervisados (SVM, Random Forest, XGBoost). Búsqueda de hiperparámetros (Grid/Random Search). Validación por sujeto (leave-one-subject-out) cuando sea posible.
5) Evaluación: métricas por clase y globales (accuracy, macro F1, matriz de confusión), latencia y estabilidad temporal de predicción.
6) Despliegue (borrador): servicio local con cámara, visualización de esqueletos, etiqueta de actividad e indicadores posturales en overlay.

## 4. Métricas de progreso
- Clasificación: accuracy, precisión, recall, F1-Score macro y por clase; matriz de confusión; balanced accuracy (por posibles desbalances).
- Tiempo real: latencia media por frame (ms), FPS efectivo del pipeline.
- Analítica postural: MAE de ángulos clave (si hay ground-truth), varianza/estabilidad del estimador.
- Robustez: desempeño por persona/condición (iluminación, vista frontal/lateral), tasa de frames con pose válida.

## 5. Datos recolectados y fuentes
- Propios: Se capturarán videos cortos por cada integrante realizando las 5 actividades en distintos ángulos, velocidades y distancias. Formato sugerido: 1080p/30fps, 10–20 s por actividad, 2–3 repeticiones.
- Públicos: Ver `Entrega 1/DataSets.md` (NTU RGB+D, PKU-MMD, MPII, COCO Keypoints, Kaggle Human Keypoints Tracking). Seleccionaremos subconjuntos adecuados para extracción de pose y etiquetado compatible con nuestras 5 clases.
- Estructura esperada de carpetas (propuesta):
  - `RawData/` videos sin procesar
  - `Annotations/` CSVs con intervalos o etiquetas por frame
  - `DataProcessing/` scripts
  - `Exports/` características tabulares (`features.csv`)

## 6. Análisis exploratorio de datos (EDA)
- Cuaderno: `Entrega 1/data_exploration.ipynb` (listo para ejecutarse en Colab).
- Contenido principal:
  - Instalación de dependencias y carga de video de ejemplo.
  - Extracción de landmarks de pose con MediaPipe y normalización por tamaño de torso.
  - Suavizado temporal y cálculo de características: ángulos de rodilla y cadera, inclinación del tronco, velocidades de muñecas/rodillas/tobillos.
  - Visualizaciones: series temporales de ángulos/inclinación, resumen estadístico.
  - (Opcional) Alineación con anotaciones si se provee un CSV de etiquetas (por intervalos o por frame).
- Producto: `features.csv` exportado para modelado posterior.

## 7. Siguientes pasos
1) Capturar videos propios y consolidar un protocolo de anotación (formato CSV por intervalos y/o framewise).
2) Ejecutar EDA con varios sujetos/condiciones; ajustar normalización y ventanas de suavizado.
3) Definir conjunto de características final y baseline de clasificación (SVM/RandomForest) con validación por sujeto.
4) Hacer búsqueda de hiperparámetros; comparar con XGBoost.
5) Preparar pipeline tiempo real con overlay (label + ángulos + inclinación) y medir latencia.
6) Documentar resultados, riesgos y mejoras para Entrega 2 (nuevos datos, tuning, robustez).

## 8. Estrategias para conseguir más datos
- Captura interna planificada: sesiones cortas con varios voluntarios (consentimiento informado), variando distancia, ropa, iluminación y fondo.
- Anotación asistida: uso de LabelStudio/CVAT con plantillas de etiquetas y revisión por pares.
- Aprovechamiento de datasets públicos: extracción de esqueletos/landmarks y mapeo de etiquetas a nuestras 5 clases.
- Aumentación temporal/geométrica sobre características (no sobre video crudo): time-warping suave, jitter leve, flips izquierda/derecha cuando tenga sentido.
- Convenios con otros grupos del curso para intercambio de muestras etiquetadas con estándares comunes.

## 9. Consideraciones éticas
- Privacidad y consentimiento para todo video propio; anonimización (difuminado facial si se requiere), retención limitada y control de acceso.
- Mitigación de sesgos: diversidad de sujetos/condiciones, reporte por subgrupos y análisis de error.
- Transparencia de uso: el sistema no sustituye evaluación clínica; mensajes claros en interfaz.
- Ver documento separado: `Entrega 1/AnalisisEtico.md`.

## 10. Recursos clave
- MediaPipe: https://ai.google.dev/edge/mediapipe/solutions/guide?hl=es-419
- LabelStudio: https://labelstud.io/
- CVAT vs LabelStudio: https://medium.com/cvat-ai/cvat-vs-labelstudio-which-one-is-better-b1a0d333842e
- Datasets: ver `Entrega 1/DataSets.md`

