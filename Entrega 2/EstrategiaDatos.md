# Estrategia implementada para la obtención de nuevos datos

## Objetivo
Aumentar y diversificar el dataset para robustecer la clasificación de 5 actividades y la analítica postural, con calidad, trazabilidad y cumplimiento ético.

## 1) Fuentes de datos
- Captura propia controlada (consentimiento informado): variando distancia, perspectiva, iluminación, vestimenta y velocidad.
- Públicos (complementarios): ver `Entrega 1/Docs/DataSets.md`. Criterio: facilidad de extraer pose y mapear etiquetas a nuestras 5 clases.

## 2) Protocolo de captura propia
- Formato: 1080p@30fps, fondo simple, 10–20 s por actividad, 2–3 repeticiones.
- Archivo por sujeto y sesión: `RawData/<sujeto>/<fecha>_<actividad>.mp4`.
- Metadatos (CSV): sujeto_id, distancia, perspectiva, iluminación.

## 3) Anotación
- Herramienta: LabelStudio/CVAT. Esquema: `caminar_adelante`, `caminar_atras`, `girar`, `sentarse`, `levantarse`.
- Exportación: CSV intervalos `[start_s,end_s,label]` o por frame `[frame,label]`.
- Calidad: doble anotación en 10–20% y resolución de desacuerdos.

## 4) Integración de datos públicos
- Extraer pose (MediaPipe) y mapear etiquetas a nuestras 5 clases; excluir ambiguas.
- Documentar licencia y cita.

## 5) Balance y cobertura
- Meta: ≥ 20–30 clips por clase, ≥ 8–10 sujetos. Balance por sujeto y condición.

## 6) Gobernanza de datos
- Estructura: `RawData/`, `Annotations/`, `Exports/`. Privacidad: difuminar rostro si aplica; retención definida.



