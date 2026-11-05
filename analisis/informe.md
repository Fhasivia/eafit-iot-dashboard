# Exploración real del CSV del tótem IoT

Fuente: `proyecto_integrador_eafit_max30102.csv`, descargado del enlace de Notion facilitado por el usuario el 5 de noviembre de 2026. Datos simulados según las instrucciones del proyecto compartidas. No representan diagnósticos médicos.

SHA-256: `dd918095c6174247956749db976400941c2560ca98ccb5b4ca66fb001bde19ea`. El CSV se conserva byte por byte. Para regenerar este informe: `python analizar.py`.

## Estructura y calidad

**2,667 filas y 8 columnas**, 295 estudiantes, 295 NFC y 1 dispositivo.

| Columna original | Tipo leído por Pandas | Nulos |
| --- | --- | ---: |
| `timestamp` | object | 0 |
| `student_id` | object | 0 |
| `nfc_id` | object | 0 |
| `device_id` | object | 0 |
| `heart_rate_bpm` | int64 | 0 |
| `spo2_percent` | float64 | 0 |
| `signal_quality` | float64 | 0 |
| `measurement_status` | object | 0 |

No hay filas idénticas duplicadas, fechas sin zona, fallos de conversión numérica ni estados desconocidos. Tampoco hay BPM no positivos, SpO₂ fuera de 0 a 100 o calidad de señal fuera de 0 a 1. Estos controles describen consistencia técnica, no validación clínica.

Hay 11 instantes compartidos por 22 filas. Cada uno corresponde a estudiantes distintos. No se eliminan por compartir fecha y hora, y no hay duplicados de estudiante e instante. El archivo sólo tiene resolución temporal de un minuto; no permite determinar la secuencia dentro de ese minuto.

Cada estudiante tiene un único NFC y cada NFC corresponde a un único estudiante en este archivo.

## Cinco KPI propuestos

| Indicador | Resultado sin filtros | Regla |
| --- | ---: | --- |
| Mediciones | 2,667 | Todas las filas del filtro |
| Estudiantes | 295 | Identificadores distintos del filtro |
| Mediciones válidas | 97.11% | Filas `valid` / todas las filas del filtro |
| BPM promedio | 75.47 bpm | Media de `heart_rate_bpm`, sólo `valid` |
| SpO₂ promedio | 97.72% | Media de `spo2_percent`, sólo `valid` |

La selección del estado también afecta el denominador. Al seleccionar sólo `invalid`, el porcentaje válido es 0% y los dos promedios no están disponibles. Si faltan datos numéricos en una futura versión del archivo, las medias omiten esos nulos sin imputarlos. No se equipara un valor ausente a cero.

Los cinco KPI son una propuesta inicial. La conversación recuperada menciona cinco obligatorios, pero no incluye su listado exacto; deben cotejarse con la rúbrica completa antes de la entrega.

## Fechas y horas

- UTC: 2026-09-30 00:50:00+00:00 hasta 2026-10-29 00:35:00+00:00.
- America/Bogota: 2026-09-29 19:50:00-05:00 hasta 2026-10-28 19:35:00-05:00.
- Hay 30 fechas locales con registros y 385 filas cambian de fecha al convertir la zona.

Se interpreta el desplazamiento explícito del CSV con `pd.to_datetime(..., utc=True)` y se convierte con `.dt.tz_convert('America/Bogota')`. La columna original se conserva. Los filtros incluyen ambas fechas extremas y los agrupamientos diarios y horarios usan Bogotá. El primer y último día del archivo son fechas de borde; no se asume cobertura completa.

## Hallazgos verificables

1. **Los valores no vacíos no garantizan validez.** Hay 2,590 filas `valid` y 77 `invalid` (2.89% del total). Las 77 inválidas contienen BPM, SpO₂ y calidad de señal numéricos. Se conservan para analizar calidad, pero no entran en promedios del sensor. Ver `resumen_por_estado.csv`.
2. **La actividad registrada es menor los fines de semana.** Al excluir las dos fechas extremas, hay 20 fechas de lunes a viernes con 121.15 registros/día y 8 fechas de fin de semana con 16.50. Describe el patrón del archivo, sin atribuirlo a horarios o causas no documentadas. Ver `actividad_diaria.csv`.
3. **La calidad de señal no explica por sí sola el estado.** La media es 0.8747 en válidas y 0.8677 en inválidas. Los intervalos se solapan: válidas de 0.750 a 1.000, inválidas de 0.754 a 0.998. No hay base para deducir un umbral único ni causalidad. Ver `resumen_por_estado.csv`.
4. **La zona horaria cambia la interpretación del calendario.** El primer registro es 30 de septiembre en UTC y 29 de septiembre en Bogotá. Agrupar directamente el texto UTC desplazaría parte de la actividad a otro día.

## Valores atípicos estadísticos

Se usa el criterio de Tukey por variable sobre filas `valid`: menor que Q1 − 1,5 × IQR o mayor que Q3 + 1,5 × IQR. Se mantienen los registros. Los límites no son rangos clínicos y no reclasifican el estado original.

| Variable | Límite inferior | Límite superior | Filas fuera |
| --- | ---: | ---: | ---: |
| heart_rate_bpm | 41.500 | 109.500 | 32 |
| spo2_percent | 95.150 | 100.350 | 44 |
| signal_quality | 0.626 | 1.122 | 0 |

## Alcance

Este análisis describe mediciones simuladas. No se infieren diagnósticos, salud individual, causas de invalidez ni relaciones causales. Las medias por medición dan más peso a estudiantes con más registros; no son medias con igual peso por estudiante. Los valores observados y la etiqueta `valid` no prueban exactitud del sensor.
