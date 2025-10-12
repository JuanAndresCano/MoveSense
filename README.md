# MoveSense

## Project Status

Active

## Contributing Members

**Members:**

- Juan Andrés Cano Ramírez. (https://github.com/JuanAndresCano)
- Pablo Guzmán Alarcón. ([Github handle])

## Contact

Contact the team leader or instructor with any questions or interest in contributing.

## Project Intro/Objective

MoveSense busca desarrollar una herramienta que identifique en tiempo real actividades humanas específicas (caminar hacia/desde la cámara, girar, sentarse, ponerse de pie) y realice el seguimiento de movimientos articulares clave para análisis postural. Se explorará el uso de bases de datos públicas de reconocimiento de actividades con seguimiento articular las cuales han de tener la cantidad suficiente de datos, de la calidad suficiente y variedad necesaria para poder realizar una herramienta de calidad. Adicionalmente, por amor academico y compromiso por el proyecto, se explorará el uso de videos propios de por lo menos, los dos miembros contribuyentes.

## Methods Used

- Machine Learning supervisado (SVM, Random Forest, XGBoost)
- Seguimiento de pose con MediaPipe
- Preprocesamiento y extracción de características
- Métricas de evaluación (precisión, recall, F1-Score)

## Technologies

- Python
- OpenCV
- MediaPipe
- Herramientas de anotación: LabelStudio o CVAT

## Project Description

- Recolección inicial de videos propios de actividades humanas específicas para entrenamiento y prueba.
- Anotación manual y/o automática de segmentos de video con actividades clave usando herramientas especializadas.
- Uso de MediaPipe para extracción de landmarks (caderas, rodillas, muñecas, etc.) y cálculo de ángulos e inclinaciones.
- Aplicación de técnicas de normalización y filtrado para preparar datos para el modelado.
- Definición de métricas para evaluar desempeño del sistema durante experimentación.
- Exploración de datasets públicos de seguimiento articular para complementar datos y validar modelos.
- Planificación y estrategia para ampliación de conjunto de datos.

## Getting Started

- Repositorio contiene carpeta “RawData” con videos iniciales capturados por el equipo.
- Anotaciones manuales en carpeta “Annotations”.
- Scripts para preprocesamiento y análisis exploratorio en “DataProcessing”.
- Documentación sobre captura de videos y uso de herramientas de anotación.
- En el documento DataSets.md se pondrán los datasets públicos considerados para el desarrollo del proyecto.

## Featured Notebooks/Analysis/Deliverables

- Primer análisis exploratorio de datos: data_exploration.ipynb
- Documentación de metodología y métricas: methodology.md
- Plan de trabajo y próximos pasos: roadmap.md
