# Análisis Ético MoveSense 

## 1. Contexto y alcance
MoveSense analiza video para reconocer actividades básicas (caminar hacia/desde cámara, girar, sentarse, levantarse) y reportar medidas posturales (ángulos, inclinación). El proyecto está orientado a investigación/educación y no sustituye evaluación clínica ni profesional.

## 2. Principios
- Respeto a la privacidad y dignidad de las personas.
- Minimización de datos personales y conservación limitada.
- Transparencia sobre capacidades y limitaciones del sistema.
- Equidad: mitigar sesgos y evaluar desempeño entre subgrupos.
- Seguridad de la información.

## 3. Privacidad y protección de datos
- Consentimiento informado por escrito para toda captura propia; permitir revocatoria y borrado.
- Minimización: grabar sólo lo estrictamente necesario (plano de cuerpo, sin audio si no es requerido; idealmente rostro difuminado cuando aplique).
- Anonimización/Pseudonimización: codificar sujetos con IDs; separar metadatos identificables de los datos analíticos.
- Retención: definir plazos y criterios de eliminación (p. ej., 6–12 meses o fin del curso/proyecto, lo que ocurra primero).
- Acceso: restringido al equipo; repositorios privados; no compartir públicamente videos de personas sin consentimiento explícito.

## 4. Seguridad de la información
- Almacenamiento cifrado cuando sea posible; backups controlados.
- Controles de acceso basados en roles; registro de cambios.
- Transporte seguro (HTTPS) si se comparten artefactos.

## 5. Sesgos y equidad
- Muestreo diverso: género, contexturas, ropa, fondos, iluminación, velocidades y perspectivas.
- Métricas por subgrupo: reportar F1, recall y errores por sujeto/condición; detectar disparidades.
- Mitigación: recolección dirigida donde haya bajo desempeño; balanceo de clases; técnicas de aumentación prudentes.

## 6. Transparencia y explicabilidad
- Interfaz con mensajes claros: “herramienta de apoyo, no diagnóstico”.
- Mostrar confianza de predicción y estabilidad temporal (suavizado) para evitar interpretaciones erróneas frame-a-frame.
- Documentar pipeline y supuestos (normalización por torso, landmarks disponibles, limitaciones en oclusiones).

## 7. Uso responsable
- Prohibido el uso para vigilancia o control sin consentimiento.
- Evitar juicios de valor sobre condición física; el objetivo es educativo y de análisis de movimiento.
- Políticas de uso aceptable en el repositorio.

## 8. Gestión de anotación
- Lineamientos a anotadores: confidencialidad, tratamiento de datos, ejemplos positivos/negativos.
- Doble anotación y resolución de desacuerdos para mejorar calidad y reducir sesgo individual.

## 9. Riesgos y mitigación
- Falsos positivos/negativos en condiciones difíciles → comunicación de incertidumbre, validación adicional.
- Sobreajuste a un sujeto/escena → validación por sujeto y diversidad de escenas.
- Deriva de distribución → pruebas periódicas y actualización de datos/modelos.
