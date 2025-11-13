# Análisis final de impacto contextual

## 1. Contexto y propósito
MoveSense busca asistir en el reconocimiento de actividades básicas (caminar adelante/atrás, girar, sentarse, pararse) y medir ángulos articulares en tiempo real. La entrega final incorpora modelos refinados (RandomForest completo y PCA+SVM) y un prototipo de despliegue con cámara. El impacto debe evaluarse considerando usuarios potenciales (estudiantes, entrenadores, fisioterapeutas en escenarios controlados) y los riesgos asociados.

## 2. Beneficios observados
- **Retroalimentación inmediata**: el pipeline en tiempo real muestra ángulos y etiqueta suavizada, lo que permite correcciones durante ejercicios.
- **Consistencia de métricas**: la validación cruzada (accuracy ≈0.99) y la reducción de latencia (0.39 ms/muestra con PCA+SVM) habilitan sesiones más fluidas en equipos modestos.
- **Doble versión de modelo**: mantener RF y PCA+SVM ofrece flexibilidad (alta precisión vs. velocidad), facilitando transferir la solución a distintos contextos.
- **Interfaz transparente**: overlay con confianza, FPS y ángulos facilita explicar qué mide el sistema y en qué condiciones baja la fiabilidad.

## 3. Riesgos identificados
- **Privacidad y autorización**: el uso de cámara implica capturar imágenes potencialmente sensibles. Requiere consentimiento explícito, almacenamiento seguro y opciones de anonimización.
- **Generalización limitada**: aunque el desempeño promedio es alto, el conjunto de datos sigue proveniente de pocos sujetos. Personas con diversidad corporal o condiciones de iluminación distintas podrían obtener peores resultados.
- **Falsos positivos/negativos**: confusiones residuales en clases `girar` vs `adelante`/`atrás` pueden afectar la retroalimentación. Necesario comunicar la incertidumbre y revisar manualmente episodios críticos.
- **Dependencia tecnológica**: la solución requiere CPU y cámara funcional; interrupciones o latencias altas pueden generar retroalimentación errónea o tardía.

## 4. Medidas de mitigación
- **Gestión de datos**: aplicar políticas de consentimiento, cifrado local y eliminación periódica (metadata.json sugiere incorporar un registro de sesiones). Considerar difuminar rostros o usar cámaras detrás del sujeto cuando sea viable.
- **Validación continua**: agregar pruebas con nuevos sujetos y escenarios; documentar métricas por subgrupo en `latency_report.json` y futuros reportes.
- **Comunicación en la UI**: mostrar mensajes cuando la confianza caiga por debajo de un umbral, sugerir reintentos y habilitar visualización histórica de probabilidades.
- **Plan de contingencia**: en sesiones supervisadas, el operador debe estar preparado para detener o reiniciar la aplicación; mantener un modo manual para registrar actividades si el modelo falla.

## 5. Impacto en actores y escenarios
- **Estudiantes / investigadores**: facilita experimentos de biomecánica con bajo costo, pero se debe capacitar en buenas prácticas de captura y ética.
- **Entrenadores / fisioterapeutas** (en ambientes controlados): provee métricas objetivas para evaluar progresos, aunque no sustituye criterio profesional. Necesita incluir disclaimers claros dentro de la aplicación y documentación.
- **Institución educativa (Universidad ICESI)**: el proyecto refuerza competencias en IA responsable y puede servir como base para nuevas cohortes. Se recomienda mantener el repositorio privado cuando contenga datos reales y compartir solo los artefactos entrenados.

## 6. Conclusión
La solución tiene potencial para transformar el análisis de actividades básicas en contextos educativos y de entrenamiento. Se alcanzó precisión y latencia adecuadas, y se establecieron medidas para mitigar riesgos principales. El despliegue requiere acompañarse de políticas claras y mejoras iterativas basadas en pruebas reales para garantizar un impacto positivo y responsable.
